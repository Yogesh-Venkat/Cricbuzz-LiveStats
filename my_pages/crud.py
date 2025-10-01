import streamlit as st
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv(dotenv_path=r"C:\Users\yoges\OneDrive\Desktop\Guvi\Cricbuzz-LiveStats\.env")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_AUTH_PLUGIN = os.getenv("DB_AUTH_PLUGIN")
import mysql.connector 

def app():
    
    st.title("📝 CRUD Operations")
    st.write("Perform Create, Read, Update, Delete operations here.")

    # --- DB CONNECTION ---
    def get_connection():
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            auth_plugin=DB_AUTH_PLUGIN
        )
   
    # --- READ (Fetch Series) ---
    def fetch_series():
        conn = get_connection()
        query = """
        SELECT 
            seriestype AS `SERIES TYPE`,
            series_id AS `SERIES ID`,
            series_name AS `SERIES NAME`,
            start_date AS `START DATE`,
            end_date AS `END DATE`
        FROM series;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    # --- CREATE (Insert Series) ---
    def add_series(series_id, seriestype, series_name, start_date, end_date):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO series (series_id, seriestype, series_name, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (series_id, seriestype, series_name, start_date, end_date))
        conn.commit()
        conn.close()

    # --- UPDATE ---
    def update_series(series_id, seriestype, series_name, start_date, end_date):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE series
            SET seriestype=%s, series_name=%s, start_date=%s, end_date=%s
            WHERE series_id=%s
        """, (seriestype, series_name, start_date, end_date, series_id))
        conn.commit()
        conn.close()

    # --- DELETE ---
    def delete_series(series_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM series WHERE series_id=%s", (series_id,))
        conn.commit()
        conn.close()

    st.title("📝 CRUD - Manage Series")

    # Menu in CRUD order
    menu = ["📋 View Series", "➕ Add Series", "✏️ Edit Series", "🗑️ Remove Series"]
    choice = st.selectbox("Select Operation", menu)

    # --- READ ---
    if choice == "📋 View Series":
        st.subheader("📋 All Series Records")
        df = fetch_series()
        if df.empty:
            st.warning("⚠️ No series data available in the database.")
        else:
            st.dataframe(df.reset_index(drop=True), use_container_width=True)

    # --- CREATE ---
    elif choice == "➕ Add Series":
        st.subheader("➕ Add a New Series")
        seriestype = st.text_input("Series Type (e.g., Domestic, International, League, Women)")
        series_id = st.text_input("Series ID (must be unique)")
        series_name = st.text_input("Series Name")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

        if st.button("Add Series"):
            if not seriestype or not series_id or not series_name or not start_date or not end_date:
                st.error("⚠️ All fields are required. Please fill in every column.")
            else:
                try:
                    add_series(series_id, seriestype, series_name, start_date, end_date)
                    st.success(f"✅ Series '{series_name}' added successfully!")
                except mysql.connector.IntegrityError:
                    st.error(f"⚠️ Series ID '{series_id}' already exists. Please use a unique ID.")

    # --- UPDATE ---
    elif choice == "✏️ Edit Series":
        st.subheader("✏️ Update Series Details")
        df = fetch_series()
        if df.empty:
            st.warning("⚠️ No series data available to update.")
        else:
            st.dataframe(df.reset_index(drop=True), use_container_width=True)

            series_id = st.text_input("Series ID to Update")
            seriestype = st.text_input("New Series Type")
            series_name = st.text_input("New Series Name")
            start_date = st.date_input("New Start Date")
            end_date = st.date_input("New End Date")

            if st.button("Update Series"):
                update_series(series_id, seriestype, series_name, start_date, end_date)
                st.success("✅ Series updated successfully!")

    # --- DELETE ---
    elif choice == "🗑️ Remove Series":
        st.subheader("🗑️ Delete Series Record")
        df = fetch_series()
        if df.empty:
            st.warning("⚠️ No series data available to delete.")
        else:
            st.dataframe(df.reset_index(drop=True), use_container_width=True)

            series_id = st.text_input("Series ID to Delete")

            if st.button("Delete Series"):
                delete_series(series_id)
                st.success("🗑️ Series deleted successfully!")
