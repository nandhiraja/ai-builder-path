import json
import time
import os
from dotenv import load_dotenv
from groq import Groq

from prompts import get_system_prompt
from tool_registry import TOOLS
from tools import check_availability, reserve_table, suggest_tables

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
MAX_ITERATIONS = 10

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

FUNCTION_MAP = {
    "check_availability": check_availability,
    "reserve_table": reserve_table,
    "suggest_tables": suggest_tables
}


def run_agent(user_message: str, history: list) -> str:
   
    messages = [{"role": "system", "content": get_system_prompt()}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    for _ in range(MAX_ITERATIONS):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        time.sleep(1)  

        assistant_msg = response.choices[0].message
        tool_calls = assistant_msg.tool_calls

        assistant_dict = {
            "role": "assistant",
            "content": assistant_msg.content or ""
        }
        if tool_calls:
            assistant_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments  
                    }
                }
                for tc in tool_calls
            ]
        messages.append(assistant_dict)

      
        if not tool_calls:
            return assistant_msg.content or "Sorry, I could not process that."

        # Execute each tool the agent called
        for tc in tool_calls:

            function_name = tc.function.name
            arguments = json.loads(tc.function.arguments)

            print(f"[Agent] {function_name}({arguments})")

            if function_name not in FUNCTION_MAP:
                result = {"error": f"Unknown tool: {function_name}"}
            else:
                result = FUNCTION_MAP[function_name](**arguments)

            print(f"[Agent] result: {result}")

        
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result)
            })

    return "I'm having trouble processing your request. Please try again."