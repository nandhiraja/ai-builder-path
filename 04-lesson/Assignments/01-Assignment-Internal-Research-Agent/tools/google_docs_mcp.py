import os
from langchain_mcp_adapters.client import MultiServerMCPClient

async def load_google_docs_mcp_tools():
    client = MultiServerMCPClient(
        {
            "googledocs": {
                "transport": "sse",
                "url": os.getenv("GOOGLE_DOCS_MCP_URL"),
            }
        }
    )
    tools = await client.get_tools()
    return tools