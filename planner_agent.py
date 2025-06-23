from agents import Agent
from agents.mcp import MCPServer
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions


voice_system_prompt = """[Voice Output Guidelines]
Your responses will be delivered via voice, so please:
1. Use conversational, natural language that sounds good when spoken
2. Keep responses concise - ideally 1-2 sentences per point
3. Avoid technical jargon unless necessary, and explain terms simply
4. Pause naturally between topics using brief sentences
5. Be warm and personable in tone
"""


async def create_insurance_agents(mcp_servers: list[MCPServer]) -> Agent:
    """Create the insurance agent workflow with voice optimization"""

    insurance_agent = Agent(
        name="InsuranceAssistant",
        instructions=voice_system_prompt + prompt_with_handoff_instructions("""
        #Identity
            You are a helpful chatbot that answers questions about our insurance plans. 
            #Task
            Use the tools provided to answer the questions. 
            #Instructions
            * Information about plans and policies are best answered with sqlite or rag_output tools.
            * web_search should be used for answering generic health questions that are not directly related to our insurance plans.
            * Evaluate the quality of the answer after the tool call. 
            * Assess whether you are confident in the answer generated.
            * If your confidence is low, try use another tool.
        """),
        mcp_servers=mcp_servers,
        model="gpt-4.1-mini"
    )
    return insurance_agent
