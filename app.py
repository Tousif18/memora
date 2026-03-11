import pyttsx3
from datetime import datetime, timedelta
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from pydub import AudioSegment
import io
import tempfile
from database import save_memory, get_memories, save_reminder, get_reminders, save_mood, get_moods
import streamlit as st
import requests
from database import save_emergency

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def speech_to_text(audio_bytes):
    recognizer = sr.Recognizer()

    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")

    temp_wav = "temp_audio.wav"
    audio_segment.export(temp_wav, format="wav")

    with sr.AudioFile(temp_wav) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return ""

st.set_page_config(page_title="Memora", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center;'>Memora</h1>
    <h4 style='text-align: center; color: gray;'>
    AI Memory & Wellness Companion for Elderly Care
    </h4>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):
    st.subheader("AI Companion")

    user = st.text_input("💬 Talk to Memora", key="chat_input")

    if st.button("Send", key="chat_button"):
        r = requests.get(f"http://127.0.0.1:8000/chat?q={user}")
        st.info(r.json()["response"])

st.divider()


with st.container(border=True):
    st.subheader("Memory Diary")

    note = st.text_area("Write today's memory", key="memory_text")

    audio = mic_recorder(start_prompt="🎤 Record Memory", stop_prompt="Stop Recording")

    if audio:
        spoken_text = speech_to_text(audio["bytes"])

        if spoken_text:
            st.success(f"Recognized: {spoken_text}")
            note = spoken_text

    if st.button("Save Memory", key="memory_button"):
        save_memory(note)
        st.success("Memory saved successfully")

    memories = get_memories()

    for memory in memories:
        st.info(f"📝 {memory[1]}")

st.divider()

with st.container(border=True):
    st.subheader("Reminder System")

    task = st.text_input("Reminder Task", key="task_input")

    audio_reminder = mic_recorder(
        start_prompt="🎤 Record Reminder",
        stop_prompt="Stop Recording",
        key="reminder_mic"
    )

    if audio_reminder:
        spoken_task = speech_to_text(audio_reminder["bytes"])

        if spoken_task:
            st.success(f"Recognized: {spoken_task}")
            task = spoken_task

    default_time = datetime.now() + timedelta(minutes=1)

    reminder_time = st.time_input(
        "Reminder Time",
        value=default_time.time(),
        key="time_input"
    )

    if st.button("Save Reminder", key="reminder_button"):
        save_reminder(task, reminder_time.strftime("%H:%M"))
        st.success("Reminder saved successfully")

    st.subheader("Saved Reminders")

    reminders = get_reminders()

    current_time = datetime.now().strftime("%H:%M")

    for reminder in reminders:
        st.info(f"⏰ {reminder[1]} at {reminder[2]}")

        saved_time = reminder[2]

        if saved_time == current_time:
            st.warning(f"Reminder: {reminder[1]}")
            speak(f"Reminder. {reminder[1]}")

st.divider()


with st.container(border=True):
    st.subheader("Mood Tracker")

    mood = st.selectbox(
        "How are you feeling today?",
        ["😊 Happy", "😐 Neutral", "😔 Sad"],
        key="mood_select"
    )

    if st.button("Save Mood", key="mood_button"):
        save_mood(mood)
        st.success("Mood saved successfully")

    st.subheader("Mood History")

    moods = get_moods()

    for m in moods:
        st.info(m[1])

    if mood == "😔 Sad":
        st.warning("Memora says: I'm here with you today. Would you like to talk?")

st.divider()


with st.container(border=True):
    st.subheader("Daily Summary")

    if st.button("Generate Daily Summary", key="summary_button"):
        memories = get_memories()
        moods = get_moods()
        reminders = get_reminders()

        latest_memory = memories[-1][1] if memories else "No memory recorded"
        latest_mood = moods[-1][1] if moods else "No mood recorded"
        latest_reminder = reminders[-1][1] if reminders else "No reminder saved"

        st.success(
            f"Today you felt {latest_mood}, remembered '{latest_memory}', and your next task is '{latest_reminder}'."
        )

st.divider()

with st.container(border=True):
    st.subheader("Emergency SOS")

    if st.button("🚨 SOS Emergency", key="sos_button"):
        current_alert_time = datetime.now().strftime("%H:%M:%S")

        alert_message = f"Emergency triggered at {current_alert_time}"

        save_emergency(alert_message)

        st.error(f"Emergency Alert Sent to Caregiver at {current_alert_time}")
        speak("Emergency alert sent. Caregiver has been notified.")

st.divider()