# smartops/ai_assistant.py
import os
import streamlit as st
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# =================== Load Gemini API Key ===================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found in .env. Add GEMINI_API_KEY=your_key and restart app.")
    st.stop()

import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

# Try initializing model
try:
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Failed to initialize Gemini model: {e}")
    st.stop()

# =================== Agriculture Data Scraping ===================
try:
    url = "https://agmarknet.gov.in/"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    agriculture_data = soup.get_text()[:5000]  # limit to 5000 chars
except Exception:
    agriculture_data = ""

# =================== Main Function ===================
def show_ai_assistant():
    st.title("🤖 AI Assistant Suite")
    st.markdown("This app contains three sections: **General AI Chat**, **Dream Analyzer**, and **Agriculture Assistant**.")

    tab1, tab2, tab3 = st.tabs(["💬 AI Chat", "💤 Dream Analyzer", "🌾 Agriculture Assistant"])

    # =================== Tab 1: AI Chat ===================
    with tab1:
        st.subheader("General AI Chat")
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your AI assistant powered by Gemini."}
            ]

        # Display messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        if prompt := st.chat_input("Ask me anything..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                placeholder = st.empty()
                try:
                    resp = model.generate_content(prompt)
                    text = getattr(resp, "text", "No response generated")
                    placeholder.markdown(text)
                except Exception as e:
                    placeholder.markdown("Error occurred")
                    st.error(e)
                st.session_state.messages.append({"role": "assistant", "content": text})

        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your AI assistant powered by Gemini."}
            ]

    # =================== Tab 2: Dream Analyzer ===================
    with tab2:
        st.subheader("Dream Analyzer + Sleep Tips")
        dream = st.text_area("Describe your dream:", height=150)
        if st.button("🔍 Analyze Dream"):
            if dream.strip():
                try:
                    dream_resp = model.generate_content(
                        f"I had this dream: {dream}. Please interpret it psychologically using symbols, emotions, and subconscious patterns."
                    )
                    st.markdown("### 🔮 Interpretation")
                    st.write(dream_resp.text)

                    tips_resp = model.generate_content(
                        "Suggest 5 short tips for better sleep and peaceful dreams."
                    )
                    st.markdown("### 💤 Sweet Sleep Tips")
                    st.markdown(tips_resp.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter a dream to analyze.")

    # =================== Tab 3: Agriculture Assistant ===================
    with tab3:
        st.subheader("AI Agriculture Assistant")
        st.write("Ask anything related to agriculture, mandi prices, crops, government schemes, etc.")

        userprompt = st.text_input("Enter your agriculture-related question:")
        if userprompt:
            prompt = f"""
You are an expert AI assistant in Indian agriculture and agri-marketing.
Help farmers, students, and policymakers with accurate answers.

Use the following scraped website data if relevant:
{agriculture_data}

User question: {userprompt}

Provide a clear and helpful answer.
"""
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🤖 Answer")
                st.write(response.text)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
