import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai


# Configure Supabase URL and Key
SUPABASE_URL = "your_supabase_url_here"
SUPABASE_KEY = "your_supabase_key_here"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure the Gemini AI key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App Configuration
st.set_page_config(page_title="CollabSphere", layout="wide")
st.title("\U0001F91D CollabSphere: Real-Time Collaboration Platform")

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
            st.experimental_rerun()
else:
    st.info("No active workspaces. Create one to start collaborating.")

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

# Simulated Canvas Section Placeholder
st.header("\U0001F5A8 Live Whiteboard Simulation")
st.info("Note: Replace this with real-time canvas simulation using your system in production.")
st.markdown("---")
st.write("\U0001F4A1 Collaboration Platform ready.")
