import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamlit_tags import st_tags
from backend.services.student_services import create_student, update_student_interests
from backend.services.assessment import assessment_scores, calculate_scores
from backend.services.gemini_services import get_chat_response
from backend.schemas.student import StudentCreate
import streamlit as st
from data.questions import questions
from assessment_styles import render_question, render_results
from recommendation_ui import render_stream_recommendation

API_BASE_URL = "http://127.0.0.1:8000"

#Initialising session states
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'welcome_done' not in st.session_state:
    st.session_state.welcome_done = False

if 'assessment_intro_done' not in st.session_state:
    st.session_state.assessment_intro_done = False

if 'question_num' not in st.session_state:
    st.session_state.question_num = 0

if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'assessment_scores' not in st.session_state:
    st.session_state.assessment_scores = {}

if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Welcome page
if not st.session_state.welcome_done:
    if st.button("Skip to College Comparison (Debug)", key="debug_10"):
        st.session_state.welcome_done = True
        st.session_state.step = 10
        st.session_state.student_id = 1
        st.rerun()
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 4rem 2rem; text-align:center;">
        <h1 style="font-size:3rem; font-weight:700; margin-bottom:1rem;">Welcome!</h1>
        <p style="font-size:1.2rem; color:#A0AEC0; max-width:600px; line-height:1.8;">
            Please fill in the following forms to help us know you better and personalise your career guidance.
        </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("Get Started →", use_container_width=True):
            st.session_state.welcome_done = True
            st.rerun()
    st.stop()

# Personal information form
if st.session_state.step == 1:
    st.subheader("Personal information")
    st.caption("Please fill in all your personal information.")
    user_name = st.text_input(label="Enter full name*")
    "---"
    user_city = st.text_input(label="Enter city*")
    "---"
    user_grade = st.selectbox("Which class are you in?*", ["9","10","11","12"], index=None)
    "---"
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if right.button('Next'):
        #Error handling
        if not user_name or not user_city or user_grade is None:
            st.error("Please fill in all fields before proceeding.")
        elif not user_name.replace(" ", "").isalpha():
            st.error("Name can only contain letters.")
        elif not user_city.replace(" ", "").isalpha():
            st.error("City name can only contain letters.")
        elif len(user_name.strip().split()) < 2:
            st.error("Please enter your full name.")
        else:
            st.session_state.name = user_name
            st.session_state.city = user_city
            st.session_state.grade = user_grade
            student_id = create_student(StudentCreate(
                name=user_name,
                city=user_city,
                stream_preference="",
                interests=[],
                academic_level=""
            ))
            st.session_state.student_id = student_id
            st.session_state.step += 1
            st.rerun()

# Academic profile form
elif st.session_state.step == 2:
    st.subheader("Academic profile")
    st.caption("Please fill in all details in regard to your academic profile.")
    user_subjects = []
    custom_subject = ""
    user_stream = st.selectbox("Which stream are you interested in?*", ['STEM','Commerce','Humanities'])
    "---"
    if user_stream == 'STEM':
        user_subjects = st.multiselect("Which subjects are you interested in?*", 
                                       ["Physics", "Chemistry", "Mathematics", "Biology","Computer Science", 
                                        "Information Technology","Engineering Graphics", "Other"])
    elif user_stream == 'Commerce':
        user_subjects = st.multiselect("Which subjects are you interested in?*", 
                                       ["Accountancy", "Business Studies", "Economics","Mathematics", 
                                        "Informatics Practices","Entrepreneurship", "Other"])
    elif user_stream == 'Humanities':
        user_subjects = st.multiselect("Which subjects are you interested in?*", 
                                       ["History", "Geography", "Political Science","Sociology", "Psychology", 
                                        "Economics","English Literature", "Hindi Literature","Legal Studies", 
                                        "Fine Arts","Physical Education", "Other"])
    "---"
    if "Other" in user_subjects:
        custom_subject = st.text_input("Please specify your subject")
    user_marks = st.slider("Select academic performance range:*", 0, 100, (75, 90))
    "---"
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if left.button('Back'):
        st.session_state.step -= 1
        st.rerun()
    if right.button('Next'):
        #Error handling
        if not user_stream or len(user_subjects) == 0:
            st.error("Please fill in all fields before proceeding.")
        elif "Other" in user_subjects and len(custom_subject) == 0:
            st.error("Please specify your custom subject.")
        else:
            st.session_state.stream = user_stream
            st.session_state.subjects = user_subjects
            st.session_state.custom = custom_subject
            st.session_state.marks = user_marks
            st.session_state.step += 1
            st.rerun()

