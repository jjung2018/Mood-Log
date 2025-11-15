import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date, timedelta
import numpy as np
import random

# ---------------------------
# Google Sheets Connection
# ---------------------------
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# 👇 Replace with your own JSON keyfile name if needed
CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    "mood-queue-477022-12a64ab5b098.json", SCOPE
)
CLIENT = gspread.authorize(CREDS)

# 👇 Change sheet name if you want, e.g. "Hackathon Revenue Log"
SHEET = CLIENT.open("Mood Log").sheet1  

EXPECTED_HEADERS = ["timestamp", "client", "revenue", "note"]
headers = SHEET.row_values(1)

if headers != EXPECTED_HEADERS:
    SHEET.insert_row(EXPECTED_HEADERS, 1)

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(
    page_title="World First Chief of Staff Hackathon – Revenue Tracker",
    page_icon="⚡",
    layout="centered",
)

st.title("⚡ Revenue & New Clients Tracker")
st.caption("Interactive demo for the World First Chief of Staff Hackathon.")

messages = [
    "How do we grow revenue 10x from here?",
    "What’s blocking the next big client?",
    "Small wins stacked daily → huge growth.",
    "Chief of Staff superpower: visibility & focus."
]
st.write(random.choice(messages))
st.write("---")

# ---------------------------
# Logging New Revenue
# ---------------------------
st.subheader("Log a New Client / Deal")

col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client name", placeholder="Acme Corp, Pilot User #3, etc.")
with col2:
    revenue_amount = st.number_input(
        "Revenue amount ($)", min_value=0.0, step=100.0, format="%.2f"
    )

note = st.text_input(
    "Notes / tags (optional)", 
    placeholder="e.g. pilot, upsell, self-serve, enterprise"
)

if st.button("Log Deal"):
    if not client_name or revenue_amount <= 0:
        st.error("Please enter a client name and a revenue amount greater than 0.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        SHEET.append_row([timestamp, client_name, revenue_amount, note])
        st.success(f"Logged ${revenue_amount:,.2f} from {client_name} at {timestamp} ✅")

st.write("---")

# ---------------------------
# Load Data from Google Sheets
# ---------------------------
data = pd.DataFrame(SHEET.get_all_records())

if data.empty:
    st.warning("No revenue logged yet. Add a deal above to get started!")
else:
    # Clean types
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    data["date"] = data["timestamp"].dt.date
    data["revenue"] = pd.to_numeric(data["revenue"], errors="coerce").fillna(0.0)

    # -----------------------
    # KPIs / Metrics
    # -----------------------
    total_revenue = data["revenue"].sum()
    unique_clients = data["client"].nunique()
    deals_count = len(data)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    with col2:
        st.metric("Unique Clients", unique_clients)
    with col3:
        avg_deal = total_revenue / deals_count if deals_count > 0 else 0
        st.metric("Avg Deal Size", f"${avg_deal:,.0f}")

    st.write("---")

    # -----------------------
    # Revenue Over Time
    # -----------------------
    st.subheader("Revenue Over Time")

    daily_revenue = (
        data.groupby("date")["revenue"]
        .sum()
        .reset_index()
        .sort_values("date")
    )
    daily_revenue["cumulative_revenue"] = daily_revenue["revenue"].cumsum()

    # Line chart: daily revenue
    fig_daily = px.line(
        daily_revenue,
        x="date",
        y="revenue",
        markers=True,
        title="Daily Revenue",
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    # Line chart: cumulative revenue
    fig_cum = px.line(
        daily_revenue,
        x="date",
        y="cumulative_revenue",
        markers=True,
        title="Cumulative Revenue",
    )
    st.plotly_chart(fig_cum, use_container_width=True)

    # -----------------------
    # Simple Revenue Forecast
    # -----------------------
    st.subheader("Simple 7-Day Revenue Forecast")

    if len(daily_revenue) >= 3:
        # fit a simple linear trend on daily revenue
        daily_revenue = daily_revenue.reset_index(drop=True)
        daily_revenue["t"] = np.arange(len(daily_revenue))  # time index 0...N-1

        # linear regression: revenue ~ t
        x = daily_revenue["t"].values
        y = daily_revenue["revenue"].values
        slope, intercept = np.polyfit(x, y, 1)

        # predict next 7 days
        last_date = daily_revenue["date"].iloc[-1]
        future_t = np.arange(len(daily_revenue), len(daily_revenue) + 7)
        future_dates = [last_date + timedelta(days=int(i + 1)) for i in range(7)]
        future_revenue = intercept + slope * future_t
        future_revenue = np.maximum(future_revenue, 0)  # no negative predictions

        forecast_df = pd.DataFrame({
            "date": list(daily_revenue["date"]) + future_dates,
            "revenue": list(daily_revenue["revenue"]) + list(future_revenue),
            "type": ["Actual"] * len(daily_revenue) + ["Forecast"] * len(future_dates),
        })

        fig_forecast = px.line(
            forecast_df,
            x="date",
            y="revenue",
            color="type",
            markers=True,
            title="Actual vs Forecasted Daily Revenue",
        )
        st.plotly_chart(fig_forecast, use_container_width=True)

        st.caption(
            "Forecast uses a simple linear trend on past daily revenue — not a fancy model, "
            "but great for storytelling in a hackathon."
        )
    else:
        st.info("Add at least 3 days of revenue data to show a forecast.")

    # -----------------------
    # Recent Deals Table
    # -----------------------
    st.subheader("Recent Deals")
    recent = data.sort_values("timestamp", ascending=False).head(20)
    st.dataframe(recent[["timestamp", "client", "revenue", "note"]])

# ---------------------------
# Footer
# ---------------------------
st.write("---")
st.markdown(
    "<small>Built by Jiwon Jung © 2025 · Demo only – not financial advice </small>",
    unsafe_allow_html=True,
)
