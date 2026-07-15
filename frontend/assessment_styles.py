import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.questions import questions
from backend.services.assessment import calculate_scores
import requests

API_BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

CARD_COLORS = [
    ("rgba(6,93,255,0.12)", "#4f9bff", "#2a4a7a"),
    ("rgba(16,185,129,0.12)", "#34d399", "#1f5c47"),
    ("rgba(160,107,255,0.12)", "#c299ff", "#4a3a7a"),
    ("rgba(245,158,11,0.12)", "#fbbf60", "#7a5a1f"),
    ("rgba(236,72,153,0.12)", "#f472b6", "#7a2a52"),
    ("rgba(132,204,22,0.12)", "#a3e635", "#4a5a1f"),
    ("rgba(239,68,68,0.12)", "#f87171", "#7a2a2a"),
]

def render_question(question_num):
    q = questions[question_num]
    color_bg, color_text, color_border = CARD_COLORS[question_num % len(CARD_COLORS)]
    progress = (question_num) / 20
    st.progress(progress)
    st.caption(f"Question {question_num + 1} of 20")
    st.markdown(f"""
        <div style="
            background: {color_bg};
            border: 1px solid {color_border};
            border-radius: 18px;
            padding: 3rem 2rem;
            margin: 1.5rem 0;
            text-align: center;
            min-height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.4s ease;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        ">
            <div>
                <p style="font-size:1rem; color:{color_text}; opacity:0.85; margin-bottom:0.5rem;">How much would you like to:</p>
                <h2 style="font-size:1.8rem; font-weight:800; color:{color_text}; margin:0; line-height:1.4;">{q['question'].replace('How much would you like to ', '').replace('How much do you ', '').capitalize()}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    ratings = [
        (c1, "😖", "Strongly\nDislike", 1),
        (c2, "😟", "Dislike", 2),
        (c3, "😐", "Unsure", 3),
        (c4, "😊", "Like", 4),
        (c5, "😄", "Strongly\nLike", 5),
    ]
    for col, emoji, label, value in ratings:
        with col:
            st.markdown(f"<div style='text-align:center; font-size:2rem; margin-bottom:0.3rem;'>{emoji}</div>", unsafe_allow_html=True)
            if st.button(label, key=f"btn_{question_num}_{value}", use_container_width=True):
                st.session_state.responses.append(value)
                st.session_state.question_num += 1
                st.rerun()

def render_results():
    scores = calculate_scores(st.session_state.responses)
    st.session_state.assessment_scores = scores
    # Save assessment scores to database
    requests.post(f"{API_BASE_URL}/api/assessment/{st.session_state.student_id}/save", json={
        "STEM": scores["STEM"],
        "Commerce": scores["Commerce"],
        "Humanities": scores["Humanities"],
        "creative": scores["Design/Creative Arts"]
    })
    st.subheader("Your Interest Profile")
    st.caption("Here's how your interests are distributed across different domains (in %).")
    short_scores = {
        "STEM": scores["STEM"] * 100,
        "Commerce": scores["Commerce"] * 100,
        "Humanities": scores["Humanities"] * 100,
        "Creative": scores["Design/Creative Arts"] * 100
    }
    st.bar_chart(short_scores, horizontal=True, height=400)
    st.markdown("<br>", unsafe_allow_html=True)
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if right.button('Next', type="primary"):
        st.session_state.assessment_complete = True
        st.rerun()