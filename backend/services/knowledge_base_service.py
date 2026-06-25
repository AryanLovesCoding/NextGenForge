import os
from pypdf import PdfReader
import chromadb

metadata_map = {
    "JOSAA Business rules.pdf": {"stream_category": "STEM", "topic": "college_admissions"},
    "The_Chartered_Accountant.pdf": {"stream_category": "Commerce", "topic": "career_guide"},
    "Skill-India-Brochure-1.pdf": {"stream_category": "General", "topic": "skill_development"},
    "Report_Skill_Roadmap.pdf": {"stream_category": "General", "topic": "skill_development"},
    "Rankings.pdf": {"stream_category": "General", "topic": "college_rankings"},
    "Pragati Scholarship.pdf": {"stream_category": "General", "topic": "scholarships"},
    "Career_in_Cyber_Security.pdf": {"stream_category": "STEM", "topic": "career_guide"},
    "Career_in_Stock_Market.pdf": {"stream_category": "Commerce", "topic": "career_guide"},
    "CLAT_information_bulletin.pdf": {"stream_category": "Humanities", "topic": "entrance_exams"},
    "CUET_Information_Bulletin.pdf": {"stream_category": "General", "topic": "entrance_exams"},
    "JEE_Mains_Information_Bulletin.pdf": {"stream_category": "STEM", "topic": "entrance_exams"},
    "NEET_Information_Bulletin.pdf": {"stream_category": "STEM", "topic": "entrance_exams"},
    "National scholarship.pdf": {"stream_category": "General", "topic": "scholarships"},
    "Career_in_Foreign_Languages.pdf": {"stream_category": "Humanities", "topic": "career_guide"},
    "Career_in_Industrial_and_Organizational_Psychology.pdf": {"stream_category": "Humanities", "topic": "career_guide"},
    "Career_in_visual_arts_.pdf": {"stream_category": "Creative", "topic": "career_guide"},
    "Career_in_Cloud_Computing.pdf": {"stream_category": "STEM", "topic": "career_guide"},
    "Career_in_Business_Analytics.pdf": {"stream_category": "Commerce", "topic": "career_guide"},
    "Actuarial_Science_Career.pdf": {"stream_category": "Commerce", "topic": "career_guide"},
    "Career_in_Artificial_Intelligence.pdf": {"stream_category": "STEM", "topic": "career_guide"},
}

def ingest_knowledge_base():
    knowledge_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "knowledge_base")
    pdf_files = [f for f in os.listdir(knowledge_base_path) if f.endswith('.pdf')]
    client = chromadb.PersistentClient(path="./chromadb_store")
    collection = client.get_or_create_collection("career_knowledge")
    if collection.count() > 0:
        print("Knowledge base already ingested. Skipping.")
        return
    for pdf in pdf_files:
        text = ""
        existing = collection.get(where={"source": pdf})
        if len(existing['ids']) > 0:
            print(f"Skipping {pdf} - already ingested")
            continue
        reader = PdfReader(os.path.join(knowledge_base_path, pdf))
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        chunks = []
        start = 0
        while start < len(text):
            chunks.append(text[start:start + 2000])
            start += 1800
        metadata = metadata_map.get(pdf, {"stream_category": "General", "topic": "general"})
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"source": pdf, "stream_category": metadata["stream_category"], "topic": metadata["topic"]}],
                ids=[f"{pdf}_chunk_{i}"]
            )

if __name__ == "__main__":
    ingest_knowledge_base()