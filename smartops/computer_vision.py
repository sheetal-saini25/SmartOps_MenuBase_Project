import time, threading, subprocess, platform
import streamlit as st
from streamlit_webrtc import VideoTransformerBase
from smartops.utils import show_page_header, CV2_AVAILABLE, MEDIAPIPE_AVAILABLE, WEBRTC_AVAILABLE
if CV2_AVAILABLE:
    import cv2
if MEDIAPIPE_AVAILABLE:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
if WEBRTC_AVAILABLE:
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
    import av

class HandGestureTransformer(VideoTransformerBase):
    def __init__(self):
        self.last_finger_count = -1
        self.last_action_time = time.time()
        self.hands = None
        if MEDIAPIPE_AVAILABLE:
            try:
                self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                                            min_detection_confidence=0.7, min_tracking_confidence=0.5)
            except Exception as e:
                print(f"Error initializing MediaPipe Hands: {str(e)}")
                self.hands = None

    def detect_fingers(self, hand_landmarks, hand_label):
        if not hand_landmarks or not hasattr(hand_landmarks, 'landmark'):
            return 0
        tips_ids = [4,8,12,16,20]
        fingers = []
        # Thumb
        if hand_label == "Right":
            fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0]-1].x else 0)
        else:
            fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x > hand_landmarks.landmark[tips_ids[0]-1].x else 0)
        # Other fingers
        for i in range(1,5):
            fingers.append(1 if hand_landmarks.landmark[tips_ids[i]].y < hand_landmarks.landmark[tips_ids[i]-2].y else 0)
        return sum(fingers)

    def execute_action(self, finger_count):
        try:
            actions_win = {1:"notepad", 2:"calc", 4:"mspaint"}
            if platform.system() == "Windows":
                if finger_count in actions_win:
                    subprocess.Popen(actions_win[finger_count], shell=True)
                elif finger_count == 5:
                    print("Five fingers detected - exit message")
            else:
                # Non-Windows: just print (GUI apps differ)
                print(f"Finger action: {finger_count}")
        except Exception as e:
            print(f"Error executing action: {str(e)}")

    def recv(self, frame):
        if not (MEDIAPIPE_AVAILABLE and self.hands and CV2_AVAILABLE):
            return frame
        try:
            img = frame.to_ndarray(format="bgr24")
            img = cv2.flip(img, 1)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)
            if results.multi_hand_landmarks and results.multi_handedness:
                for hl, handed in zip(results.multi_hand_landmarks, results.multi_handedness):
                    mp_drawing.draw_landmarks(img, hl, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing_styles.get_default_hand_landmarks_style(),
                                              mp_drawing_styles.get_default_hand_connections_style())
                    label = handed.classification[0].label
                    count = self.detect_fingers(hl, label)
                    cv2.putText(img, f"Fingers: {count}", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                    t = time.time()
                    if (count != self.last_finger_count) and (t - self.last_action_time) > 1.5:
                        self.last_finger_count = count
                        self.last_action_time = t
                        threading.Thread(target=self.execute_action, args=(count,), daemon=True).start()
            return av.VideoFrame.from_ndarray(img, format="bgr24")
        except Exception as e:
            print(f"Error in hand gesture recognition: {str(e)}")
            return frame

def show_computer_vision():
    show_page_header("👁️ Computer Vision")

    if not CV2_AVAILABLE:
        st.error("⚠️ OpenCV (cv2) required: pip install opencv-python")
        return
    if not MEDIAPIPE_AVAILABLE:
        st.error("⚠️ MediaPipe required: pip install mediapipe")
        return
    if not WEBRTC_AVAILABLE:
        st.error("⚠️ streamlit-webrtc required: pip install streamlit-webrtc")
        return

    st.markdown("""
    ## Hand Gesture Recognition

    Use your hand gestures to control applications:
    - 👆 1 finger: Open Notepad (Windows)
    - ✌️ 2 fingers: Open Calculator (Windows)
    - 🤟 3 fingers: (reserved)
    - ✋ 4 fingers: Open Paint (Windows)
    - 🖐️ 5 fingers: Show exit message
    """)

    st.warning("⚠️ Camera access is required. Video is processed locally; not stored/transmitted.")

    try:
        webrtc_ctx = webrtc_streamer(
            key="hand-gesture",
            video_transformer_factory=HandGestureTransformer,
            rtc_configuration=RTCConfiguration({"iceServers":[{"urls":["stun:stun.l.google.com:19302"]}]}),
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
        if not webrtc_ctx.state.playing:
            st.info("Waiting for camera access...")
    except Exception as e:
        st.error(f"❌ Error initializing video stream: {str(e)}")
        st.warning("Ensure no other app is using the camera and permissions are granted.")
