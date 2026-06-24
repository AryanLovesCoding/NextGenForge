import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def get_stream_recommendation(scores: dict, academic_level: str, keywords: list):
    client = genai.Client(api_key=api_key)
    
    json_structure = '{"recommended_stream": "one of: Science/PCM, Science/PCB, Commerce, Humanities", "justification": "minimum 150 word personalised justification", "alternative_stream": "only if scores are very close, otherwise null"}'
    
    prompt = f"You are a college counsellor helping students pick their subject choices and career paths for their future. The student has taken an interests assessment and gotten the following results: {scores}, where each score is normalised between 0 and 1 and 1 indicates the strongest interest in that domain. The student has also filled out their personal information and stated that their academic performance is between {academic_level}%. They have also provided a list of keywords as future career aspirations and streams they are interested in: {keywords}. Based on this information, recommend one of four streams (Science/PCM, Science/PCB, Commerce, Humanities) with a minimum 150-word personalised justification, explaining in detail your suggestions for their career and choices they should make. Note that a high Design/Creative Arts score may indicate suitability for design-oriented paths within Science/PCM or Arts streams. In case their scores and interests match multiple career choices and domains, please mention all such possibilities. Respond ONLY with a JSON object with no additional text, no markdown, no backticks, using this exact structure: {json_structure}"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    
    if not response.text:
        raise ValueError("Empty response from Gemini")
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON response from Gemini: {response.text}")
    
def get_degree_recommendation(stream: str, interests: list, scores: dict):
    client = genai.Client(api_key=api_key)

    json_structure = '{"degrees": [{"degree_name": "most preferable degree for the student", "description": "comprehensive description of what the degree is and what it entails", "career_pathways": ["career 1", "career 2", "career 3"], "entrance_exams": ["exam 1", "exam 2", "exam 3"], "timeline": "complete career timeline including degree duration and time to first job"}, {"degree_name": "...", "description": "...", "career_pathways": ["...", "...", "..."], "entrance_exams": ["...", "...", "..."], "timeline": "..."}, {"degree_name": "...", "description": "...", "career_pathways": ["...", "...", "..."], "entrance_exams": ["...", "...", "..."], "timeline": "..."}, {"degree_name": "...", "description": "...", "career_pathways": ["...", "...", "..."], "entrance_exams": ["...", "...", "..."], "timeline": "..."}, {"degree_name": "...", "description": "...", "career_pathways": ["...", "...", "..."], "entrance_exams": ["...", "...", "..."], "timeline": "..."}]}'

    prompt = f"You are a college counsellor helping students understand which degree is best for them. The student has filled out a form and is interested in {stream}. The student has taken an interests assessment and gotten the following results: {scores}, where each score is normalised between 0 and 1 and 1 indicates the strongest interest in that domain. Additionally, in the form they have also mentioned their interests, take those into account: {interests}. Respond ONLY with a JSON object with no additional text, no markdown, no backticks, using this exact structure: {json_structure}"

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    
    if not response.text:
        raise ValueError("Empty response from Gemini")
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON response from Gemini: {response.text}")
    
def get_chat_response(message: str, chat_history: list[dict], student_context: dict):
    client = genai.Client(api_key=api_key)
    prompt = f"""You are a warm and knowledgeable career counsellor helping a student navigate their higher education and career choices. 

        Student profile:
        - Stream preference: {student_context.get('stream', 'Not specified')}
        - Subjects: {student_context.get('subjects', 'Not specified')}
        - Academic performance: {student_context.get('marks', 'Not specified')}%
        - Career aspirations: {student_context.get('keywords', 'Not specified')}
        - Interest profile scores: {student_context.get('scores', 'Not specified')}

        Conversation so far: {chat_history}

        Student's current question: {message}

        Answer the student's question in a warm, helpful, and conversational tone in 150-200 words. Refer to their specific profile where relevant. Only answer career and admission related questions. If asked something unrelated, politely redirect the conversation back to career guidance."""
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    if not response.text:
        raise ValueError("Empty response from Gemini")
    else:
        return response.text