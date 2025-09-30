import streamlit as st
import re
import math
import pandas as pd
from datetime import datetime

from dotenv import load_dotenv
from pathlib import Path
import os
env_path = r"C:\Users\yoges\OneDrive\Desktop\Guvi\Cricbuzz-LiveStats\.env"
load_dotenv(dotenv_path=env_path)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_AUTH_PLUGIN = os.getenv("DB_AUTH_PLUGIN")
import mysql.connector 
def app():
    st.title("🥇 Top Player Stats")
    st.write("Show top player statistics here.")
    st.title("👤 Cricket Player Profile & Performance")

    # 📂 Folder where your pickle files are stored
    # --- Player Search Box ---
    search_name = st.text_input("🔍 Search for a player by name:")

    if search_name:
        # --- DB CONNECTION ---
        def get_connection():
            return mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                auth_plugin=DB_AUTH_PLUGIN
            )

        def load_player_data():
            conn = get_connection()
            players_info = pd.read_sql("SELECT * FROM players_get_info", conn)
            players_bowling = pd.read_sql("SELECT * FROM players_bowling", conn)
            players_batting = pd.read_sql("SELECT * FROM players_batting", conn)
            conn.close()
            return players_info, players_bowling, players_batting

        players_info, players_bowling, players_batting = load_player_data()

        # Filter players by name
        filtered_players = players_info[players_info['name'].str.contains(search_name, case=False, na=False)]
        if filtered_players.empty:
            st.info("🔔 No players match that name. Try again!")
        else:
            player_selected = st.selectbox("🎯 Choose a player", filtered_players['name'].tolist())
            if player_selected:
                player_data = filtered_players[filtered_players['name'] == player_selected].iloc[0]

                # --- Helper function to handle NaN ---
                def display_value(val):
                    if val is None or (isinstance(val, float) and math.isnan(val)):
                        return " - "
                    return val

                st.subheader(f"**{display_value(player_data['name'])} — Profile Overview**")
                st.markdown(f"**Nickname:** {display_value(player_data.get('nickname'))}")

                # --- Tabs for profile & stats ---
                tab1, tab2, tab3 = st.tabs(["**🧾 Profile**", "**🏏 Batting**", "**⚾ Bowling**"])

                # --- Player Profile ---
                with tab1:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Player ID:** {display_value(player_data.get('player_id'))}")
                        st.markdown(f"**Role:** {display_value(player_data.get('role'))}")
                        st.markdown(f"**Batting Style:** {display_value(player_data.get('bat'))}")
                        st.markdown(f"**Bowling Style:** {display_value(player_data.get('bowl'))}")
                        st.markdown(f"**International Team:** {display_value(player_data.get('intlTeam'))}")
                    with col2:
                        st.markdown(f"**Date of Birth:** {display_value(player_data.get('DoB'))}")
                        st.markdown(f"**Birth Place:** {display_value(player_data.get('birthPlace'))}")
                    with col3:
                        st.markdown(f"**Test Batting Rank:** {display_value(player_data.get('bat_testRank'))}")
                        st.markdown(f"**ODI Batting Rank:** {display_value(player_data.get('bat_odiRank'))}")
                        st.markdown(f"**T20 Batting Rank:** {display_value(player_data.get('bat_t20Rank'))}")

                    st.markdown(f"**Teams:** {display_value(player_data.get('Teams'))}")

                    # --- Display Bio ---
                    bio_html = player_data.get('bio', '-')
                    if bio_html is None or bio_html.strip() == "":
                        bio_text = "-"
                    else:
                        bio_text = re.sub('<[^<]+?>', '', bio_html)
                        bio_text = bio_text.replace('&nbsp;', ' ').replace('&amp;', '&').strip()

                    st.subheader("📝 **Player Bio**")
                    st.text_area("", bio_text, height=400)
                    web_url = display_value(player_data.get('webURL'))
                    st.markdown(f"[🔗 **Read More**]({web_url})")

                # --- Batting Stats ---
                with tab2:
                    st.subheader("🏏 **Batting Performance**")
                    batting_stats = players_batting[
                        players_batting['player_id'] == player_data['player_id']
                    ].fillna('-')

                    if not batting_stats.empty:
                        stats_dict = batting_stats.iloc[0].to_dict()
                        formats = {
                            "Test": ["matches_test", "innings_test", "runs_test", "balls_test", "highest_test", "average_test", "sr_test", "not_out_test", "fours_test", "sixes_test", "ducks_test", "50s_test", "100s_test"],
                            "ODI": ["matches_odi", "innings_odi", "runs_odi", "balls_odi", "highest_odi", "average_odi", "sr_odi", "not_out_odi", "fours_odi", "sixes_odi", "ducks_odi", "50s_odi", "100s_odi"],
                            "T20": ["matches_t20", "innings_t20", "runs_t20", "balls_t20", "highest_t20", "average_t20", "sr_t20", "not_out_t20", "fours_t20", "sixes_t20", "ducks_t20", "50s_t20", "100s_t20"],
                            "IPL": ["matches_ipl", "innings_ipl", "runs_ipl", "balls_ipl", "highest_ipl", "average_ipl", "sr_ipl", "not_out_ipl", "fours_ipl", "sixes_ipl", "ducks_ipl", "50s_ipl", "100s_ipl"],
                        }
                        label_map = {
                            "matches": "Matches", "innings": "Innings", "runs": "Runs",
                            "balls": "Balls Faced", "highest": "Highest Score",
                            "average": "Batting Avg", "sr": "Strike Rate", "not_out": "Not Outs",
                            "fours": "Fours", "sixes": "Sixes", "ducks": "Ducks",
                            "50s": "50s", "100s": "100s",
                        }
                        for fmt, stats in formats.items():
                            with st.expander(f"📊 **{fmt} Format**", expanded=False):
                                for i in range(0, len(stats), 3):
                                    cols = st.columns(3)
                                    for j, col in enumerate(cols):
                                        if i + j < len(stats):
                                            key = stats[i + j]
                                            value = stats_dict.get(key, "-")
                                            base = key.replace(f"_{fmt.lower()}", "")
                                            label = label_map.get(base, key)
                                            if isinstance(value, (int, float)):
                                                if "average" in key or "sr" in key:
                                                    value = f"{value:.2f}"
                                                else:
                                                    value = int(value)
                                            col.metric(label, value)
                    else:
                        st.info("ℹ️ **Batting data not available for this player.**")

                # --- Bowling Stats ---
                with tab3:
                    st.subheader("⚾ **Bowling Performance**")
                    bowling_stats = players_bowling[
                        players_bowling['player_id'] == player_data['player_id']
                    ].fillna('-')

                    if not bowling_stats.empty:
                        stats_dict = bowling_stats.iloc[0].to_dict()
                        formats = {
                            "Test": ["matches_test", "innings_test", "balls_test", "runs_test", "maidens_test", "wickets_test", "avg_test", "eco_test", "sr_test", "bbi_test", "bbm_test", "4w_test", "5w_test", "10w_test"],
                            "ODI": ["matches_odi", "innings_odi", "balls_odi", "runs_odi", "maidens_odi", "wickets_odi", "avg_odi", "eco_odi", "sr_odi", "bbi_odi", "bbm_odi", "4w_odi", "5w_odi", "10w_odi"],
                            "T20": ["matches_t20", "innings_t20", "balls_t20", "runs_t20", "maidens_t20", "wickets_t20", "avg_t20", "eco_t20", "sr_t20", "bbi_t20", "bbm_t20", "4w_t20", "5w_t20", "10w_t20"],
                            "IPL": ["matches_ipl", "innings_ipl", "balls_ipl", "runs_ipl", "maidens_ipl", "wickets_ipl", "avg_ipl", "eco_ipl", "sr_ipl", "bbi_ipl", "bbm_ipl", "4w_ipl", "5w_ipl", "10w_ipl"],
                        }
                        label_map = {
                            "matches": "Matches", "innings": "Innings", "balls": "Balls Bowled",
                            "runs": "Runs Conceded", "maidens": "Maidens", "wickets": "Wickets",
                            "avg": "Bowling Avg", "eco": "Economy Rate", "sr": "Strike Rate",
                            "bbi": "Best Bowling Innings", "bbm": "Best Bowling Match",
                            "4w": "4 Wickets", "5w": "5 Wickets", "10w": "10 Wickets",
                        }
                        for fmt, stats in formats.items():
                            with st.expander(f"🎯 **{fmt} Format**", expanded=False):
                                for i in range(0, len(stats), 3):
                                    cols = st.columns(3)
                                    for j, col in enumerate(cols):
                                        if i + j < len(stats):
                                            key = stats[i + j]
                                            value = stats_dict.get(key, "-")
                                            base = key.replace(f"_{fmt.lower()}", "")
                                            label = label_map.get(base, key)
                                            if isinstance(value, (int, float)):
                                                if "avg" in key or "eco" in key or "sr" in key:
                                                    value = f"{value:.2f}"
                                                else:
                                                    value = int(value)
                                            col.metric(label, value)
                    else:
                        st.info("ℹ️ **Bowling data not available for this player.**")

    st.markdown("---")
    st.write("📈 **Top batting & bowling stats will be displayed here (from Cricbuzz API).**")