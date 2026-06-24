import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.questions import questions
from backend.services.assessment import calculate_scores, assessment_scores

CARD_COLORS = [
    ("#E6F1FB", "#0C447C"),
    ("#E1F5EE", "#085041"),
    ("#EEEDFE", "#3C3489"),
    ("#FAEEDA", "#633806"),
    ("#FBEAF0", "#72243E"),
    ("#EAF3DE", "#27500A"),
    ("#FAECE7", "#712B13"),
]

def render_question(question_num):
    q = questions[question_num]
    color_bg, color_text = CARD_COLORS[question_num % len(CARD_COLORS)]
    progress = (question_num) / 20
    st.progress(progress)
    st.caption(f"Question {question_num + 1} of 20")
    st.markdown(f"""
    <div style="
        background: {color_bg};
        border-radius: 16px;
        padding: 3rem 2rem;
        margin: 1.5rem 0;
        text-align: center;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.5s ease;
    ">
        <div>
            <p style="font-size:1rem; color:{color_text}; opacity:0.8; margin-bottom:0.5rem;">How much would you like to:</p>
            <h2 style="font-size:1.8rem; font-weight:700; color:{color_text}; margin:0; line-height:1.4;">{q['question'].replace('How much would you like to ', '').replace('How much do you ', '').capitalize()}</h2>
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
            st.markdown(f"<div style='text-align:center; font-size:1.8rem;'>{emoji}</div>", unsafe_allow_html=True)
            if st.button(label, key=f"btn_{question_num}_{value}", use_container_width=True):
                st.session_state.responses.append(value)
                st.session_state.question_num += 1
                st.rerun()

def render_results():
    scores = calculate_scores(st.session_state.responses)
    st.session_state.assessment_scores = scores
    # Save assessment scores to database
    assessment_scores(st.session_state.student_id, scores)
    st.subheader("Your Interest Profile")
    st.caption("Here's how your interests are distributed across different domains.")
    short_scores = {
        "STEM": scores["STEM"],
        "Commerce": scores["Commerce"],
        "Humanities": scores["Humanities"],
        "Creative": scores["Design/Creative Arts"]
    }
    st.bar_chart(short_scores, horizontal=True, height=400)
    st.markdown("<br>", unsafe_allow_html=True)
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if right.button('Next'):
        st.session_state.assessment_complete = True
        st.rerun()