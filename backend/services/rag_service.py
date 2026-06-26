from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def get_rag_response(query, stream=None):
    vectorstore = Chroma(collection_name="career_knowledge", persist_directory="./chromadb_store")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key = api_key)
    prompt = PromptTemplate(template="You are a warm and knowledgeable career counsellor helping a student navigate their higher education and career choices. Use only the following information to answer: {context}. Cite which document the answer came from. You are strictly not allowed to answer from outside the provided context. Include the user's {question}.", input_variables=["context", "question"])
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type_kwargs={"prompt": prompt}, return_source_documents=True)
    result = chain.invoke({"query": query})
    return {"response": result["result"], "sources": list(set(doc.metadata.get("source") for doc in result["source_documents"] if doc.metadata.get("source")))}