
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from rag import VectorIndex

def use_rag(chat_llm, raw_text: str, source_type: str, *, k: int = 6):

    docs = [Document(page_content=raw_text, metadata={"source_type": source_type})]

    collection = f"genius_{source_type}".lower()
    index = VectorIndex()
    index.build_or_load(docs, collection)
    retriever = index.as_retriever(k=k)

    contextualize_prompt  = ChatPromptTemplate.from_messages([
        ("system", "Rewrite the user query to be self-contained using the chat history. Do not answer."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    history_aware_retriever = create_history_aware_retriever(chat_llm, retriever, contextualize_prompt)

    quality_prompt = ChatPromptTemplate.from_messages([
        ("system", "Use the provided context to answer. If unsure, say you don't know.\n\nContext:\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    quality_chain = create_stuff_documents_chain(chat_llm, quality_prompt)

    chain = create_retrieval_chain(history_aware_retriever, quality_chain)

    # Return Only The Final Answer Text For Streaming In The Chat UI
    return chain.pick("answer")