import streamlit as st
import google.generativeai as genai
from datetime import datetime
import random
import time

# Configure the Gemini AI key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App Configuration
st.set_page_config(page_title="CollabSphere", layout="wide")
st.title("\U0001F91D CollabSphere: Real-time Collaboration Platform")

# Anonymous User Login
username = st.text_input("Enter a pseudonym to join anonymously:", placeholder="E.g., CreativeSoul123")
if not username:
    st.warning("Please enter a pseudonym to proceed.")
    st.stop()

st.success(f"Welcome, {username}! Ready to collaborate?")

# Workspace Selection
workspace = st.text_input("Enter or create a workspace name:", placeholder="E.g., TeamAlpha")
if not workspace:
    st.warning("Please provide a workspace name.")
    st.stop()

st.info(f"You are now in the workspace: {workspace}")

# Sidebar for AI Tools
st.sidebar.header("\U0001F916 Gemini AI Assistant")
ai_tool = st.sidebar.selectbox("Choose an AI Tool:", [
    "Brainstorm Ideas", "Summarize Text", "Task Prioritization", "Custom Prompt"
])


# AI Interaction Logic
def handle_ai_requests(tool_name):
    if tool_name == "Brainstorm Ideas":
        prompt = st.sidebar.text_area("Describe what you need ideas for:", placeholder="E.g., Strategies for product launch")
        if st.sidebar.button("Generate Ideas"):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.sidebar.write(response.text)
    elif tool_name == "Summarize Text":
        text_to_summarize = st.sidebar.text_area("Enter text to summarize:")
        if st.sidebar.button("Summarize"):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Summarize: {text_to_summarize}")
            st.sidebar.write(response.text)
    elif tool_name == "Task Prioritization":
        tasks = st.sidebar.text_area("Enter tasks (comma-separated):")
        if st.sidebar.button("Prioritize Tasks"):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Prioritize these tasks: {tasks}")
            st.sidebar.write(response.text)
    elif tool_name == "Custom Prompt":
        custom_prompt = st.sidebar.text_area("Enter custom prompt:")
        if st.sidebar.button("Submit"):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(custom_prompt)
            st.sidebar.write(response.text)


handle_ai_requests(ai_tool)

# Main Collaboration Workspace
st.header("\U0001F4C2 Collaboration Board")


# Shared Notes Section
st.subheader("\U0001F4DD Shared Notes")
if "notes" not in st.session_state:
    st.session_state.notes = ""

# Shared Notes real-time sync simulation
st.session_state.notes = st.text_area(
    "Collaborative Notes:", value=st.session_state.notes, height=200, key="shared_notes"
)

# Task Management Section
st.subheader("\U00002705 Task Management")
if "tasks" not in st.session_state:
    st.session_state.tasks = []

task_input = st.text_input("Add a new task:", placeholder="E.g., Complete proposal")
if st.button("Add Task"):
    if task_input:
        st.session_state.tasks.append(
            {"task": task_input, "status": "Pending", "assigned": username}
        )
        st.success("Task added!")

for idx, task in enumerate(st.session_state.tasks):
    col1, col2, col3 = st.columns([6, 2, 2])
    col1.write(f"{task['task']} (Assigned: {task['assigned']})")
    col2.write(task["status"])
    if col3.button("Mark Complete", key=f"complete_{idx}"):
        st.session_state.tasks[idx]["status"] = "Completed"
        st.experimental_rerun()

# Gamification: Leaderboard Section
st.subheader("\U0001F3C6 Leaderboard")
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

# Simulate leaderboard points dynamically
def update_leaderboard(username, points):
    if username in st.session_state.leaderboard:
        st.session_state.leaderboard[username] += points
    else:
        st.session_state.leaderboard[username] = points


update_leaderboard(username, random.randint(1, 5))  # Simulate points gain
leaderboard_sorted = sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True)

for rank, (user, points) in enumerate(leaderboard_sorted, start=1):
    st.write(f"{rank}. {user}: {points} points")


# File Sharing Section
st.subheader("\U0001F4C4 File Sharing")
uploaded_files = st.file_uploader(
    "Share files with your team here:", type=["pdf", "txt", "docx"], accept_multiple_files=True
)
if uploaded_files:
    for file in uploaded_files:
        st.success(f"Shared file: {file.name}")


# Real-time Chat Simulation
st.subheader("\U0001F4AC Real-time Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.container():
    chat_box = st.empty()
    user_message = st.text_input(
        "Type your message:", placeholder="Type and press Enter"
    )
    if st.button("Send Message"):
        if user_message:
            st.session_state.messages.append({"username": username, "message": user_message})
            st.experimental_rerun()

# Render messages dynamically
if st.session_state.messages:
    for msg in st.session_state.messages:
        st.info(f"{msg['username']}: {msg['message']}")


# Footer Section
st.write("\n---\n")
st.write("\U0001F4A1 Powered by Gemini AI & built with Streamlit")
