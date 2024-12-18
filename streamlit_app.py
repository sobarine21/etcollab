import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Streamlit App
st.set_page_config(page_title="Firebase Collaboration Platform", layout="wide")
st.title("🚀 Real-Time Collaboration Platform")

# Initialize Firebase
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate({
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"],
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        })
        firebase_admin.initialize_app(cred, {"databaseURL": st.secrets["firebase"]["database_url"]})
        st.success("Firebase initialized successfully")
    except Exception as e:
        st.error(f"Firebase initialization error: {e}")
        st.stop()

# Reference to database
db_ref = db.reference("/collaboration")

# Prompt User for Name
username = st.text_input("Enter your username:", placeholder="e.g., Astronaut42")
if not username:
    st.warning("Please enter a username to proceed.")
    st.stop()

st.success(f"Welcome {username}!")

# Workspace input
workspace = st.text_input("Enter or create a workspace:", placeholder="e.g., Workspace123")
if not workspace:
    st.warning("Please provide a workspace name.")
    st.stop()

# Reference to specific workspace
workspace_ref = db_ref.child(workspace)

# Collaborative Notes Section
st.subheader("📝 Shared Notes")
try:
    notes = workspace_ref.child("notes").get() or ""
    updated_notes = st.text_area("Notes", value=notes, height=300)
    if st.button("Save Notes"):
        workspace_ref.child("notes").set(updated_notes)
        st.success("Notes successfully saved!")
except Exception as e:
    st.error(f"Error fetching or saving notes: {e}")

# Task Management Section
st.subheader("✅ Tasks")
try:
    tasks = workspace_ref.child("tasks").get() or {}
    for task_id, task_info in tasks.items():
        col1, col2, col3 = st.columns([5, 2, 2])
        col1.write(task_info['task'])
        col2.write(task_info['status'])
        if col3.button("Mark Complete", key=f"task_{task_id}"):
            task_info['status'] = "Completed"
            workspace_ref.child("tasks").child(task_id).set(task_info)
            st.success("Task marked as completed.")
except Exception as e:
    st.error(f"Error fetching or updating tasks: {e}")

# Add Task Section
new_task = st.text_input("Add new task:", placeholder="e.g., Prepare team presentation")
if st.button("Add Task"):
    try:
        task_id = workspace_ref.child("tasks").push({
            "task": new_task,
            "status": "Pending",
            "assigned": username
        }).key
        st.success(f"Task added with ID: {task_id}")
    except Exception as e:
        st.error(f"Error adding task: {e}")
