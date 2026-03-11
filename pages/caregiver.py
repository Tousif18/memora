import streamlit as st
from database import get_memories, get_reminders, get_moods
from streamlit_autorefresh import st_autorefresh
from database import get_emergency
import pandas as pd

st_autorefresh(interval=3000, key="caregiver_refresh")

st.title("Caregiver Dashboard")

st.subheader("Emergency Alerts")

alerts = get_emergency()

if alerts:
    latest_alert = alerts[-1][1]
    st.error(f"🚨 {latest_alert}")
else:
    st.success("No emergency alerts")
    
# Memories
st.subheader("Recent Memories")
memories = get_memories()

for memory in memories:
    st.info(memory[1])

st.divider()
# Reminders
st.subheader("Active Reminders")
reminders = get_reminders()

for reminder in reminders:
    st.warning(f"{reminder[1]} at {reminder[2]}")

st.divider()
# Mood History
st.subheader("Mood Trend Analysis")

moods = get_moods()

if moods:
    mood_map = {
        "😊 Happy": 3,
        "😐 Neutral": 2,
        "😔 Sad": 1
    }

    mood_values = [mood_map[m[1]] for m in moods]

    st.metric("Latest Mood", moods[-1][1])

    df = pd.DataFrame(mood_values, columns=["Mood Score"])

    st.line_chart(df)

    st.caption("Mood Score: 3 = Happy, 2 = Neutral, 1 = Sad")

    for mood in moods:
        st.success(mood[1])

    if mood_values[-1] == 1:
        st.error("Attention: Latest mood indicates sadness")
        
st.subheader("Emergency Alerts")
st.error("No current emergency alerts")
