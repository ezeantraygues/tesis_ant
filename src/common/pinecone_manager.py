from typing import List
from langchain_pinecone import PineconeVectorStore
import os

index_name = os.getenv("PINECONE_INDEX_NAME")


from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document


# Create the AzureOpenAIEmbeddings object
azure_openai_embeddings = AzureOpenAIEmbeddings(
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME"),
    api_version="2024-08-01-preview",
)

class PineconeManager:
    def __init__(self, k: int = 4):
        self.db = PineconeVectorStore(index_name=index_name, embedding=azure_openai_embeddings)
        self.k = k
        self.results_history: List[List[str]] = []

    def upload(self, vector_list:List[tuple]) -> None:
        """
            vector_list: list of tuples, each with a pair (text,metadata)
        """

        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        
        for vector in vector_list:
            text, metadata = vector
            docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
            for doc in docs:
                doc.metadata = metadata
            self.db.add_documents(documents=docs)     


    def search(self, query: str) -> List[dict]:
        # Search for the query in the database
        results = self.db.similarity_search(query, k=self.k)
        search_results = [{**result.metadata, "texto":result.page_content} for result in results]
        return search_results
