import chromadb
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def get_rag_response(query, stream=None):
    chrome_client = chromadb.PersistentClient(path="./chromadb_store")
    collection = chrome_client.get_or_create_collection(name="career_knowledge")
    query_params = {"query_texts": [query], "n_results": 5}
    if stream:
        query_params["where"] = {"stream_category": stream}
    results = collection.query(**query_params)
    chunk_texts = results['documents'][0]
    metadatas = results['metadatas'][0]
    context = "\n\n".join(chunk_texts)
    prompt = f"""You are a warm and knowledgeable career counsellor helping a student navigate their higher education and career choices. 
    Use only the following information to answer: {context}. Cite which document the answer came from. You are strictly not allowed to answer from outside the provided context. Include the user's {query}."""
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    if not response.text:
        raise ValueError("Empty response from Gemini")
    else:
        return {
    "response": response.text,
    "sources": list(set([m["source"] for m in metadatas]))
    }
