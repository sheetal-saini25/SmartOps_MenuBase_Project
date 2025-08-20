# smartops/project_links.py
import streamlit as st

def show_project_links():
    st.title("📂 Project Links")
    st.write("Choose a project to explore:")

    links = {
        "Dream Analyzer": "http://localhost:8501/dream_analyzer",
        "AI Assistant": "http://localhost:8501/ai_assistant",
        "Linux Runner": "http://localhost:8501/linux_runner",
        "Docker Runner": "http://localhost:8501/docker_runner"
    }

    for name, url in links.items():
        st.markdown(f"[{name}]({url})")
