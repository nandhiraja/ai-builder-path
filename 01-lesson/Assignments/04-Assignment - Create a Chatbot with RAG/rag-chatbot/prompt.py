class PromptBuilder:

    @staticmethod
    def build(context_chunks, user_query):

        context = ""

        for index, chunk in enumerate(context_chunks, start=1):

            source = chunk["metadata"].get("source", "Unknown")

            context += (
                f"Source {index}: {source}\n"
                f"{chunk['text']}\n\n"
            )

        prompt = f"""
                You are an AI assistant for the department.
                
                Your job is to answer questions ONLY using the provided context.
                
                Rules:
                
                1. Use only the retrieved context.
                2. Do not make up information.
                3. If the answer is not present in the context, say:
                   "I couldn't find this information in the department documents."
                4. Be clear and concise.
                5. Mention the source document(s) used.
                
                ==========================
                Retrieved Context
                ==========================
                
                {context}
                
                ==========================
                User Question
                ==========================
                
                {user_query}
                
                ==========================
                Answer
                ==========================
                """

        return prompt.strip()