import os
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@tool
def list_docs_tool() -> str:
    """Lists all available internal corporate documentation files."""
  
    try:
        if not os.path.exists(DATA_DIR):
            return "No documentation directory found."
        files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
        if not files:
            return "No documentation files available."
        return "Available documentation files:\n" + "\n".join(f"- {f}" for f in files)
    except Exception as e:
        return f"Error listing documents: {str(e)}"

@tool
def read_file_tool(filename: str) -> str:
   
    """Reads the contents of an internal corporate documentation file by name."""
    
    safe_path = os.path.basename(filename)
    full_path = os.path.join(DATA_DIR, safe_path)

    if not os.path.exists(full_path):
        return f"Error: File '{safe_path}' not found. Use list_docs_tool to see available files."

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{safe_path}': {str(e)}"

@tool
def web_search_tool(query: str) -> str:
   
    """Search the web for external information, industry benchmarks, market updates, or public comparison data."""
    
    try:
        search = TavilySearch(max_results=3)
        raw = search.invoke(query)

        if isinstance(raw, str):
            return raw

        if isinstance(raw, list):
            formatted = []
            for idx, res in enumerate(raw, 1):
                if isinstance(res, dict):
                    formatted.append(
                        f"Result {idx}:\n"
                        f"Title: {res.get('title', 'N/A')}\n"
                        f"URL: {res.get('url', 'N/A')}\n"
                        f"Snippet: {res.get('content', '')}\n"
                    )
                else:
                    formatted.append(f"Result {idx}: {res}\n")
            return "\n".join(formatted)

        return str(raw)
   
    except Exception as e:
        return f"Web Search Error: {str(e)}"
