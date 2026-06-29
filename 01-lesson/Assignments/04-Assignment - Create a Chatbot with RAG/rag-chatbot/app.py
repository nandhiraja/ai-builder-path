from ollama_client import OllamaClient
from vector_store import VectorStore
from prompt import PromptBuilder


class RAGChatBot:

    def __init__(self):

        self.ollama = OllamaClient()

        self.vector_store = VectorStore()

    def ask(self, question):
        query_embedding = self.ollama.generate_embedding(
                          question
                           )

        retrieved_chunks = self.vector_store.search(
                                 query_embedding=query_embedding,
                                 top_k=3
                             )

        if not retrieved_chunks:

            return (
                "No relevant information found "
                "in the knowledge base."
            )

        prompt = PromptBuilder.build(
            retrieved_chunks,
            question
        )

        answer = self.ollama.chat(prompt)

        return answer, retrieved_chunks


def main():

    print("=" * 60)
    print(" Department RAG Chatbot")
    print("=" * 60)

    print("\nType 'exit' to quit.\n")

    chatbot = RAGChatBot()

    while True:

        question = input("You : ").strip()

        if question.lower() == "exit":
            break

        answer, sources = chatbot.ask(question)

        print("\nAssistant:\n")

        print(answer)

        print("\nSources Used:")

        for source in sources:

            metadata = source["metadata"]

            print(
                f"- {metadata['source']} "
                f"(Chunk {metadata['chunk']})"
                 )

        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()