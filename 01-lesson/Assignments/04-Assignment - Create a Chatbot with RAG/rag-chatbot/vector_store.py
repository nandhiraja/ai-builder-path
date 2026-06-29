import chromadb
from chromadb.config import Settings


class VectorStore:
    """
    ChromaDB Vector Store
    """
    def __init__(
        self,
        db_path="vector_db",
        collection_name="department_documents"
    ):

        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

 
    # Add Documents
    def add_documents(self,ids,documents, embeddings,metadatas ):

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
         )

    
    # Search
    def search(self, query_embedding, top_k=3):
       
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        response = []

        for i in range(len(results["ids"][0])):

            response.append({

                "id":
                    results["ids"][0][i],

                "text":
                    results["documents"][0][i],

                "metadata":
                    results["metadatas"][0][i],

                "distance":
                    results["distances"][0][i]

            })

        return response

    #Total stored chunks.
    def count(self):
       
        return self.collection.count()

    # Delete Collection
    def reset(self):
       
        self.client.delete_collection(
            self.collection.name
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection.name
        )