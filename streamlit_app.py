import streamlit as st
from supabase import create_client, Client

# **Supabase Credentials**
SUPABASE_URL = st.secrets["supabase_url"]  # URL from Supabase project
SUPABASE_ANON_KEY = st.secrets["supabase_anon_key"]  # Key from Supabase project

# Connect to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Title
st.title("Streamlit + Supabase Example")

# Menu for navigation
menu = ["Home", "Add Note", "View Notes"]
choice = st.sidebar.selectbox("Menu", menu)

# **Home Section**
if choice == "Home":
    st.subheader("Welcome!")
    st.write(
        "This example demonstrates how to integrate Supabase with Streamlit to fetch and insert data into a database."
    )

# **Add Note Section**
elif choice == "Add Note":
    st.subheader("Add a New Note")

    # Input fields
    note_title = st.text_input("Title")
    note_content = st.text_area("Content")

    if st.button("Submit"):
        if note_title and note_content:
            # Insert data into Supabase database
            response = supabase.table("notes").insert(
                {"title": note_title, "content": note_content}
            ).execute()

            st.success("Note added successfully!")
        else:
            st.error("Both fields are required!")

# **View Notes Section**
elif choice == "View Notes":
    st.subheader("View All Notes")

    # Fetch data from the Supabase database
    try:
        response = supabase.table("notes").select("*").execute()
        notes = response.data

        if notes:
            for note in notes:
                st.write(f"### {note['title']}")
                st.write(note["content"])
                st.markdown("---")
        else:
            st.info("No notes available.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
