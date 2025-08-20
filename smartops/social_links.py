import streamlit as st
import os
import json
from smartops.utils import show_page_header

DATA_FILE = "linkedin_links.json"

def load_links():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_links(links):
    with open(DATA_FILE, "w") as f:
        json.dump(links, f, indent=2)

def show_social_links_manager():
    show_page_header("🔗 Social Links")
    st.info("Add your LinkedIn profiles with custom names. (Multiple links can be saved)")

    if "linkedin_links" not in st.session_state:
        st.session_state.linkedin_links = load_links()

    # Input fields
    link_name = st.text_input("Profile Name (e.g., Work LinkedIn, Personal LinkedIn)")
    linkedin = st.text_input("LinkedIn URL")

    # Save button
    if st.button("💾 Save"):
        if link_name and linkedin:
            st.session_state.linkedin_links.append({"name": link_name, "url": linkedin})
            save_links(st.session_state.linkedin_links)
            st.success(f"Saved: {link_name}")
        else:
            st.warning("Please enter both name and LinkedIn URL")

    # Preview clickable links with delete option
    if st.session_state.linkedin_links:
        st.subheader("Saved LinkedIn Profiles")
        for i, link in enumerate(st.session_state.linkedin_links):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"- [{link['name']}]({link['url']})", unsafe_allow_html=True)
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    st.session_state.linkedin_links.pop(i)
                    save_links(st.session_state.linkedin_links)
                    st.experimental_rerun()  # refresh the page to update
