import streamlit as st
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(r"C:\Users\yoges\OneDrive\Desktop\Guvi\Cricbuzz-LiveStats\.env")

from utils.fetch_live import fetch_live_matches, fetch_scorecard  # Make sure this exists

def app():
    st.title("🎥 Live Cricket Matches - Real Time Updates ⚡")
    st.write("Follow ongoing matches with live stats and scorecards.")

    # Fetch live matches from API
    data = fetch_live_matches()
    if not data:
        st.info("📭 No live matches available at the moment. Make sure CRICBUZZ_API_KEY is set in .env")
        return

    matches, match_id_list, match_info_map = [], [], {}
    for t in data.get("typeMatches", []):
        for sm in t.get("seriesMatches", []):
            if 'seriesAdWrapper' in sm:
                for m in sm['seriesAdWrapper'].get("matches", []):
                    info = m['matchInfo']
                    team1 = info.get("team1", {}).get("teamName", "Team 1")
                    team2 = info.get("team2", {}).get("teamName", "Team 2")
                    match_desc = info.get("matchDesc", "")
                    matches.append(f"🏏 {team1} vs {team2} - {match_desc}")
                    match_id_list.append(int(info.get("matchId")))
                    venue = info.get("venueInfo", {}).get("ground", "N/A")
                    series_name = info.get("seriesName", "N/A")
                    match_format = info.get("matchFormat", "N/A")
                    start_ts = int(info.get("startDate", 0))
                    start_date = datetime.fromtimestamp(start_ts / 1000).strftime("%d %b %Y") if start_ts else "N/A"
                    match_info_map[int(info.get("matchId"))] = {
                        "team1": team1,
                        "team2": team2,
                        "venue": venue,
                        "series": series_name,
                        "format": match_format,
                        "start_date": start_date
                    }

    if not matches:
        st.info("📭 No live matches available right now.")
        return

    # Match selection dropdown
    selected_match = st.selectbox("🎯 **Select a Match to Follow:**", matches)
    selected_index = matches.index(selected_match)
    selected_match_id = match_id_list[selected_index]
    info = match_info_map[selected_match_id]

    st.markdown(f"##  {info['team1']} vs {info['team2']}")
    c1, c2 = st.columns([1, 2])
    c1.markdown(f"📝 **Format:** {info['format']}")
    c2.markdown(f"🏆 **Series:** {info['series']}")
    c3, c4 = st.columns([1, 2])
    c3.markdown(f"📅 **Date:** {info['start_date']}")
    c4.markdown(f"🏟 **Venue:** {info['venue']}")

    # Fetch scorecard
    match_data = fetch_scorecard(selected_match_id)
    if not match_data:
        st.info("📭 Scorecard not available yet.")
        return

    status_text = match_data.get("status", "N/A")
    st.markdown(f"**Match Status**: {status_text}")

    scorecards = match_data.get("scorecard", [])
    if not scorecards:
        st.info("📭 Live innings not started yet.")
        return

    # Determine current innings
    live_innings = next((inn for inn in scorecards if inn.get("isCurrent")), None)
    if not live_innings:
        live_innings = next((inn for inn in reversed(scorecards) if inn.get("score")), scorecards[-1])

    st.markdown("### Current Innings")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏏 Batting Team", live_innings.get("batteamname", "N/A"))
    c2.metric("📈 Score", f"{live_innings.get('score', '0')}/{live_innings.get('wickets', '0')}")
    c3.metric("⏱ Overs", live_innings.get("overs", "0"))
    c4.metric("⚡ Run Rate", live_innings.get("runrate", "0"))

    # Tabs for each innings
    innings_tabs = st.tabs([f"🏟 Innings {i+1}" for i in range(len(scorecards))])
    for idx, inn in enumerate(scorecards):
        with innings_tabs[idx]:
            st.markdown(f"### {inn.get('batteamname','N/A')} - {inn.get('score',0)}/{inn.get('wickets',0)} ({inn.get('overs','0')} overs)")
            nested_tabs = st.tabs(["🏏 Batting", "🔴 Bowling", "🤝 Partnerships"])

            # Batting tab
            with nested_tabs[0]:
                batsmen = [[b.get("name","N/A"), b.get("runs","0"), b.get("balls","0"), b.get("fours","0"),
                            b.get("sixes","0"), b.get("strkrate","0"), b.get("outdec","N/A")] 
                           for b in inn.get("batsman", [])]
                if batsmen:
                    st.table(pd.DataFrame(batsmen, columns=["Batsman","R","B","4s","6s","SR","Status"]))
                else:
                    st.info("📭 Batsman details not available.")

            # Bowling tab
            with nested_tabs[1]:
                bowlers = [[b.get("name","N/A"), b.get("overs","0"), b.get("maidens","0"), b.get("runs","0"),
                            b.get("wickets","0"), b.get("economy","0")] 
                           for b in inn.get("bowler", [])]
                if bowlers:
                    st.table(pd.DataFrame(bowlers, columns=["Bowler","O","M","R","W","Econ"]))
                else:
                    st.info("📭 Bowler details not available.")

            # Partnerships tab
            with nested_tabs[2]:
                partnerships = [[p.get("bat1name","N/A"), p.get("bat2name","N/A"), p.get("totalruns","N/A"), p.get("totalballs","N/A")] 
                                for p in inn.get("partnership", {}).get("partnership", [])]
                if partnerships:
                    st.table(pd.DataFrame(partnerships, columns=["Batsman 1","Batsman 2","Runs","Balls"]))
                else:
                    st.info("📭 Partnership details not available.")
