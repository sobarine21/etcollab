import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import threading
import asyncio

# Streamlit app configuration
st.set_page_config(page_title="CollabSphere", layout="wide")
st.title("\U0001F91D CollabSphere: Real-Time Collaboration Platform")

# Fetch Supabase URL and Key from Streamlit's secrets
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]

# Create a Supabase client
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

# Asynchronous listener function for Supabase real-time updates
async def listen_to_tasks():
    from supabase import create_client
    async with create_client(SUPABASE_URL, SUPABASE_KEY) as client:
        channel = client.realtime.channel("tasks")
        await channel.subscribe()

        # Listen for real-time insertions (for example, new tasks)
        await channel.on("INSERT", lambda payload: st.rerun())  # Correct usage

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

# Real-time file sharing simulation
def file_upload():
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "docx", "pdf", "jpg", "png"])
    if uploaded_file is not None:
        st.write(f"File uploaded: {uploaded_file.name}")
        st.write(uploaded_file.getvalue())

# Real-time Task Management Example
st.header("Task Management")
task = st.text_input("Enter a task description:")
if st.button("Add Task"):
    try:
        supabase.table("tasks").insert({"task": task, "workspace": st.session_state.current_workspace}).execute()
        st.success(f"Task '{task}' added to the workspace.")
    except Exception as e:
        st.error(f"Error: {e}")

# Sidebar for AI Tools
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

# Collaboration Platform ready
st.write("\U0001F4A1 Collaboration Platform ready.")
