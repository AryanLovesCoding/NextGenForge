# AI Career Guidance & Admission Intelligence Platform

An AI-powered EdTech platform to help Class 12 students go through career choices, stream selection, degree guidance, and college admissions. Powered by Gemini API, RAG, and a FastAPI-Streamlit architecture.

---

## Project Overview

This platform delivers personalised career stream recommendations, degree guidance, admission intelligence, and AI-generated career roadmaps to Class 12 students across India. Built as part of the NextGen Forge Technologies AI/ML Internship Program.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Student-facing frontend UI |
| FastAPI | REST API backend |
| Gemini API | Generative AI for recommendations and roadmaps |
| LangChain | AI orchestration and RAG pipeline |
| ChromaDB | Vector database for knowledge retrieval |
| SQLite | Student profiles, sessions, conversation history |
| Pandas & NumPy | Data processing |
| PyPDF | PDF document ingestion |
| ReportLab | PDF report generation |
| Render | Cloud deployment |

---

## Folder Structure

```
NextGenForge/
├── frontend/          # Streamlit application and UI components
├── backend/           # FastAPI application, routers, models, services
├── data/              # Career datasets and structured data files
├── knowledge_base/    # Career guidance documents for RAG pipeline
├── reports/           # Generated student PDF reports
├── notebooks/         # Jupyter notebooks for experimentation
├── .env               # Environment variables (not committed)
├── .gitignore         
├── requirements.txt   
└── README.md          
```

---

## Prerequisites

- Python 3.10 or higher
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/)

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/AryanLovesCoding/NextGenForge
   cd NextGenForge
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv NextGenForge
   source NextGenForge/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Gemini API key from Google AI Studio |

---

## Internship Details

| Field | Detail |
|---|---|
| Candidate | Aryan Ajmera |
| Reference Number | NFGT/HR/INT/2026/160 |
| Company | NextGen Forge Technologies |
| Domain | AI/ML Engineering |
