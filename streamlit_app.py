import streamlit as st
from supabase import create_client, Client
import time

# Initialize Supabase client (replace these with your actual Supabase credentials)
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Automatically create the tables if they don't exist
def create_tables_if_not_exist():
    """Create tables in Supabase if they do not exist"""
    try:
        # Create 'workspaces' table if it does not exist
        supabase.rpc("create_workspaces_table").execute()
    except Exception as e:
        print("Workspaces table exists or error:", e)
    
    try:
        # Create 'ideas' table if it does not exist
        supabase.rpc("create_ideas_table").execute()
    except Exception as e:
        print("Ideas table exists or error:", e)

# Create a new workspace
def create_workspace(workspace_name: str):
    """Create a new workspace in Supabase"""
    response = supabase.table('workspaces').insert({
        'name': workspace_name
    }).execute()
    return response.data[0]['id']

# Fetch all workspaces
def get_workspaces():
    """Fetch all workspaces from Supabase"""
    response = supabase.table('workspaces').select('name').execute()
    return [workspace['name'] for workspace in response.data]

# Fetch ideas for a specific workspace
def get_workspace_ideas(workspace_name: str):
    """Get ideas for a specific workspace from Supabase"""
    response = supabase.table('workspaces').select('id').eq('name', workspace_name).execute()
    workspace_id = response.data[0]['id']
    ideas_response = supabase.table('ideas').select('idea').eq('workspace_id', workspace_id).execute()
    return [idea['idea'] for idea in ideas_response.data]

# Add a new idea to a workspace
def add_idea(workspace_name: str, idea: str):
    """Add a new idea to the specified workspace"""
    # First, get the workspace ID
    response = supabase.table('workspaces').select('id').eq('name', workspace_name).execute()
    workspace_id = response.data[0]['id']
    
    # Insert the new idea
    response = supabase.table('ideas').insert({
        'workspace_id': workspace_id,
        'idea': idea
    }).execute()
    
    return response.data

# Listen for real-time updates to the 'ideas' table in the selected workspace
def listen_for_ideas(workspace_name: str):
    """Listen for real-time changes to ideas in the selected workspace"""
    # Get workspace ID
    response = supabase.table('workspaces').select('id').eq('name', workspace_name).execute()
    workspace_id = response.data[0]['id']
    
    # Subscribe to real-time updates for the 'ideas' table
    def on_insert(payload):
        new_idea = payload['new']['idea']
        st.session_state.ideas.append(new_idea)  # Append new idea to session state
    
    # Listen to real-time insert events in the 'ideas' table
    supabase.table('ideas').on('INSERT', on_insert).eq('workspace_id', workspace_id).subscribe()

# Set the title of the app
st.title("Collaborative Brainstorming Workspace")

# Ensure that tables are created
create_tables_if_not_exist()

# Sidebar - workspace creation
st.sidebar.header("Create a New Workspace")

# User input for workspace name
workspace_name = st.sidebar.text_input("Enter workspace name")

if st.sidebar.button("Create Workspace"):
    if workspace_name:
        create_workspace(workspace_name)
        st.sidebar.success(f"Workspace '{workspace_name}' created!")
    else:
        st.sidebar.warning("Please enter a valid workspace name.")

# Display list of available workspaces
st.sidebar.header("Available Workspaces")
workspaces = get_workspaces()
selected_workspace = st.sidebar.selectbox("Select a workspace", workspaces)

if selected_workspace:
    st.subheader(f"Brainstorming Ideas in '{selected_workspace}'")
    
    # Display existing ideas in the selected workspace (using session_state for real-time updates)
    if 'ideas' not in st.session_state:
        st.session_state.ideas = get_workspace_ideas(selected_workspace)
    
    for idea in st.session_state.ideas:
        st.write(f"- {idea}")

    # Input for new idea
    new_idea = st.text_input("Add your idea")
    
    if st.button("Add Idea"):
        if new_idea:
            add_idea(selected_workspace, new_idea)
            st.session_state.ideas.append(new_idea)  # Append to session state for real-time update
            st.success(f"Idea '{new_idea}' added to workspace '{selected_workspace}'!")
        else:
            st.warning("Please enter an idea before submitting.")
    
    # Real-time updates for new ideas
    listen_for_ideas(selected_workspace)
    
    # Keep the session state updated by re-running the app every 2 seconds for real-time updates
    time.sleep(2)
    st.experimental_rerun()
