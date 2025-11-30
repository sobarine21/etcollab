import requests
import streamlit as st

FUNCTION_URL = "https://zmxnoeekcvtptybentct.supabase.co/functions/v1/external-db-query"

st.set_page_config(
    page_title="External DB Query Runner",
    page_icon="🗄️",
    layout="wide",
)

st.title("🗄️ External DB Query Runner")
st.caption("Run SQL against your external database via the Supabase Edge Function.")

# -----------------------------
# Sidebar – API key
# -----------------------------
st.sidebar.header("API Settings")

default_api_key = ""
if "EXTERNAL_DB_API_KEY" in st.secrets:
    default_api_key = st.secrets["EXTERNAL_DB_API_KEY"]

api_key = st.sidebar.text_input(
    "x-api-key",
    value=default_api_key,
    type="password",
    help="API key that the Edge Function expects in the `x-api-key` header.",
)

# -----------------------------
# Main form
# -----------------------------
st.subheader("Query Configuration")

with st.form("query_form"):
    database_id = st.text_input(
        "Database ID",
        placeholder="your-database-id",
        help="The database_id required by the function.",
    )

    query_text = st.text_area(
        "SQL Query",
        value="SELECT * FROM users LIMIT 10;",
        height=160,
        help="Write any SQL query supported by the external database.",
    )

    submitted = st.form_submit_button("▶️ Run Query")

# -----------------------------
# Call function
# -----------------------------
if submitted:
    if not api_key:
        st.error("Please provide the x-api-key in the sidebar.")
    elif not database_id.strip():
        st.error("Database ID is required.")
    elif not query_text.strip():
        st.error("Query text is required.")
    else:
        payload = {
            "database_id": database_id.strip(),
            "query_text": query_text,
        }

        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
        }

        st.write("📡 Sending request to Edge Function…")

        try:
            resp = requests.post(FUNCTION_URL, headers=headers, json=payload, timeout=60)
            st.write(f"Status code: `{resp.status_code}`")

            if not resp.ok:
                st.error("Request failed.")
                st.code(resp.text, language="json")
            else:
                # Try JSON first
                try:
                    data = resp.json()
                    st.success("Query executed successfully (JSON response).")
                    st.json(data)

                    # If looks like rows (list of dicts), show as table
                    if isinstance(data, list) and data and isinstance(data[0], dict):
                        st.subheader("Table View")
                        st.dataframe(data, use_container_width=True)
                except ValueError:
                    # Fallback to plain text (maybe CSV or raw text)
                    st.success("Query executed successfully (non-JSON response).")
                    st.code(resp.text)
        except requests.RequestException as e:
            st.error(f"Request error: {e}")
