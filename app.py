import streamlit as st

# ===================== TOP LEVEL CONFIG =====================
st.set_page_config(
    page_title="SmartOps MenuBase",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== IMPORTS =====================
from smartops.utils import initialize_app, show_page_header
from smartops.home import show_home
from smartops.social_links import show_social_links_manager
from smartops.python_automation import show_python_automation
from smartops.ai_assistant import show_ai_assistant
from smartops.machine_learning import show_machine_learning, show_titanic_survival
from smartops.computer_vision import show_computer_vision
from smartops.devops_tools import show_devops_tools
from smartops.web_js_tasks import show_web_js_tasks
from smartops.linux_command_manager import show_linux_command_manager
from smartops.project_links import show_project_links

# ===================== MAIN =====================
def main():
    # Initialize session state
    initialize_app()

    # Sidebar navigation
    with st.sidebar:
        st.title("🔧 SmartOps MenuBase")
        st.markdown("---")
        page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "🔗 Social Links",
                "🐍 Python Automation",
                "🤖 AI Assistant",
                "📊 Machine Learning",
                "🚢 Titanic Survival",
                "👁️ Computer Vision",
                "🛠️ DevOps Tools",
                "🌐 Web/JS Tasks",
                "🐧 Linux Command Manager",
                "📁 Project Links",
            ],
            key="page_selector",
        )

    # Render pages
    if page == "🏠 Home":
        show_home()
    elif page == "🔗 Social Links":
        show_social_links_manager()
    elif page == "🐍 Python Automation":
        show_python_automation()
    elif page == "🤖 AI Assistant":
        show_ai_assistant()
    elif page == "📊 Machine Learning":
        show_machine_learning()
    elif page == "🚢 Titanic Survival":
        show_titanic_survival()
    elif page == "👁️ Computer Vision":
        show_computer_vision()
    elif page == "🛠️ DevOps Tools":
        show_devops_tools()
    elif page == "🌐 Web/JS Tasks":
        show_web_js_tasks()
    elif page == "🐧 Linux Command Manager":
        show_linux_command_manager()
    elif page == "📁 Project Links":
        show_project_links()

# ===================== RUN APP =====================
if __name__ == "__main__":
    main()
