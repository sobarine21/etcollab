import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import threading
import asyncio
from datetime import datetime
import io
from PIL import Image
import docx
import pdfplumber

# Streamlit app configuration
st.set_page_config(page_title="CollabSphere", layout="wide")
st.title("\U0001F91D CollabSphere: Real-Time Collaboration Platform")

# Fetch Supabase URL and Key from Streamlit's secrets
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]

# Create a Supabase client (synchronous version for normal operations)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure the Gemini AI key
genai.configure(api_key=st.secrets["google"]["GOOGLE_API_KEY"])

# Real-time fetch of active workspaces from Supabase
def fetch_workspaces():
    try:
        # Query the workspace list from Supabase
        response = supabase.table("workspaces").select("name").execute()
        return [row["name"] for row in response.data]
    except Exception as e:
        st.error(f"Failed to fetch workspaces: {e}")
        return []

# Real-time workspace creation
def create_workspace(workspace_name):
    try:
        # Insert the new workspace into Supabase
        supabase.table("workspaces").insert({"name": workspace_name}).execute()
        st.success(f"Workspace '{workspace_name}' created.")
    except Exception as e:
        st.error(f"Failed to create workspace: {e}")

# Real-time task fetch and display
def fetch_tasks(workspace):
    try:
        # Query tasks for the selected workspace
        response = supabase.table("tasks").select("*").eq("workspace", workspace).execute()
        return response.data
    except Exception as e:
        st.error(f"Failed to fetch tasks: {e}")
        return []

# Function to add a new task
def add_task(task_description, workspace):
    try:
        task = {
            "task": task_description,
            "workspace": workspace,
            "created_at": datetime.utcnow().isoformat()
        }
        supabase.table("tasks").insert(task).execute()
        st.success(f"Task '{task_description}' added.")
    except Exception as e:
        st.error(f"Error adding task: {e}")

# Asynchronous listener function for Supabase real-time updates
async def listen_to_tasks():
    from supabase import create_client
    from supabase.realtime import RealtimeClient

    # Use the asynchronous RealtimeClient
    client = RealtimeClient(SUPABASE_URL, SUPABASE_KEY)

    # Create the real-time subscription for tasks
    channel = client.channel("tasks")
    await channel.subscribe()

    # Listen for real-time insertions (for example, new tasks)
    await channel.on("INSERT", lambda payload: st.rerun())  # Re-run the app when a task is added

# Function to start the listener in a separate thread
def start_listener():
    asyncio.run(listen_to_tasks())

# Start the listener in a new thread
listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()

# UI for workspace management
st.header("\U0001F3C6 Workspace Management")

# Input field for a new workspace name
workspace_name = st.text_input("Enter a workspace name to join or create one:", placeholder="Workspace Name")
col1, col2 = st.columns([3, 2])

# Button to create workspace
if col1.button("Create Workspace"):
    if workspace_name:
        create_workspace(workspace_name)
    else:
        st.error("Please provide a valid name.")

# Real-time update of the workspace list
st.write("Current Active Workspaces:")
workspace_list = fetch_workspaces()

if workspace_list:
    for ws in workspace_list:
        if col2.button(f"Join Workspace: {ws}", key=ws):
            st.session_state.current_workspace = ws
            st.success(f"Joined '{ws}' workspace.")
            st.rerun()  # Re-render page to reflect changes
else:
    st.info("No active workspaces. Create one to start collaborating.")

# Real-time Task Management Example
st.header("Task Management")

if "current_workspace" in st.session_state:
    workspace = st.session_state.current_workspace
    tasks = fetch_tasks(workspace)
    task_description = st.text_input(f"Enter a task description for '{workspace}':")
    
    if st.button("Add Task"):
        if task_description:
            add_task(task_description, workspace)
        else:
            st.error("Please provide a valid task description.")

    # Display tasks for the current workspace
    if tasks:
        for task in tasks:
            st.write(f"• {task['task']} (Added at {task['created_at']})")
    else:
        st.write("No tasks found for this workspace.")
else:
    st.info("Please join or create a workspace first.")

# Real-time file sharing simulation
def file_upload():
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "docx", "pdf", "jpg", "png"])
    if uploaded_file is not None:
        st.write(f"File uploaded: {uploaded_file.name}")
        st.write(uploaded_file.getvalue())

        # File preview logic based on file type
        if uploaded_file.type.startswith("image/"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        elif uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                st.write(text)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            full_text = "\n".join([para.text for para in doc.paragraphs])
            st.text_area("Document Content", full_text)

# Real-time AI-enhanced Task Suggestions
st.sidebar.header("\U0001F916 Gemini AI Assistant")
ai_tool = st.sidebar.selectbox("Choose an AI Tool:", [
    "Brainstorm Ideas",
    "Summarize Text",
    "Task Prioritization",
    "Custom Prompt"
])

if ai_tool == "Brainstorm Ideas":
    prompt = st.sidebar.text_area("Describe what you need ideas for:", placeholder="E.g., Marketing strategies for product launch")
    if st.sidebar.button("Generate Ideas"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.sidebar.write(response.text)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

if ai_tool == "Task Prioritization":
    task_description = st.sidebar.text_area("Enter your task description here:", placeholder="E.g., Design marketing plan")
    if st.sidebar.button("Prioritize Tasks"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Prioritize the following tasks: {task_description}")
            st.sidebar.write(response.text)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# Collaboration Platform ready
st.write("\U0001F4A1 Collaboration Platform ready.")