# Keywords form
elif st.session_state.step == 3:
    st.subheader("Career Aspirations")
    st.caption("Type a keyword, press tab when it shows up, and press enter to add it. Add up to 5 aspirations.")
    user_keywords = keywords = st_tags(label='Enter Keywords:*', text='Press enter to add more',
                                       suggestions=[
                                                    'Doctor', 'Engineer', 'Lawyer', 'Designer', 'Data Scientist',
                                                    'Entrepreneur', 'Teacher', 'Architect', 'Chartered Accountant',
                                                    'Civil Services', 'Journalist', 'Psychologist', 'Pilot', 'Chef',
                                                    'Filmmaker', 'Animator', 'Game Developer', 'Researcher', 'Banker',
                                                    'Stock Analyst', 'Marketing', 'HR Manager', 'Product Manager',
                                                    'Software Developer', 'Cybersecurity', 'AI Engineer', 'Nurse',
                                                    'Pharmacist', 'Dentist', 'Surgeon', 'Economist', 'Social Worker',
                                                    'Politician', 'Army Officer', 'Navy Officer', 'Air Force Officer',
                                                    'Fashion Designer', 'Interior Designer', 'Athlete', 'Coach'],
                                       maxtags=5)
    "---"
    left, m1, m2, m3, m4, m5, right = st.columns(7)
    if left.button('Back'):
        st.session_state.step -= 1
        st.rerun()
    if right.button('Submit'):
        #Error handling
        invalid_keyword = any(not key.replace(" ", "").isalpha() for key in user_keywords)
        if invalid_keyword:
            st.error("Keywords can only contain letters.")
        elif len(user_keywords) == 0:
            st.error("Please add at least one keyword.")
        elif len(user_keywords) > 5:
            st.error("Please enter a maximum of 5 keywords.")
        else:
            st.session_state.keywords = user_keywords
            update_student_interests(st.session_state.student_id, st.session_state.subjects, user_keywords)
            st.session_state.step += 1
            st.rerun()

# Confirmation screen
elif st.session_state.step == 4:
    st.subheader("Summary")
    st.badge("Received the following information", icon=":material/check:", color="green")
    user_information = {
    "Field": ["Name", "City", "Class", "Stream", "Subjects", "Marks", "Keywords"],
    "Answers": [st.session_state.name, st.session_state.city, st.session_state.grade, st.session_state.stream, 
                (", ".join(st.session_state.subjects)), 
                (f"{st.session_state.marks[0]}% - {st.session_state.marks[1]}%"), 
                (", ".join(st.session_state.keywords))]
    }
    st.dataframe(user_information, hide_index=True)
    "---"
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if left.button('Back'):
        st.session_state.step -= 1
        st.rerun()
    elif right.button('Next'):
        st.session_state.step += 1
        st.rerun()

# Assessment page
elif st.session_state.step == 5:
    if not st.session_state.assessment_intro_done:
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 4rem 2rem; text-align:center;">
            <h1 style="font-size:3rem; font-weight:700; margin-bottom:1rem;">Almost there!</h1>
            <p style="font-size:1.2rem; color:#A0AEC0; max-width:600px; line-height:1.8;">
                Please answer the following questions to help us personalise your guidance.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("Start →", use_container_width=True):
                st.session_state.assessment_intro_done = True
                st.rerun()
        st.stop()

    # Assessment complete - transition page
    if st.session_state.question_num == 20 and st.session_state.assessment_complete:
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 4rem 2rem; text-align:center;">
            <h1 style="font-size:3rem; font-weight:700; margin-bottom:1rem;">Thank you!</h1>
            <p style="font-size:1.2rem; color:#A0AEC0; max-width:600px; line-height:1.8;">
                Here is your career guidance based on your profile and assessment.
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("Continue →", use_container_width=True):
                st.session_state.step += 1
                st.rerun()
        st.stop()
    elif st.session_state.question_num == 20:
        render_results()
        st.stop()
    else:
        render_question(st.session_state.question_num)

# Google Gemini stream recommendation
elif st.session_state.step == 6:
    payload = {
        "scores": st.session_state.assessment_scores,
        "academic_level": f"{st.session_state.marks[0]}-{st.session_state.marks[1]}",
        "keywords": st.session_state.keywords
    }
    response = requests.post(f"{API_BASE_URL}/api/recommend/stream", json=payload)
    if response.status_code == 200:
        res = response.json()
        render_stream_recommendation(res)
    else:
        st.error("Could not get recommendation. Please try again.")
    "---"
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if left.button('Back'):
        st.session_state.step -= 1
        st.rerun()
    if right.button('Next'):
        st.session_state.step += 1
        st.rerun()

# Google Gemini degree recommendation
elif st.session_state.step == 7:
    response = requests.get(f"{API_BASE_URL}/api/recommend/degrees/{st.session_state.student_id}")
    if response.status_code == 200:
        res = response.json()
        st.header("Recommended Degrees")
        for degree in res['degrees']:
            with st.expander(degree['degree_name']):
                st.subheader("Description:")
                st.markdown(degree['description'])
                st.subheader("Career Pathways:")
                st.markdown(", ".join(degree['career_pathways']))
                st.subheader("Entrance Exams:")
                st.markdown(", ".join(degree['entrance_exams']))
                st.subheader("Timeline:")
                st.markdown(degree['timeline'])
    else:
        st.error("Could not get recommendations. Please try again.")
    "---"
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if left.button('Back'):
        st.session_state.step -= 1
        st.rerun()
    if right.button('Next'):
        st.session_state.step += 1
        st.rerun()

