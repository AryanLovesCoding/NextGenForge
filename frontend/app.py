import streamlit as st
from streamlit_tags import st_tags

#Initialising session state 
if 'step' not in st.session_state:
    st.session_state.step = 1

# Personal info form
if st.session_state.step == 1:
    st.subheader("Personal information")
    st.caption("Please fill in all your personal information.")
    user_name = st.text_input(label="Enter full name*")
    "---"
    user_city = st.text_input(label="Enter city*")
    "---"
    user_grade = st.selectbox("Which class are you in?*", ["9","10","11","12"], index=None)
    "---"
    if st.button('Next'):
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
    if st.button('Next'):
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
elif st.session_state.step == 3:
    st.subheader("Career Aspirations")
    st.caption("Type a keyword, press tab when it shows up, and press enter to add it. Add up to 5 aspirations.")
    user_keywords = keywords = st_tags(label='Enter Keywords:*',text='Press enter to add more',
                                       suggestions=[
                                                    'Doctor', 'Engineer', 'Lawyer', 'Designer', 'Data Scientist',
                                                    'Entrepreneur', 'Teacher', 'Architect', 'Chartered Accountant',
                                                    'Civil Services', 'Journalist', 'Psychologist', 'Pilot', 'Chef',
                                                    'Filmmaker', 'Animator', 'Game Developer', 'Researcher', 'Banker',
                                                    'Stock Analyst', 'Marketing', 'HR Manager', 'Product Manager',
                                                    'Software Developer', 'Cybersecurity', 'AI Engineer', 'Nurse',
                                                    'Pharmacist', 'Dentist', 'Surgeon', 'Economist', 'Social Worker',
                                                    'Politician', 'Army Officer', 'Navy Officer', 'Air Force Officer',
                                                    'Fashion Designer', 'Interior Designer', 'Athlete', 'Coach'],maxtags=5)
    "---"
    if st.button('Next'):
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