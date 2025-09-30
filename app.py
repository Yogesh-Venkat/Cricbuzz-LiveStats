import streamlit as st
import importlib
import sys, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(r"C:\Users\yoges\OneDrive\Desktop\Guvi\Cricbuzz-LiveStats\cricbuzz_api_key.env")

# Ensure project root is in sys.path
sys.path.append(os.path.dirname(__file__))

# Import utils
from utils.fetch_live import fetch_live_matches, fetch_scorecard

# ✅ Only ONE set_page_config call
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    layout="centered",
    initial_sidebar_state="expanded"
)




# Sidebar navigation
st.sidebar.title("🏏 Cricbuzz LiveStats Dashboard")
my_pages = {
    "🏡 Home": "home",
    "🎥 Live Match": "live_match",
    "🥇 Top Player Stats": "top_players",
    "📈 SQL Queries & Analytics": "sql_analytics",
    "📝 CRUD Operations": "crud"
}

selected_page = st.sidebar.radio("Select a page:", list(my_pages.keys()))

# Import and run selected page
try:
    page_module = importlib.import_module(f"my_pages.{my_pages[selected_page]}")
    page_module.app()
except ModuleNotFoundError as e:
    st.error(f"⚠️ Module not found: {e}")
except AttributeError as e:
    st.error(f"⚠️ Page is missing app() function: {e}")
except Exception as e:
    st.error(f"⚠️ Error loading page: {e}")
