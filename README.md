# 🏏 Cricbuzz LiveStats Dashboard

A Streamlit-based cricket statistics dashboard that fetches live match data, scorecards, player stats, and supports SQL analytics + CRUD operations.  

This project is built with Python, Streamlit, and MySQL, integrating live cricket data for analysis and visualization.  

---

## 🚀 Features

- 📡 **Live Match Tracking** – View live scores and match details in real time  
- 📊 **Scorecards** – Detailed score updates (batsmen, bowlers, partnerships, etc.)  
- 🥇 **Top Player Stats** – Analyze player performance across formats  
- 📈 **SQL Analytics** – Run queries on match/player data  
- 📝 **CRUD Operations** – Add, edit, delete, and manage data  
- 🎨 **Custom Sidebar Navigation** – Clean UI with modular pages  

---

## 📂 Project Structure

```
Cricbuzz-LiveStats/
│── app.py                  # Main entry point
│── .env                    # Environment variables (DB credentials, API keys)
│── .env.example            # Example env file (template for users)
│── utils/
│   ├── __init__.py
│   ├── fetch_live.py 
│   └── queries.py      # Functions to fetch live matches & scorecards
│── my_pages/               # Custom pages (Home, Live Match, etc.)
│   ├── __init__.py
│   ├── home.py
│   ├── live_match.py
│   ├── top_players.py
│   ├── sql_analytics.py
│   └── crud.py
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
```

---

## ⚙️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/Cricbuzz-LiveStats.git
   cd Cricbuzz-LiveStats
   ```

2. **Create virtual environment & activate**  
   ```bash
   python -m venv venv
   venv\Scripts\activate    # On Windows
   source venv/bin/activate # On Mac/Linux
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 API Key Setup

This project uses the **Cricbuzz API** for live cricket data.  

1. Copy the example environment file:  
   ```bash
   cricbuzz_api_key.env.sample
   ```

2. Open `cricbuzz_api_key.env.sample` and add your **Cricbuzz API key**:  
   ```ini
   CRICBUZZ_API_KEY=your_api_key_here
   ```

3. Save and run the app:  
   ```bash
   streamlit run app.py
   ```


---

## ▶️ Running the App

Start the Streamlit server:
```bash
streamlit run app.py
```

Then open:  
👉 [http://localhost:8501](http://localhost:8501)  

---

## 📜 Requirements

Main libraries used:
- Streamlit
- MySQL Connector
- Pandas
- python-dotenv

---

## 🖼️ Screenshots

### Sidebar Navigation
- 🏡 Home  
- 🎥 Live Match  
- 🥇 Top Player Stats  
- 📈 SQL Queries & Analytics  
- 📝 CRUD Operations  

![alt text](image.png)

---

## 🛠️ Future Improvements

- Add player vs player comparison charts  
- Improve scorecard UI (team logos, match highlights)  
- Deploy on Streamlit Cloud / Docker  

---

## 👨‍💻 Author

- **Your Name** – [GitHub](https://github.com/your-username)

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
