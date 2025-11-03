# ⚡ Mood of the Queue

Hi! I’m **Jiwon Jung** 👋  
This is a quick internal tool I built to help the Operations team capture the *vibe* of the patient support queue throughout the day.

Each time an agent logs how the queue “feels” — happy, frustrated, confused, or excited — the app records it with a timestamp in a shared Google Sheet and instantly updates a visualization.  
It’s the kind of small, practical project you’d spin up on a Friday to make the team’s day a little smoother.

---

## 🧠 What it does
- Lets users **select a mood emoji** and add an optional note.  
- Automatically **logs each entry** (timestamp, mood, note) to a Google Sheet.  
- Displays **live bar and line charts** showing mood trends for the day.  
- Calculates an **average mood score** to see how the team’s energy shifts.

---

## 🧱 Built with
| Purpose | Tool |
|----------|------|
| App Framework | [Streamlit](https://streamlit.io) |
| Visualization | [Plotly Express](https://plotly.com/python/plotly-express/) |
| Data Storage | Google Sheets (via `gspread` + `oauth2client`) |
| Language | Python 3.9 |

---

## 🚀 Live Demo
You can try the deployed version here:  
👉 **[Mood of the Queue App](https://jjung2018-mood-log.streamlit.app)**  

The app uses a private Google Sheet as its backing data store.

---

## 💻 Run it locally
If you want to test the app yourself:

1. **Clone this repo**
   ```bash
   git clone https://github.com/jjung2018/Mood-Log.git
   cd Mood-Log
