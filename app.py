import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import datetime
import json
from pathlib import Path
from uuid import uuid4

# Load the .env file
load_dotenv()

# Environment vars
GEMINI_API = os.getenv("GEMINI_API")
DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD")  # set this in .env to enable auth

# Configure the SDK only if the key exists
if GEMINI_API:
    genai.configure(api_key=GEMINI_API)

# App config
st.set_page_config(page_title="DocGenius Dashboard", layout="wide")

# Ensure uploads dir exists
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar: authentication and info
with st.sidebar:
    st.title("DocGenius")
    st.markdown("**Instructions:** Upload a PDF, select it (optional), enter a prompt, and click Ask.")
    if DASHBOARD_PASSWORD:
        pwd = st.text_input("Dashboard password", type="password")
        if st.button("Login"):
            if pwd == DASHBOARD_PASSWORD:
                st.session_state.authenticated = True
                # No explicit rerun: Streamlit re-executes the script after a button press
            else:
                st.error("Invalid password")
    else:
        st.warning("DASHBOARD_PASSWORD not set in .env — auth is disabled. Set it to enable password protection.")
        if st.button("Continue without auth"):
            st.session_state.authenticated = True
            # No explicit rerun needed here; the page will re-execute on button click
    st.write(f"Auth enabled: {'Yes' if DASHBOARD_PASSWORD else 'No'}")

    if st.session_state.authenticated:
        if st.button("Logout"):
            st.session_state.authenticated = False
            # Logout will take effect on next script run (no explicit rerun) 

# Require authentication to proceed
if not st.session_state.authenticated:
    st.info("Please log in via the sidebar to access the dashboard.")
    st.stop()

# Layout: left column for uploads and history, right column for prompt and response
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Uploads")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded in uploaded_files:
            # Save file with a uuid prefix to avoid collisions
            uid = uuid4().hex
            safe_name = f"{uid}_{uploaded.name}"
            save_path = UPLOADS_DIR / safe_name
            with open(save_path, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success(f"Saved {uploaded.name}")

    st.markdown("**Available files**")
    files = sorted(UPLOADS_DIR.iterdir(), key=os.path.getmtime, reverse=True)
    choices = [None]
    for f in files:
        # display original filename (after first underscore)
        display_name = "_".join(f.name.split("_")[1:]) if "_" in f.name else f.name
        cols = st.columns([4, 1])
        cols[0].write(display_name)
        if cols[1].button("Delete", key=f"del_{f.name}"):
            try:
                f.unlink()
                st.success(f"Deleted {display_name}")
                # Page will refresh on next interaction; no explicit rerun
            except Exception as e:
                st.error(f"Failed to delete {display_name}: {e}")
        choices.append(f.name)

    st.markdown("---")
    st.header("History & Export")
    st.write(f"Total interactions: {len(st.session_state.history)}")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"**{item['prompt']}** — *{item['timestamp']}*")
            st.write(item['response'])
            st.markdown("---")

    if st.button("Clear history"):
        st.session_state.history = []
        st.success("Conversation history cleared")

    if st.session_state.history:
        history_json = json.dumps(st.session_state.history, indent=2)
        st.download_button("Download history (JSON)", history_json, file_name="docgenius_history.json", mime="application/json")

with col2:
    st.header("Ask your PDF")
    selected = st.selectbox("Select a file (optional)", choices, format_func=lambda x: ("None" if x is None else ("_".join(x.split("_")[1:]) if x else x)))
    prompt = st.text_area("Enter your prompt:")
    if st.button("Ask"):
        if not prompt:
            st.error("Please enter a prompt before asking.")
        else:
            # Call Gemini if available
            try:
                if GEMINI_API:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    response_text = getattr(response, "text", str(response))
                else:
                    response_text = "GEMINI_API not set. This is a mock response for testing."
            except Exception as e:
                response_text = f"Error calling Gemini: {e}"

            timestamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            st.subheader("Response")
            st.write(response_text)
            st.caption(f"Generated on: {timestamp}")

            # Save to history
            st.session_state.history.append({
                "prompt": prompt,
                "response": response_text,
                "timestamp": timestamp,
                "file": (None if selected is None else selected)
            })

            # UI will reflect the new history on the next rerun triggered by user interaction