# Technical Architecture

This document describes the system architecture of the AI Career Guidance & Admission Intelligence Platform: its major components, the RAG pipeline that powers the career guidance chatbot, and the database schema.

---

## 1. System Component Diagram

```mermaid
graph TB
    subgraph Client
        A[Streamlit Frontend<br/>frontend/app.py]
    end

    subgraph Backend["FastAPI Backend"]
        B[API Routers]
        C[Services Layer<br/>gemini_services / rag_service /<br/>student_services / pdf_service]
        D[slowapi Rate Limiter]
    end

    subgraph Data["Data & AI Layer"]
        E[(SQLite<br/>Student / Session /<br/>ConversationHistory /<br/>AssessmentScores)]
        F[(ChromaDB<br/>Vector Store<br/>35+ knowledge base docs)]
        G[Gemini API<br/>gemini-2.5-flash]
    end

    A -->|HTTP requests<br/>requests.post/get| B
    B --> D
    D --> C
    C -->|CRUD| E
    C -->|similarity search| F
    C -->|generate_content| G
    G -->|JSON responses| C
    C -->|responses + sources + confidence| B
    B -->|JSON| A
```

**Key points:**
- The frontend never talks to Gemini, ChromaDB, or SQLite directly — all access goes through the FastAPI backend, keeping the API key and data layer server-side only.
- `slowapi` rate limiting sits in front of the four Gemini-cost endpoints (`/api/recommend/stream`, `/api/recommend/degrees/{id}`, `/api/roadmap/{student_id}`, `/api/chat/rag`).
- Streamlit-side `st.cache_data` caches recommendation/roadmap responses per student for 24h; FastAPI-side `lru_cache` caches the (largely static) colleges endpoint. Analytics is deliberately left uncached since it reflects live usage data.

---

## 2. RAG Pipeline Diagram

```mermaid
graph TD
    A[Student query<br/>+ chat_history + student_context] --> B{is_prompt_injection?}
    B -->|Yes| C[400 rejected<br/>'Prompt violated our policies']
    B -->|No| D{classify_intent<br/>keyword match}
    D -->|admission-related| E[Retrieval filtered to:<br/>entrance_exams, syllabus,<br/>application_guide, scholarships,<br/>academic_calendar]
    D -->|career-related| F[Unfiltered retrieval<br/>top-k=5]
    E --> G[ChromaDB similarity_search]
    F --> G
    G --> H[Retrieved chunks + metadata]
    H --> I[Custom PromptTemplate<br/>student profile injected via f-string<br/>+ retrieved context]
    I --> J[ConversationalRetrievalChain<br/>+ ConversationBufferMemory]
    J --> K[Gemini API]
    K --> L[Grounded response]
    H --> M[similarity_search_with_score<br/>separate call, no extra Gemini cost]
    M --> N[Avg L2 distance < 1.3?]
    N -->|Yes| O[Confidence: High]
    N -->|No| P[Confidence: Medium]
    L --> Q[Response + Sources + Confidence]
    O --> Q
    P --> Q
    Q --> R[Saved to ConversationHistory]
    Q --> S[Returned to frontend:<br/>chat bubble + sources expander<br/>+ confidence badge]
```

**Key design decisions:**
- **Defense in depth against prompt injection:** a keyword filter rejects known injection phrases before any Gemini call; the prompt itself is also reinforced to redirect off-topic/role-override attempts that slip past the filter.
- **Intent-based retrieval filtering** avoids surfacing irrelevant admission documents for career questions and vice versa.
- **Confidence scoring** required restructuring away from `ConversationalRetrievalChain`'s default relevance-score method (miscalibrated for this Chroma collection's L2 distance metric) to a raw-distance threshold empirically derived by comparing on-topic vs. off-topic query distances (average distance < 1.3 → High).
- **Student personalisation** is injected via plain string interpolation into the prompt template rather than as extra `chain.invoke()` keys, because `ConversationalRetrievalChain`'s memory component only supports a single top-level input key.

---

## 3. Database Schema

```mermaid
erDiagram
    Student {
        int id PK
        string name
        string city
        string stream_preference
        string interests
        int academic_level
        text created_at
    }
    Session {
        int id PK
        int student_id FK
        text created_at
    }
    ConversationHistory {
        int id PK
        int session_id FK
        string role
        string message
        text timestamp
    }
    AssessmentScores {
        int id PK
        int student_id FK
        real stem_score
        real commerce_score
        real humanities_score
        real creative_score
        text created_at
    }
    CollegeComparision {
        int id PK
        string name
        string stream
        string city
        string state
        int ranking
        string annual_fees
        string entrance_exam
        string placement_average
        text notable_alumni
    }

    Student ||--o{ Session : "has"
    Session ||--o{ ConversationHistory : "has"
    Student ||--o{ AssessmentScores : "has"
```

**Indexing:** `Session.student_id`, `ConversationHistory.session_id`, `AssessmentScores.student_id`, and `Student.stream_preference` are indexed to keep lookups fast as student volume grows (added in W10.1). `CollegeComparision` has no foreign key to `Student` — it is static reference data, not linked per-student.

**Note:** `CollegeComparision` is intentionally excluded from the entity relationships above since it has no foreign key link to `Student` — it's standalone seed data queried directly with filters (stream, state, max fee) rather than joined against student records.
