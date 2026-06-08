import streamlit as st
import requests
from backend.reminder_storage import get_reminders_for_senior, mark_taken, mark_notified
from datetime import datetime
from companion.voice_output import speak, stop_speaking
from companion.chatbot import companion_reply
from companion.voice_companion import start_voice_chat
from backend.storage import get_latest_health, get_last_7_records
from backend.email_alert import send_missed_med_alert
import os


def show_senior_dashboard():

    # 🔹 Tell AI which senior is logged in
    os.environ["CURRENT_SENIOR"] = st.session_state.username

    # ---------- PAGE STYLE ----------
    st.markdown("""
    <style>
    .main { background:#f4f8ff; }
    .card {
        background:white;
        padding:20px;
        border-radius:15px;
        margin-bottom:20px;
        box-shadow:0px 4px 10px rgba(0,0,0,0.05);
    }
    .section-title {
        color:#2c7be5;
        font-weight:bold;
        margin-bottom:10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("👴 AI Companion")

    # -------- SESSION --------
    if "listening" not in st.session_state:
        st.session_state.listening = False

    if "history" not in st.session_state:
        st.session_state.history = []

    if "to_speak" not in st.session_state:
        st.session_state.to_speak = None

    # ================= VOICE =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗣 Talk with your companion</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    if col1.button("🎤 Start Listening"):
        st.session_state.listening = True

    if col2.button("⏹ Stop"):
        st.session_state.listening = False
        stop_speaking()

    if st.session_state.listening:
        st.warning("Listening... Speak now")

        user, reply = start_voice_chat(st.session_state.history)

        if user:
            st.session_state.history.append(user)
            st.session_state.to_speak = reply
            st.success(reply)

        st.session_state.listening = False

    user_input = st.text_input("Type message")

    if st.button("Send"):
        if user_input:
            reply = companion_reply(user_input, st.session_state.history)

            st.session_state.history.append(user_input)
            st.session_state.to_speak = reply
            st.success(reply)

    if st.session_state.to_speak:
        speak(st.session_state.to_speak)
        st.session_state.to_speak = None

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= HEALTH INPUT =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🩺 Enter Health Details</div>', unsafe_allow_html=True)

    bp = st.number_input("Blood Pressure")
    sugar = st.number_input("Sugar Level")
    hr = st.number_input("Heart Rate")

    if st.button("Check My Health"):

        response = requests.post(
            "http://127.0.0.1:8000/submit-health",
            params={
                "senior": st.session_state.username,
                "bp": bp,
                "sugar": sugar,
                "hr": hr
            }
        )

        if response.status_code == 200:
            risk = response.json()["risk_level"]
        else:
            st.error("Server error. Try again.")
            return

        if risk == "High Risk":
            st.error("⚠️ High Risk Detected")
            speak("High health risk detected. Caregiver has been informed.")
        elif risk == "Warning":
            st.warning("⚠️ Warning")
        else:
            st.success("✅ Normal")

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= LATEST HEALTH =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">❤️ Latest Health Status</div>', unsafe_allow_html=True)

    bp, sugar, hr = get_latest_health(st.session_state.username)

    col1, col2, col3 = st.columns(3)

    col1.metric("Blood Pressure", bp if bp else "--")
    col2.metric("Sugar Level", sugar if sugar else "--")
    col3.metric("Heart Rate", hr if hr else "--")

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= HISTORY =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 My Health History</div>', unsafe_allow_html=True)

    data = get_last_7_records(st.session_state.username)

    if data is not None:
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No history yet")

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= MEDICATION =================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💊 My Medication</div>', unsafe_allow_html=True)

    reminders = get_reminders_for_senior(st.session_state.username)

    if not reminders.empty:

        now = datetime.now().time()

        for i, r in reminders.iterrows():

            st.write(f"💊 **{r['Medicine']}**  ⏰ {r['Start']} - {r['End']}")

            start_time = datetime.strptime(str(r["Start"]), "%H:%M:%S").time()
            end_time = datetime.strptime(str(r["End"]), "%H:%M:%S").time()

            if r["Taken"] == "No":

                # ✅ Within allowed time
                if start_time <= now <= end_time:
                    if st.button(f"Mark Taken - {r['Medicine']}", key=i):
                        mark_taken(i)
                        st.success("Marked as Taken")

                # ❌ Missed → send email ONLY ONCE
                elif now > end_time:

                    if r["Notified"] == "No":
                        st.error("⏰ Missed! Caregiver notified")

                        send_missed_med_alert(
                            st.session_state.username,
                            r["Medicine"]
                        )

                        mark_notified(i)

                # ⏳ Too early
                else:
                    st.info("⏳ Not time yet")

            else:
                st.success("Taken ✔")

    else:
        st.info("No reminders yet")

    st.markdown('</div>', unsafe_allow_html=True)