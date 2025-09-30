import streamlit as st
import os
import pandas as pd

def app():


    Data_dir = r"c:\Users\yoges\OneDrive\Desktop\Guvi\Cricbuzz-LiveStats\Data"

    # ✅ SQL Questions list
    qns = [
        "QN 1: All players representing India with full name, playing role, batting style, and bowling style.",
        "QN 2: Cricket matches played in the last few days with match description, both team names, venue name with city, and match date. Sorted by most recent first.",
        "QN 3: Top 10 highest run scorers in ODI cricket with player name, total runs, batting average, and number of centuries. Ordered by highest run scorer first.",
        "QN 4: Cricket venues with seating capacity greater than 30,000, showing venue name, city, country, and capacity. Ordered by largest capacity first.",
        "QN 5: Total number of matches won by each team, showing team name and number of wins. Ordered by most wins first.",
        "QN 6: Count of players in each playing role (Batsman, Bowler, All-rounder, Wicket-keeper), showing role and player count.",
        "QN 7: Highest individual batting score in each cricket format (Test, ODI, T20I) with format and highest score.",
        "QN 8: Cricket series started in 2024 with series name, host country, match type, start date, and total number of matches planned.",
        "QN 9: All-rounder players with more than 1000 runs and 50 wickets, showing player name, total runs, total wickets, and most played format.",
        "QN 10: Last 20 completed matches with match description, both team names, winning team, victory margin, victory type (runs/wickets), and venue name. Sorted by most recent first.",
        "QN 11: Players’ performance comparison across different formats for those who played at least 2 formats, showing total runs in Test, ODI, T20I, and overall batting average.",
        "QN 12: International teams’ performance at home vs away with count of wins for each team in home and away matches.",
        "QN 13: Batting partnerships where two consecutive batsmen scored 100+ runs in the same innings, showing both player names, combined runs, and innings number.",
        "QN 14: Bowling performance at different venues for bowlers with ≥3 matches at the same venue and ≥4 overs per match, showing average economy rate, total wickets, and matches played.",
        "QN 15: Players performing well in close matches (<50 runs or <5 wickets), showing average runs, total close matches played, and matches won when batting.",
        "QN 16: Players’ batting performance over years since 2020, showing average runs per match and average strike rate per year for players with ≥5 matches per year.",
        "QN 17: Toss advantage analysis showing percentage of matches won by toss-winning teams, broken down by toss decision (bat first/bowl first).",
        "QN 18: Most economical bowlers in ODI and T20 with overall economy rate and total wickets for bowlers with ≥10 matches and ≥2 overs per match.",
        "QN 19: Most consistent batsmen since 2022 with average runs and standard deviation for players facing ≥10 balls per innings.",
        "QN 20: Matches played and batting averages per player across formats, showing Test, ODI, T20 match counts and respective batting averages for players with ≥20 total matches.",
        "QN 21: Comprehensive player ranking combining batting, bowling, and fielding performance using weighted scores. Top performers ranked for each format (Test, ODI, T20, IPL).",
        "QN 22: Head-to-head match analysis for team pairs with ≥5 matches in the last 3 years, showing total matches, wins for each team, average victory margin, performance batting first vs bowling first, and overall win percentage.",
        "QN 23: Recent player form analysis based on last 10 batting performances, showing average runs in last 5 vs last 10 matches, recent strike rate trends, number of scores above 50, consistency score, and form category.",
        "QN 24: Successful batting partnerships for pairs with ≥5 consecutive partnerships, showing average partnership runs, count of 50+ partnerships, highest partnership, success rate, and ranking best combinations.",
        "QN 25: Time-series analysis of player performance evolution, tracking quarterly average runs and strike rate, trends compared to previous quarters, and career phase categorization for players with ≥6 quarters and ≥3 matches per quarter."
    ]

    # ✅ Build pickle_dict
    pickle_dict = {}
    for i in qns:
        q_num = i.split(":")[0].replace("QN", "").strip()
        for suffix in ["", "_test", "_odi", "_t20", "_ipl", "_1", "_2", "_3", "_4"]:
            filename = f"qn_{q_num}{suffix}.pkl"
            filepath = os.path.join(Data_dir, filename)
            if os.path.exists(filepath):
                pickle_dict.setdefault(q_num, []).append(filepath)

    # Dropdown
    selected_question = st.selectbox("Choose a question:", qns)
    st.caption("Showing results from pre-saved pickle files.")
    q_num = selected_question.split(":")[0].replace("QN", "").strip()

    # Special handling
    if q_num == "21" and q_num in pickle_dict:
        st.subheader("🥇 Top 5 Players per Format")
        tabs = st.tabs(["Test", "ODI", "T20", "IPL"])
        for tab, path in zip(tabs, sorted(pickle_dict[q_num])):
            with tab:
                df = pd.read_pickle(path)
                st.dataframe(df.reset_index(drop=True), use_container_width=True)

    elif q_num == "22" and q_num in pickle_dict:
        st.subheader("🤝 Head-to-Head Match Analysis")
        tabs = st.tabs(["Summary", "Venue-wise"])
        for tab, path in zip(tabs, sorted(pickle_dict[q_num])):
            with tab:
                df = pd.read_pickle(path)
                st.dataframe(df.reset_index(drop=True), use_container_width=True)

    elif q_num in pickle_dict:
        df = pd.read_pickle(pickle_dict[q_num][0])
        st.dataframe(df.reset_index(drop=True), use_container_width=True)
    else:
        st.info("ℹ️ No data available for this question yet.")
