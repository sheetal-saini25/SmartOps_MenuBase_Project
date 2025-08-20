import streamlit as st

# Availability flags
def _check(pkg):
    try:
        __import__(pkg)
        return True
    except Exception:
        return False

CV2_AVAILABLE = _check("cv2")
MEDIAPIPE_AVAILABLE = _check("mediapipe")
WEBRTC_AVAILABLE = _check("streamlit_webrtc")
SKLEARN_AVAILABLE = _check("sklearn")
MATPLOTLIB_AVAILABLE = _check("matplotlib") and _check("seaborn")
DOCKER_AVAILABLE = _check("docker")
TF_AVAILABLE = _check("tensorflow")

def initialize_app():
    """
    Initialize app-wide settings.
    IMPORTANT: Do NOT call st.set_page_config() here!
    """
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        # You can initialize other session state variables here

def show_page_header(title, subtitle=None):
    col1, _ = st.columns([1, 3])
    with col1:
        st.title(title)
        if subtitle:
            st.caption(subtitle)
