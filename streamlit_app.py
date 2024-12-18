import streamlit as st
import google.generativeai as genai
from datetime import datetime
import random

# Configure the Gemini AI key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App Configuration
st.set_page_config(page_title="CollabSphere", layout="wide")
st.title("\U0001F91D CollabSphere: Real-Time Collaboration Platform")

# Anonymous User Login
username = st.text_input("Enter a pseudonym to join anonymously:", placeholder="E.g., CreativeSoul123")
if not username:
    st.warning("Please enter a pseudonym to proceed.")
    st.stop()

st.success(f"Welcome, {username}! Let's start collaborating!")

# Workspace Selection
workspace = st.text_input("Enter or create a workspace name:", placeholder="E.g., TeamAlpha")
if not workspace:
    st.warning("Please provide a workspace name.")
    st.stop()

st.info(f"You are in the workspace: {workspace}")

# Sidebar for AI Tools
st.sidebar.header("\U0001F916 Gemini AI Assistant")
ai_tool = st.sidebar.selectbox("Choose an AI Tool:", [
    "Brainstorm Ideas",
    "Summarize Text",
    "Task Prioritization",
    "Custom Prompt"
])

# AI Tools Logic
if ai_tool == "Brainstorm Ideas":
    prompt = st.sidebar.text_area("Describe what you need ideas for:", placeholder="E.g., Marketing strategies for product launch")
    if st.sidebar.button("Generate Ideas"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.sidebar.write(response.text)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

elif ai_tool == "Summarize Text":
    text_to_summarize = st.sidebar.text_area("Enter text to summarize:", placeholder="Paste a long document or text here")
    if st.sidebar.button("Summarize"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Summarize this: {text_to_summarize}")
            st.sidebar.write(response.text)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# Main Collaboration Workspace
st.header("\U0001F4C2 Collaboration Board")

# Shared Chat Section
st.subheader("\U0001F4AC Live Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []

def send_message():
    """Appends a new message to the session state."""
    user_message = st.session_state.chat_input
    if user_message:
        st.session_state.messages.append(f"{username}: {user_message}")
        st.session_state.chat_input = ""

# Display the chat messages in real-time
for msg in st.session_state.messages:
    st.write(msg)

# Input for sending new messages
st.text_input("Type your message:", key="chat_input", on_change=send_message)

st.markdown("---")

# Live Whiteboard Section
st.subheader("\U0001F5A8 Live Whiteboard")

# Use Session State to maintain shared canvas across users
if "drawing_data" not in st.session_state:
    st.session_state.drawing_data = []

# Draw tools on live whiteboard
st.write("Draw something in the canvas:")
canvas = st.canvas(
    key="shared_whiteboard",
    width=500,
    height=400,
    background_color="white",
    stroke_width=3,
    drawing_mode="freedraw",
    point_display_radius=3,
)

# Save drawing data in session state for real-time sharing
if canvas:
    st.session_state.drawing_data = canvas.get_drawings()

# Task Management Section
st.header("\U00002705 Task Management")
if "tasks" not in st.session_state:
    st.session_state.tasks = []

task_input = st.text_input("Add a new task:", placeholder="E.g., Complete project proposal")
if st.button("Add Task"):
    st.session_state.tasks.append({"task": task_input, "status": "Pending", "assigned": username})
    st.success("Task added!")

if st.session_state.tasks:
    for idx, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([6, 2, 2])
        col1.write(f"{task['task']} (Assigned: {task['assigned']})")
        col2.write(task['status'])
        if col3.button("Mark Complete", key=f"complete_{idx}"):
            task['status'] = "Completed"
            st.experimental_rerun()

# Footer
st.write("\n---\n")
st.write("\U0001F4A1 Powered by Gemini AI and built with Streamlit.")
