from __future__ import annotations
import os
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

DEFAULT_PERSIST_DIR = os.getenv("VECTORSTORE_DIR", ".chroma")

class VectorIndex:
    def __init__(self, persist_dir: str = DEFAULT_PERSIST_DIR):
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        self.vectorstore = None
    
    def build_or_load(self, docs: List[Document], collection_name: str):
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        if docs:
            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120, separators=["\n\n", "\n", ". ", " ", ""])
            chunks = splitter.split_documents(docs)
            self._vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name=collection_name,
                persist_directory=self.persist_dir
            )
            self._vectorstore.persist()
        else:
            self._vectorstore = Chroma(
                embedding_function=embeddings,
                persist_directory=self.persist_dir,
                collection_name=collection_name
            )
    
    def as_retriever(self, k: int = 6):
        if self._vectorstore is None:
            raise RuntimeError("Vectorstore not built or loaded. Invoke build_or_load() first.")
        return self._vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": k, "fetch_k": max(k*3,10), "lambda_mult": 0.5},
        )
