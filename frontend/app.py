import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamlit_tags import st_tags
from backend.services.student_services import create_student
from backend.services.assessment import assessment_scores, calculate_scores
from backend.schemas.student import StudentCreate
from backend.services.assessment import calculate_scores
import streamlit as st
from data.questions import questions
from backend.services.assessment import calculate_scores
from assessment_styles import render_question, render_results, render_welcome

API_BASE_URL = "http://127.0.0.1:8000"

#Initialising session states
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'question_num' not in st.session_state:
    st.session_state.question_num = 0

if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'assessment_started' not in st.session_state:
    st.session_state.assessment_started = False

if 'assessment_scores' not in st.session_state:
    st.session_state.assessment_scores = {}

if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False

# Assessment questions form for insight on interests
if st.session_state.step == 1:
    if st.session_state.question_num == 20 and st.session_state.assessment_complete:
        st.header("         Thanks!")
        st.subheader("Please fill the following forms to help us personalise your career guidance.")
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("Start →", use_container_width=True):
                st.session_state.step += 1
                st.rerun()
        st.stop()
    elif st.session_state.question_num == 20:
        render_results()
        st.stop()
    elif not st.session_state.assessment_started:
        render_welcome()
        st.stop()
    else:
        render_question(st.session_state.question_num)

# Personal info form
elif st.session_state.step == 2:
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
            assessment_scores(student_id, st.session_state.assessment_scores)
            st.session_state.step += 1
            st.rerun()

# Academic profile form
elif st.session_state.step == 3:
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

# Keywords
elif st.session_state.step == 4:
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
            st.session_state.step += 1
            st.rerun()

# Confirmation screen
elif st.session_state.step == 5:
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
        st.ession_state.step += 1
        st.rerun()

#Google Gemini stream recommendation display
elif st.session_state.step == 6:
    payload = {
    "scores": st.session_state.assessment_scores,
    "academic_level": f"{st.session_state.marks[0]}-{st.session_state.marks[1]}",
    "keywords": st.session_state.keywords
    }
    response = requests.post(f"{API_BASE_URL}/api/recommend/stream", json = payload)
    if response.status_code == 200:
        res = response.json()
        st.header(f"Suggested stream: {res['recommended_stream']}")
        st.subheader(f"Justification:")
        st.markdown(f"Suggested stream: {res['justification']}")
        if res['alternative_stream']:
            st.subheader(f"Alternative stream: {res['alternative_stream']}")
    else:
        st.error("Could not get recommendation. Please try again.")