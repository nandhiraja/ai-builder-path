from langchain_chroma import Chroma
from langchain_core.tools.retriever import create_retriever_tool
from langchain_community.embeddings import HuggingFaceEmbeddings

PERSIST_DIR = "chroma_hr_policies"
COLLECTION_NAME = "hr_policy_docs"

def build_hr_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 8}
    )

    tool = create_retriever_tool(
        retriever,
        name="search_hr_policies",
        description="Search internal HR policy documents for hiring, leave, conduct, compliance, employee guidelines, and AI data handling rules."
    )
    return tool