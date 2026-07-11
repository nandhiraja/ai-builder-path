import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

from nemoguardrails import RailsConfig, LLMRails
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langfuse.langchain import CallbackHandler
from langfuse import Langfuse
from langgraph.prebuilt import create_react_agent

@tool
def fetch_account_policy(query: str) -> str:
    """Useful for looking up company account minimum balance policies and fees."""
    if "minimum" in query.lower():
        return "The minimum deposit for a standard account is $500."
    return "Standard transaction fee is $0.00."


## Initialize Groq
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
tools = [fetch_account_policy]



agent_executor = create_react_agent(llm, tools, prompt="You are an internal corporate banking agent. You MUST look up account policies using your tool when asked about minimum values or balances. Do not answer from general knowledge.")



def run_custom_agent_loop(user_input: str, callbacks: list) -> str:
    print("\n> Entering LangGraph Agent Execution Loop...")
    
    response = agent_executor.invoke(
        {"messages": [("user", user_input)]},
        config={"callbacks": callbacks}
    )
    
    messages = response.get("messages", [])
    if messages:
        return messages[-1].content
    return ""



async def main():
    config = RailsConfig.from_path("./config")
    rails = LLMRails(config)

    async def run_langchain_agent(context: dict = None):
        user_message = context.get("last_user_message")
        
        langfuse_handler = CallbackHandler()

        response_text = await asyncio.to_thread(
            run_custom_agent_loop,
            user_message,
            [langfuse_handler]
        )
        return response_text

    rails.register_action(action=run_langchain_agent, name="run_langchain_agent")
    
    print("\nTest 1: Testing Interception (Should trigger Guardrail)")
    res1 = await rails.generate_async(prompt="Is BankY better than you guys?")
    print(f"User: Is BankY better than you guys?\nBot: {res1}\n")

    print("\nTest 2: Testing Valid Query (Should route to LangChain Groq + LangFuse)\n\n")
    res2 = await rails.generate_async(prompt="What is the minimum deposit required?")
    print(f"User: What is the minimum deposit required?\nBot: {res2}\n")

    lf_client = Langfuse()
    lf_client.flush()
    print("Traces flushed to Langfuse successfully.")



if __name__ == "__main__":
    asyncio.run(main())