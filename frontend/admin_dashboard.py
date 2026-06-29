from wordcloud import WordCloud
import streamlit as st
import hmac
import os
from dotenv import load_dotenv
import requests
import matplotlib.pyplot as plt

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

load_dotenv()

def check_password():
    if hmac.compare_digest(st.session_state["password_input"], os.getenv("ADMIN_PASSWORD")):
        st.session_state["logged_in"] = True
        del st.session_state["password_input"]
    else:
        st.session_state["logged_in"] = False
        st.error("❌ Incorrect password. Please try again.")
if not st.session_state["logged_in"]:
    st.title("🔒 Locked Application")
    st.text_input(
            "Enter Password", 
            type="password", 
            key="password_input", 
            on_change=check_password
        )
    st.button("Login", on_click=check_password)
    st.stop()

else:
    st.title("Admin Dashboard")
    API_BASE_URL = "http://127.0.0.1:8000"
    data = requests.get(f"{API_BASE_URL}/api/analytics/summary").json()
    st.header("Total students:")
    st.write(data["total_students"])
    st.header("Interest profile distribution:")
    dist = {row[0]: row[1] for row in data["stream_preference_distribution"] if row[0]}
    st.bar_chart(dist)
    st.header("Top 5 career streams recommended:")
    fig, ax = plt.subplots()
    pie_dist = {row[0]: row[1] for row in data["recommended_stream_distribution"] if row[0]}
    ax.pie(list(pie_dist.values()), labels=list(pie_dist.keys()), autopct='%1.1f%%')
    ax.legend(list(pie_dist.keys()), loc="best")
    ax.axis('equal')  
    st.pyplot(fig)
    st.header("Most frequent chatbot query topics:")
    if data["messages"]:
        text = " ".join([msg[0] for msg in data["messages"]])
        wc = WordCloud().generate(text)
    else:
        st.caption("No conversation history yet.")
    st.header("Daily active session counts:")
    fig, ax = plt.subplots()
    dates = [row[0] for row in data["daily_sessions"]]
    counts = [row[1] for row in data["daily_sessions"]]
    ax.plot(dates, counts, color="blue", linewidth=2)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of sessions")
    st.pyplot(fig)


    