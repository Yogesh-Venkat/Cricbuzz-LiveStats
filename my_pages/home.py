import streamlit as st
def app():
    st.title("Home Page")


    st.title("🏠 Welcome to the Cricket Analytics Dashboard")
        
    st.write("""
    Explore comprehensive cricket statistics and live match updates in one interactive dashboard!  

    This project leverages **real-time cricket data**, SQL analytics, and Python-based data processing for a complete cricket insights experience.
    """)

    st.subheader("🛠 Tools")
    st.markdown("""
    - **Streamlit** for interactive web app  
    - **MySQL** for storing and querying cricket data  
    - **Python** libraries: `pandas`, `mysql.connector`  
    - **Cricbuzz API** for live match data
    """)

    st.subheader("🌟 Key Features")
    st.markdown("""
    1. **Live Match Updates**  
        - Follow ongoing matches with ball-by-ball details  
        - View batsmen/bowler performance and match summary  

    2. **Top Player Statistics**  
        - Analyze top performers in batting and bowling  
        - Metrics include most runs, highest scores, wickets, strike rates, and economy rates  

    3. **SQL Queries & Insights**  
        - Run 25+ advanced SQL queries to explore player and match data  
        - Interactive tables for instant insights  

    4. **CRUD Operations**  
        - Add, update, delete, or view player and match records  
        - Form-based interface for easy database management  

    5. **User Guidance**  
        - Use the **sidebar** to navigate across pages  
        - Project documentation and instructions included
    """)

    st.info("📌 Navigate using the sidebar to explore Live Matches, Top Player Stats, SQL Analytics, and CRUD operations!")

