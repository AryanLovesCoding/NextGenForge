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