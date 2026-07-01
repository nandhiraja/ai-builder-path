import ollama


class OllamaClient:

    def __init__(self, model="llama3.1:8b"):
        self.model = model

    def chat(self, prompt: str) -> str:

        try:

            response = ollama.chat(

                model=self.model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]

            )

            return response["message"]["content"]

        except Exception as e:

            return f"Error: {str(e)}"