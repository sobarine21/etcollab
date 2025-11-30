# streamlit_app.py
import streamlit as st
import requests
import json

st.set_page_config(page_title="Internal DB Query", layout="centered")

st.title("🔍 Supabase Internal DB Query")

st.markdown(
    "Run SQL against your internal DB function "
    "(`/functions/v1/internal-db-query`)."
)

# ---- Configuration ----
col1, col2 = st.columns(2)
with col1:
    base_url = st.text_input(
        "Supabase project URL (without trailing slash)",
        value="https://zmxnoeekcvtptybentct.supabase.co",
        help="Same base URL that appears in your curl command."
    )
with col2:
    fn_path = st.text_input(
        "Function path",
        value="/functions/v1/internal-db-query",
        help="Path after the base URL."
    )

api_key = st.text_input(
    "x-api-key",
    type="password",
    help="The API key used in the curl example (not your anon/public key)."
)

database_id = st.text_input(
    "database_id",
    placeholder="your-database-id"
)

default_query = "SELECT * FROM users LIMIT 10"
query_text = st.text_area(
    "SQL query_text",
    value=default_query,
    height=150
)

run_btn = st.button("▶️ Run Query")

# ---- Action ----
if run_btn:
    if not (base_url and fn_path and api_key and database_id and query_text.strip()):
        st.error("Please fill in all fields before running the query.")
    else:
        url = f"{base_url.rstrip('/')}{fn_path}"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
        }

        payload = {
            "database_id": database_id,
            "query_text": query_text,
        }

        st.info(f"Sending request to: `{url}`")
        with st.spinner("Executing query..."):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=60)
            except Exception as e:
                st.error(f"Request failed: {e}")
            else:
                st.code(f"Status: {resp.status_code}", language="bash")

                # Try to parse JSON; fall back to raw text
                try:
                    data = resp.json()
                except json.JSONDecodeError:
                    st.subheader("Raw response")
                    st.text(resp.text)
                else:
                    st.subheader("JSON response")
                    st.json(data)

                    # If the response looks like tabular rows, display as table
                    if isinstance(data, dict):
                        rows = data.get("rows") or data.get("data")
                    else:
                        rows = data

                    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
                        st.subheader("Table view")
                        st.dataframe(rows)
