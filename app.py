import streamlit as st
from pathlib import Path

# Import page modules from my_pages folder
from my_pages import home, live_match, top_players, sql_analytics, crud

# Sidebar navigation
st.sidebar.title("🏏 Cricbuzz LiveStats Dashboard")
page = st.sidebar.radio(
    "Select a page:",
    ["🏡 Home", "🎥 Live Match", "🥇 Top Player Stats", "📈 SQL Queries & Analytics", "📝 CRUD Operations"]
)

# Run the selected page
if page == "🏡 Home":
    home.app()
elif page == "🎥 Live Match":
    live_match.app()
elif page == "🥇 Top Player Stats":
    top_players.app()
elif page == "📈 SQL Queries & Analytics":
    sql_analytics.app()
elif page == "📝 CRUD Operations":
    crud.app()
