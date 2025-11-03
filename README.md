# Mood Logging Application

This is a quick  tool I built to help clients log how they're feeling throughout their days, and show the daily mood with visualization.

Each time a client logs how they are feeling (happy, frustrated, confused, excited, etc) the app records it with a timestamp in a shared Google Sheet and instantly updates a visualization.  


## What it does
- Lets users select a mood emoji and add an optional note.  
- Automatically logs each entry (timestamp, mood, note) to a Google Sheet.  
- Displays live bar and line charts showing mood trends for the day.  
- Calculates an average mood score to see how the client’s energy shifts.

## Built with
App Framework - [Streamlit](https://streamlit.io) 

Visualization - [Plotly Express](https://plotly.com/python/plotly-express/) 

Data Storage - Google Sheets

Language - Python 3.9 

## Live Demo
You can try the deployed version here:  
[Mood Logging App] - https://mood-log-duuvhpoq4e4xpa7jcsgdvn.streamlit.app/

The app uses a private Google Sheet as its backing data store.

