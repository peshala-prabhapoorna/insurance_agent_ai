import os
from mcp.server.fastmcp import FastMCP
from openai import OpenAI, NotFoundError
from agents import set_tracing_export_api_key

from dotenv import load_dotenv, set_key
load_dotenv()

# Create server
mcp = FastMCP("Search Server")
_vector_store_id = os.environ.get("VECTOR_STORE_ID")


def _run_rag(query: str) -> str:
    """Do a search for answers within the knowlege base and internal documents
    of the user.
    Args:
        query: The user query
    """
    if not _vector_store_id:
        raise Exception("Error: Vector store id is not available")

    results = client.vector_stores.search(
        vector_store_id=_vector_store_id,
        query=query,
        rewrite_query=True
    )
    return results.data[0].content[0].text


def _summarize_rag_response(rag_output: str) -> str:
    """Summarize the RAG response using GPT-4
    Args:
        rag_output: the RAG response
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        tools=[{"type": "web_search_preview"}],
        input="Summarize the following text concisely \n\n" + rag_output
    )
    return response.output_text


@mcp.tool()
def generate_rag_output(query: str) -> str:
    """Generate a summarized RAG output for a given query
    Args:
        query: The user query
    """
    print("[debug-server] generate_rag_output: ", query)
    rag_output = _run_rag(query)
    return _summarize_rag_response(rag_output)


@mcp.tool()
def run_web_search(query: str) -> str:
    """Run a web search for the given query.
    Args:
        query: The user query
    """
    print("[debug-server] run_web_search: ", query)
    response = client.responses.create(
        model="gpt-4.1-mini",
        tools=[{"type": "web_search_preview"}],
        input=query
    )
    return response.output_text


def index_documents(directory: str):
    """Index the documents in the given directory to the vector store
    Args:
        directory: The directory to index the documents from
    """

    SUPPORTED_EXTENSIONS = {
        '.pdf', '.txt', '.md', '.docx', '.pptx', '.csv', '.rtf', '.html', '.json', '.xml'
    }
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    # Filter files for supported extenstions only
    supported_files = []
    for file_path in files:
        _, ext = os.path.splitext(file_path)
        if ext.lower() in SUPPORTED_EXTENSIONS:
            supported_files.append(file_path)
        else:
            print(f"[warning] Skipping unsopported file for retrieval: {file_path}")

    vector_store = client.vector_stores.create(name="Support FAQ")
    global _vector_store_id
    _vector_store_id = vector_store.id
    set_key(
        dotenv_path=".env",
        key_to_set="VECTOR_STORE_ID",
        value_to_set=vector_store.id
    )

    for file_path in supported_files:
        # Upload each file to the vector store, ensuring the file handle is closed
        with open(file_path, "rb") as fp:
            client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store.id,
                file=fp
            )
            print(f"[debug-server] Uploading file: {file_path}")


if __name__ == "__main__":
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    set_tracing_export_api_key(openai_api_key)
    client = OpenAI(api_key=openai_api_key)

    def create_vector_store():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        samples_dir = os.path.join(current_dir, "sample_files")
        print("\nCreating new vector store and indexing files...")
        index_documents(samples_dir)

    # Check if files are alread indexed and a vector store exists
    if _vector_store_id:
        try:
            response = client.vector_stores.retrieve(
                vector_store_id=_vector_store_id
            )
        except NotFoundError as e:
            print(f"Error: Vector store not found: {e}")
            create_vector_store()
    else:
        create_vector_store()

    mcp.run(transport="sse")
