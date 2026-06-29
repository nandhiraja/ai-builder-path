import ollama


class OllamaClient:

    def __init__(self, chat_model="llama3.1:8b",embedding_model="nomic-embed-text"):
        
        self.chat_model = chat_model
        self.embedding_model = embedding_model

    def generate_embedding(self, text):
       
        response = ollama.embed(
            model=self.embedding_model,
            input=text
        )

        return response["embeddings"][0]

    def generate_embeddings(self, texts):
      
        response = ollama.embed(
            model=self.embedding_model,
            input=texts
        )

        return response["embeddings"]

    def chat(self, prompt):
      
        response = ollama.chat(
            model=self.chat_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]