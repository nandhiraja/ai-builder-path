from langchain_community.tools.tavily_search import TavilySearchResults

def build_web_search_tool():
    return TavilySearchResults(
        max_results=5,
        name="industry_web_search",
        description="Search the web for industry benchmarks, market trends, and regulatory or compliance updates."
    )