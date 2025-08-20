import os, smtplib, requests
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

def show_communication_dashboard():
    st.markdown("---")
    try:
        from twilio.rest import Client as TwilioClient
    except Exception:
        TwilioClient = None

    # ------------------ SEND SMS ------------------
    with st.expander("📩 Send SMS", expanded=True):
        with st.form("sms_form"):
            st.subheader("📩 Send SMS")
            twilio_sid = st.text_input("Twilio SID", type="password", value=os.getenv("TWILIO_ACCOUNT_SID",""))
            twilio_token = st.text_input("Twilio Auth Token", type="password", value=os.getenv("TWILIO_AUTH_TOKEN",""))
            twilio_number = st.text_input("Twilio Phone Number (with +country code)", value=os.getenv("TWILIO_PHONE",""))
            recipient_number = st.text_input("Recipient Phone Number (with +country code)")
            sms_body = st.text_input("Message Text", value="Hello from Python, I am PLK!")
            sms_submit = st.form_submit_button("Send SMS")
            if sms_submit:
                if not TwilioClient:
                    st.error("Twilio client not installed: pip install twilio")
                else:
                    try:
                        client = TwilioClient(twilio_sid, twilio_token)
                        message = client.messages.create(body=sms_body, from_=twilio_number, to=recipient_number)
                        st.success(f"✅ SMS sent! SID: {message.sid}")
                    except Exception as e:
                        st.error(f"❌ SMS Error: {e}")

    # ------------------ MAKE CALL ------------------
    with st.expander("📞 Make a Call", expanded=False):
        with st.form("call_form"):
            st.subheader("📞 Make a Call")
            call_sid = st.text_input("Twilio SID (Call)", type="password", value=os.getenv("TWILIO_ACCOUNT_SID",""))
            call_token = st.text_input("Twilio Auth Token (Call)", type="password", value=os.getenv("TWILIO_AUTH_TOKEN",""))
            call_from = st.text_input("Twilio Phone Number (Call)", value=os.getenv("TWILIO_PHONE",""))
            call_to = st.text_input("Recipient Phone Number (Call)")
            call_msg = st.text_area("Call Message", value="Hello! This is a Python-Twilio call. Have a great day!")
            call_submit = st.form_submit_button("Make Call")
            if call_submit:
                if not TwilioClient:
                    st.error("Twilio client not installed: pip install twilio")
                else:
                    try:
                        client = TwilioClient(call_sid, call_token)
                        twiml = f'<Response><Say>{call_msg}</Say></Response>'
                        call = client.calls.create(to=call_to, from_=call_from, twiml=twiml)
                        st.success(f"✅ Call initiated! SID: {call.sid}")
                    except Exception as e:
                        st.error(f"❌ Call Error: {e}")

    # ------------------ SEND EMAIL ------------------
    with st.expander("📧 Send Email", expanded=False):
        with st.form("email_form"):
            st.subheader("📧 Send Email")
            sender_email = st.text_input("Your Gmail Address", value=os.getenv("GMAIL_ADDRESS",""))
            app_password = st.text_input("App Password", type="password", value=os.getenv("GMAIL_APP_PASSWORD",""))
            receiver_email = st.text_input("Receiver Email")
            subject = st.text_input("Subject", value="Test Email from Python")
            plain_text = st.text_input("Plain Text Message", value="Hi, how are you?")
            html_content = st.text_area("HTML Message", value="<h2>Hello!</h2><p>This is a test email from Streamlit + Python.</p>")
            email_submit = st.form_submit_button("Send Email")

            if email_submit:
                try:
                    msg = MIMEMultipart("alternative")
                    msg["Subject"] = subject
                    msg["From"] = sender_email
                    msg["To"] = receiver_email
                    msg.attach(MIMEText(plain_text, "plain"))
                    msg.attach(MIMEText(html_content, "html"))
                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, app_password)
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                    st.success("✅ Email sent successfully!")
                except Exception as e:
                    st.error(f"❌ Email Error: {e}")

    # ------------------ INSTAGRAM POST (instagrapi) ------------------
    with st.expander("📸 Instagram Auto Post", expanded=False):
        st.warning("⚠️ Instagram automation may be against Instagram's Terms. Use responsibly.")
        with st.form("insta_form"):
            st.subheader("📸 Instagram Auto Post (instagrapi)")
            insta_user = st.text_input("Instagram Username")
            insta_pass = st.text_input("Instagram Password", type="password")
            caption = st.text_input("Caption", value="Automated post from Streamlit + Python ❤️")
            uploaded_img = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
            insta_submit = st.form_submit_button("Post to Instagram")
            if insta_submit:
                if uploaded_img is None:
                    st.warning("⚠️ Please upload an image to post.")
                else:
                    try:
                        from instagrapi import Client
                        with open("temp_insta_img.jpg", "wb") as f:
                            f.write(uploaded_img.read())
                        cl = Client()
                        cl.login(insta_user, insta_pass)
                        cl.photo_upload("temp_insta_img.jpg", caption)
                        st.success("✅ Instagram post uploaded!")
                    except Exception as e:
                        st.error(f"❌ Instagram Error: {e}")

