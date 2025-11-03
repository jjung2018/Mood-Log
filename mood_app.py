# ==========================================================
#  Queue Pulse Tracker ⚡
#  Built by Jiwon Jung
#  A lightweight Streamlit app to log and visualize team mood
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
import random

# Connect to Google Sheets
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    "mood-queue-477022-12a64ab5b098.json", SCOPE
)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("Mood Log").sheet1 

headers = SHEET.row_values(1)
if headers != ["timestamp", "mood", "note"]:
    SHEET.insert_row(["timestamp", "mood", "note"], 1)

# Streamlit App
st.set_page_config(page_title="Mood Tracker", page_icon="⚡", layout="centered")
st.title("Mood Tracker")
st.caption("Track how you're feeling today.")

# UI/UX Enhancements
messages = [
    "Doing great! Keep it up :)",
    "You’ve got this",
    "Take a deep breath, you’re doing amazing!",
]
st.write(random.choice(messages))
st.write("---")

# Logging Mood Input
moods = {"🎉 Energized": "Energized", "😊 Chill": "Chill", "😕 Stressed": "Stressed", "😴 Tired": "Tired", "😤 Frustrated": "Frustrated", "😄 Joyful": "Joyful","🤔 Confusing": "Confusing"}
mood_scores = {"🎉 Energized": 2, "😊 Chill": 1, "😕 Stressed": -1, "😴 Tired": -2, "😤 Frustrated": -3, "😄 Joyful": 3, "🤔 Confusing": 0}

emoji = st.selectbox("How are you feeling right now?", list(moods.keys()))
note = st.text_input("Tags or notes about your mood (optional):")

if st.button("Log Mood"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    SHEET.append_row([timestamp, emoji, note]) 
    st.success(f"Logged {emoji} {moods[emoji]} — {timestamp}")

st.write("---")

# Bar Chart Visualization
data = pd.DataFrame(SHEET.get_all_records())

if not data.empty:
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    today_df = data[data["timestamp"].dt.date == date.today()]

    if not today_df.empty:
        today_df["score"] = today_df["mood"].map(mood_scores)

        # Count moods for today
        mood_counts = today_df["mood"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]

        # Average mood score
        avg_score = today_df["score"].mean()
        st.metric("Average Mood Score (−2 to +2)", f"{avg_score:.2f}")

        # Bar chart of today's moods
        fig = px.bar(
            mood_counts,
            x="Mood",
            y="Count",
            text="Count",
            color="Mood",
            title="Today's Mood Breakdown",
            height=350,
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        # Line chart over time
        fig2 = px.line(
            today_df.sort_values("timestamp"),
            x="timestamp",
            y="score",
            title="Mood Score Over Time",
            markers=True,
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Today's entries
        with st.expander("See today’s mood entries"):
            st.dataframe(today_df[["timestamp", "mood", "note"]])

    else:
        st.info("No moods logged yet!")
else:
    st.warning("Log a mood to get started!")

# Footer
st.write("---")
st.markdown("<small>Built by Jiwon Jung © 2025</small>", unsafe_allow_html=True)
