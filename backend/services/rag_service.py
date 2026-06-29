from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def classify_intent(query: str):
    """
    Classifies the intent as either admission query or career query using keywords

    Args: query(str): text message input by student

    Returns: (str): the string 'admission' or 'career' based on the type of query it is  
    """
    admission_keywords = ["admission","admissions","apply","application","enroll","enrollment","register","registration","eligibility","eligible","criteria",
    "requirements","qualification","qualify","cutoff","cut-off","merit","seat","seats","counselling","counseling","allotment",
    "college","university","institute","campus","intake","vacancy","deadline","last date","form","documents","certificate","fee",
    "tuition","prospectus","round","quota","reservation","admit","jee","neet","cuet","clat"]
    for keyword in admission_keywords:
        if keyword in query.lower():
            return 'admission'
    return 'career'

def get_rag_response(query, stream=None, chat_history=[]):
    """
    Gets the Retrieval-Augmented Generation response

    Args: 
        query(str): text message input by student
        stream(str): the stream Gemini thinks is best for the student based on the studen't previous responses
        chat_history(list[dict]): all the chat that has happened so far so that it can be injected into the new prompt for context

    Returns: the response for the question along with the sources it referred  
    """
    type_of_query = classify_intent(query)
    if type_of_query == "admission":
        search_kwargs = {"k": 5, "filter": {"topic": {"$in": ["entrance_exams", "syllabus", "application_guide", "scholarships", "academic_calendar"]}}}
    else:
        search_kwargs = {"k": 5}
    vectorstore = Chroma(collection_name="career_knowledge", persist_directory="./chromadb_store")
    retriever = vectorstore.as_retriever(search_kwargs = search_kwargs)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key = api_key)
    prompt = PromptTemplate(template="You are a warm and knowledgeable career counsellor helping a student navigate their higher education and career choices. Use only the following information to answer: {context}. Cite which document the answer came from. You are strictly not allowed to answer from outside the provided context. Include the user's {question}.", input_variables=["context", "question"])
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    for msg in chat_history:
        if msg["role"] == "user":
            memory.chat_memory.add_user_message(msg["content"])
        else:
            memory.chat_memory.add_ai_message(msg["content"])
    chain = ConversationalRetrievalChain.from_llm(llm=llm,retriever=retriever,memory=memory,return_source_documents=True)
    result = chain.invoke({"question": query})
    return {"response": result["answer"], "sources": list(set(doc.metadata.get("source") for doc in result["source_documents"] if doc.metadata.get("source")))}


