import streamlit as st
from smartops.utils import show_page_header

def show_home():
    """Display the home page with an overview of the application."""
    show_page_header("🏠 Welcome to SmartOps MenuBase")

    st.markdown("""
    ### 🚀 Your one-stop dashboard for automation, AI, and DevOps tools

    SmartOps MenuBase is a powerful platform that brings together various automation, 
    artificial intelligence, and development operations tools in one place.
    """)

    st.markdown("## ✨ Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🤖 AI Assistant")
        st.markdown("""
        - Chat with AI models
        - Get coding help
        - Generate content
        - Answer questions
        """)

    with col2:
        st.markdown("### ⚙️ Automation")
        st.markdown("""
        - Web scraping
        - File operations
        - Social media automation
        - Scheduled tasks
        """)

    with col3:
        st.markdown("### 🛠️ DevOps")
        st.markdown("""
        - Docker management
        - SSH command execution
        - Server monitoring
        - Cloud operations
        """)

    st.markdown("## 🚀 Quick Start")
    st.markdown("""
    1. **Navigate** using the sidebar menu to access different tools
    2. **Configure** the required settings for each tool
    3. **Execute** your tasks with a single click
    4. **View** results and download outputs as needed
    """)

    st.markdown("## 📊 System Status")
    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1: st.metric("AI Services", "🟢 Online")
    with status_col2: st.metric("Automation Tools", "🟢 Online")
    with status_col3: st.metric("System Resources", "⚡ Optimal")

    with st.expander("📋 Recent Activity"):
        st.markdown("""
        - 🔵 Connected to AI services
        - 🔄 Updated automation scripts
        - 📊 Generated system report
        - 🔒 Security check completed
        """)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <p>SmartOps MenuBase v1.0.0 | Made with ❤️ for automation enthusiasts</p>
        <p>Need help? Check out the documentation or contact support.</p>
    </div>
    """, unsafe_allow_html=True)