def show_google_search():
    st.header("🔍 Google Search")
    query = st.text_input("Search Query")
    if st.button("Search"):
        try:
            # pip install googlesearch-python
            from googlesearch import search
            results = list(search(query, num_results=5))
            for url in results:
                st.write(f"🔗 {url}")
        except Exception as e:
            st.error(f"❌ Error performing search: {str(e)}")
            st.warning("Install: pip install googlesearch-python")

def show_whatsapp_instant():
    st.header("📱 Send WhatsApp Message (Instant, Send Twice)")
    number = st.text_input("Phone Number (+91...)")
    message = st.text_area("Message")
    if st.button("Send Instantly Twice"):
        try:
            import pywhatkit
            pywhatkit.sendwhatmsg_instantly(number, message, wait_time=15, tab_close=True)
            pywhatkit.sendwhatmsg_instantly(number, message, wait_time=30, tab_close=True)
            st.success("✅ Message sent twice instantly! Keep your WhatsApp Web open.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.warning("Install: pip install pywhatkit")

def show_instagram_poster():
    st.header("📸 Post on Instagram (instabot)")
    st.warning("⚠️ May violate ToS. Use at your own risk.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    caption = st.text_area("Caption")
    photo = st.file_uploader("Upload Photo", type=['jpg', 'png'])
    if st.button("Post"):
        if photo is not None:
            try:
                from instabot import Bot
                with open("temp_photo.jpg", "wb") as f:
                    f.write(photo.getbuffer())
                bot = Bot()
                bot.login(username=username, password=password)
                bot.upload_photo("temp_photo.jpg", caption=caption)
                # cleanup
                import os
                if os.path.exists("temp_photo.jpg.REMOVE_ME"): os.remove("temp_photo.jpg.REMOVE_ME")
                if os.path.exists("temp_photo.jpg"): os.remove("temp_photo.jpg")
                st.success("✅ Posted to Instagram!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.warning("Install: pip install instabot")
        else:
            st.warning("Please upload a photo first!")

def show_web_scraper():
    st.header("🌐 Website Scraper")
    url = st.text_input("Website URL")
    if st.button("Scrape"):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]): script.extract()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            st.subheader("📄 Extracted Text")
            st.text_area("Scraped Content", text, height=300)
            st.download_button("💾 Download as Text", data=text.encode('utf-8'),
                               file_name="scraped_content.txt", mime="text/plain")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def show_face_swap_tool():
    st.header("😆 Face Swap")
    st.warning("⚠️ Requires dlib + OpenCV; guide only.")
    st.code("pip install dlib opencv-python numpy")
    st.info("Download shape predictor: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")

def show_linkedin_dm():
    st.header("💼 LinkedIn DM Sender")
    st.warning("⚠️ Simulation. Use Selenium to automate in real use.")
    st.code("pip install selenium  # then add webdriver and automate login/msg flow")

def show_gmail_reader():
    st.header("📧 Gmail Reader")
    st.warning("⚠️ Needs Google Cloud Console OAuth credentials.")
    st.info("""Steps:
1) Create project + enable Gmail API
2) Create OAuth client
3) Download credentials.json into working directory
4) First run opens browser to authorize""")

def show_python_automation():
    from smartops.utils import show_page_header
    show_page_header("🐍 Python Automation")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🔍 Google Search", "📱 WhatsApp", "📸 Instagram", "🌐 Web Scraper",
        "😆 Face Swap", "💼 LinkedIn DM", "📧 Gmail", "📡 Communication Dashboard"
    ])
    with tab1: show_google_search()
    with tab2: show_whatsapp_instant()
    with tab3: show_instagram_poster()
    with tab4: show_web_scraper()
    with tab5: show_face_swap_tool()
    with tab6: show_linkedin_dm()
    with tab7: show_gmail_reader()
    with tab8: show_communication_dashboard()
