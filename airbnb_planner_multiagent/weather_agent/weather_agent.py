import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioServerParameters,
)


def create_weather_agent() -> LlmAgent:
    """Constructs the ADK agent."""
    # Use the Google AI Studio routing of LiteLLM by default. Prefixing the
    # model name with "gemini/" prevents the client from treating it as a
    # Vertex AI model (which would require ADC credentials).
    LITELLM_MODEL = os.getenv('LITELLM_MODEL', 'gemini/gemini-2.5-flash')
    return LlmAgent(
        model=LiteLlm(model=LITELLM_MODEL),
        name='weather_agent',
        description='An agent that can help questions about weather',
        instruction="""You are a specialized weather forecast assistant. Your primary function is to utilize the provided tools to retrieve and relay weather information in response to user queries. You must rely exclusively on these tools for data and refrain from inventing information. Ensure that all responses include the detailed output from the tools used and are formatted in Markdown""",
        tools=[
            MCPToolset(
                connection_params=StdioServerParameters(
                    command='python',
                    args=['./weather_mcp.py'],
                ),
            )
        ],
    )
