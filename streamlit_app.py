import streamlit as st
import requests

st.title("Internal DB Query")

url = "https://zmxnoeekcvtptybentct.supabase.co/functions/v1/internal-db-query"

api_key = st.text_input("YOUR_API_KEY", type="password")
database_id = st.text_input("database_id")
query_text = st.text_area("query_text", "SELECT * FROM users LIMIT 10")

if st.button("Run"):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    payload = {
        "database_id": database_id,
        "query_text": query_text
    }

    r = requests.post(url, json=payload, headers=headers)

    st.write("Status:", r.status_code)
    try:
        st.json(r.json())
    except:
        st.write(r.text)
