import streamlit as st
from PIL import Image, ImageDraw
import google.generativeai as genai
import numpy as np


# Configure the Gemini AI key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App Configuration
st.set_page_config(page_title="CollabSphere", layout="wide")
st.title("\U0001F91D CollabSphere: Real-Time Collaboration Platform")

# Workspace Management
if "workspaces" not in st.session_state:
    st.session_state.workspaces = []  # Store workspace names

st.header("\U0001F3C6 Workspace Management")

# Allow users to create a new workspace or join an existing one
workspace_name = st.text_input("Enter a workspace name to join or create one:", placeholder="Workspace Name")
col1, col2 = st.columns([3, 2])

# Button to create a new workspace
if col1.button("Create Workspace"):
    if workspace_name and workspace_name not in st.session_state.workspaces:
        st.session_state.workspaces.append(workspace_name)
        st.success(f"Workspace '{workspace_name}' created successfully.")
    else:
        st.error("Workspace already exists or name is invalid.")

# Allow joining existing workspaces
st.write("Available Workspaces:")
for ws in st.session_state.workspaces:
    if col2.button(f"Join Workspace: {ws}", key=ws):
        st.session_state.current_workspace = ws
        st.success(f"Joined workspace '{ws}'")
        st.experimental_rerun()

if "current_workspace" in st.session_state:
    st.success(f"Welcome to the '{st.session_state.current_workspace}' workspace!")

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


# Simulated Canvas Alternative for Basic Whiteboard-Like Functionality
st.header("\U0001F5A8 Live Whiteboard Simulation")

canvas_size = (400, 400)  # Whiteboard size in pixels
if "canvas_image" not in st.session_state:
    # Create a blank white canvas (numpy array with white background)
    st.session_state.canvas_image = np.ones(canvas_size, dtype=np.uint8) * 255

st.write("Click on 'Enable Drawing' to draw on the whiteboard.")
drawing = st.checkbox("Enable Drawing Mode", value=False)

if drawing:
    st.write("Drawing mode is now active. Simulated whiteboard ready.")
    st.image(st.session_state.canvas_image, use_column_width=True)
else:
    st.image(st.session_state.canvas_image, use_column_width=True)

st.markdown("---")
st.write("\U0001F4A1 Collaboration Platform ready.")
