import asyncio
import os

from servers import ServerProcess

from agents import set_default_openai_key
from agents.mcp import MCPServerSse, MCPServerStdio
from dotenv import load_dotenv
from planner_agent import create_insurance_agents
from voice_io import continuous_voice_conversation

async def main():
    """Main function to run the voice assistant"""
    this_dir = os.getcwd()
    server_file = os.path.join(this_dir, "search_server.py")

    async with ServerProcess(server_file):
        # Initialize MCP servers
        async with MCPServerSse(
            name="SSE Python Server",
            params={
                "url": "http://localhost:8000/sse",
                "timeout": 120.0
            },
            client_session_timeout_seconds=120.0
        ) as search_server:
            async with MCPServerStdio(
                cache_tools_list=True,
                client_session_timeout_seconds=600,
                params={"command": "uvx", "args": ["mcp-server-sqlite", "--db-path", "./sample_database.db"]}
            ) as sql_server:
                # Create insurance agent with MCP tools
                agent = await create_insurance_agents([search_server, sql_server])

                # Run the voice assistant
                try:
                    await continuous_voice_conversation(agent)
                except Exception as e:
                    print(f"nError in voice conversation: {e}")
                    raise


if __name__ == "__main__":
    load_dotenv()
    set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
    asyncio.run(main())
