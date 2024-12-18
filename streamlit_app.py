import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
import pandas as pd
import numpy as np
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("/credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("CollabSphere")

# Authentication
def login():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.get_user_by_email(email)
            st.success("Logged in as {}".format(user.email))
        except:
            st.error("Invalid credentials")

def register():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            st.success("Registered as {}".format(user.email))
        except:
            st.error("Registration failed")

st.sidebar.title("Menu")
page = st.sidebar.selectbox("Choose a page", ["Login", "Register", "Dashboard"])

if page == "Login":
    login()
elif page == "Register":
    register()
elif page == "Dashboard":
    st.write("Welcome to the Dashboard")

    # Real-time Collaboration
    st.subheader("Real-time Collaboration")
    doc_ref = db.collection("collabs").document("example")
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        st.write(data)
    else:
        st.write("No collaboration data available.")

    # Task Management
    st.subheader("Task Management")
    tasks = ["Task 1", "Task 2", "Task 3"]
    for task in tasks:
        st.checkbox(task)

    # Knowledge Sharing
    st.subheader("Knowledge Sharing")
    if st.button("Share Knowledge"):
        st.write("Sharing knowledge...")

    # AI-enhanced Productivity Tools
    st.subheader("AI-enhanced Productivity Tools")
    if st.button("Enhance Productivity"):
        st.write("Enhancing productivity with AI...")

    # Gamification
    st.subheader("Gamification")
    points = 100
    st.write("You have {} points.".format(points))

    # Integrations
    st.subheader("Integrations")
    if st.button("Integrate"):
        st.write("Integrating with external services...")