# AI ChatBot
elif st.session_state.step == 8:
    # Persistent sidebar - conversation history
    with st.sidebar:
        st.title("💬 Conversation History")
        if st.session_state.chat_history:
            for msg in st.session_state.chat_history:
                role_label = "You" if msg["role"] == "user" else "AI"
                st.caption(f"**{role_label}:** {msg['content'][:80]}...")
            if st.button("Clear History"):
                st.session_state.chat_history = []
                st.rerun()
        else:
            st.caption("No conversation history yet.")
    st.subheader("Career Guidance Chat")
    st.caption("Ask me anything about your career, stream, or college admissions.")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    user_input = st.chat_input("Ask me anything about your career...")
    if user_input:
        st.chat_message("user").write(user_input)
        student_context = {
            "stream": st.session_state.stream,
            "subjects": st.session_state.subjects,
            "marks": st.session_state.marks,
            "keywords": st.session_state.keywords,
            "scores": st.session_state.assessment_scores
        }
        payload = {
            "message": user_input,
            "chat_history": st.session_state.chat_history,
            "student_context": student_context
        }
        response = requests.post(f"{API_BASE_URL}/api/chat", json=payload)
        if response.status_code == 200:
            ai_response = response.json()["response"]
        else:
            ai_response = "Sorry, I couldn't process your request. Please try again."
        st.chat_message("assistant").write(ai_response)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    "---"
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if left.button('Back'):
        st.session_state.step -= 1
        st.rerun()
    if right.button('Next'):
        st.session_state.step += 1
        st.rerun()
    
# RoadMap
elif st.session_state.step == 9:
    st.subheader("RoadMap")
    st.caption("Here's the roadmap for your career: ")
    student_id = st.session_state.student_id
    response = requests.get(f"{API_BASE_URL}/api/roadmap/{student_id}")
    col1, col2, col3, col4, col5 = st.columns(5)
    if response.status_code == 200:
        roadmap = response.json()
        with col1:
            st.subheader("Class 11-12")
            st.write(roadmap['class_11_12_preparation'])

        with col2:
            st.subheader("Entrance Exams")
            for exam in roadmap['entrance_exam_timeline']:
                st.write(f"**{exam['exam']}** — {exam['when']}")
                st.caption(exam['preparation_tip'])

        with col3:
            st.subheader("Undergraduate")
            for milestone in roadmap['undergraduate_milestones']:
                st.write(f"**{milestone['year']}**")
                st.write(milestone['focus'])

        with col4:
            st.subheader("Internships")
            st.write(roadmap['internship_milestones'])

        with col5:
            st.subheader("Industry Entry")
            st.write(roadmap['industry_entry_pathway'])
    else:
        st.error("Could not generate roadmap. Please try again.")
        st.stop()
    "---"
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if left.button('Back'):
        st.session_state.step -= 1
        st.rerun()
    if right.button('Next'):
        st.session_state.step += 1
        st.rerun()

elif st.session_state.step == 10:
    st.subheader("College Comparision")
    st.caption("Here's the top 30 colleges in India: ")
    all_colleges = requests.get(f"{API_BASE_URL}/api/colleges").json()
    max_fee = max(int(c['annual_fees'].replace(",", "")) for c in all_colleges)
    col1, col2, col3 = st.columns(3)
    with col1:
            stream_filter = st.selectbox("Stream", [None, "STEM", "Commerce", "Humanities"])
    with col2:
        state_filter = st.selectbox("State", [None, "Delhi", "Maharashtra", "Tamil Nadu", "Uttar Pradesh", "West Bengal", "Uttarakhand", "Assam", "Karnataka", "Rajasthan", "Telangana", "Haryana"])
    with col3:
        fee_filter = st.slider("Max Annual Fee (₹)", 0, max_fee, max_fee, step = 50000)

    params = {}
    if stream_filter:
        params["stream"] = stream_filter
    if state_filter:
        params["state"] = state_filter
    if fee_filter > 0:
        params["max_fee"] = fee_filter
        
    filtered_colleges = requests.get(f"{API_BASE_URL}/api/colleges", params=params).json()
    college_names = [c['name'] for c in filtered_colleges]
    selected = st.multiselect("Select 2-3 colleges to compare", college_names, max_selections=3)
    if selected:
        selected_data = [c for c in filtered_colleges if c['name'] in selected]
        comparison = {
            "Field": ["Stream", "City", "State", "Ranking", "Annual Fees", "Entrance Exam", "Placement Average", "Notable Alumni"]
        }
        for c in selected_data:
            comparison[c['name']] = [c['stream'], c['city'], c['state'], c['ranking'], c['annual_fees'], c['entrance_exam'], c['placement_average'], c['notable_alumni']]
        st.dataframe(comparison, hide_index=True)
    "---"
    left, m1, m2, m3, m4, m5, m6, m7, right = st.columns(9)
    if left.button('Back'):
        st.session_state.step -= 1
        st.rerun()
    elif right.button('Next'):
        st.session_state.step += 1
        st.rerun()
