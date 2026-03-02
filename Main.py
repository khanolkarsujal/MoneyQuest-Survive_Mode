import streamlit as st
import pandas as pd
import os
from datetime import datetime
import calendar

# --- 1. PAGE CONFIG (Friendly Icon: Compass) ---
st.set_page_config(
    page_title="MoneyQuest",
    page_icon="🧭", 
    layout="centered",
)

# --- 2. CUSTOM CSS (Minimalist & Professional) ---
st.markdown("""
    <style>
    .hero-container {
        background-color: #1E1E1E;
        padding: 35px;
        border-radius: 15px;
        border-left: 10px solid #007bff;
        margin-bottom: 25px;
    }
    .hero-quote {
        font-size: 30px !important; 
        font-weight: 700;
        color: #FFFFFF !important;
        line-height: 1.3;
    }
    .q-mark {
        color: #007bff;
        font-size: 45px;
        font-weight: 800;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        transition: 0.2s;
    }
    .stButton>button:hover {
        border: 2px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA CHECK (Provident Logic) ---
PLAN_FILE = "plan.csv"
def get_daily_limit():
    if os.path.exists(PLAN_FILE):
        try:
            df = pd.read_csv(PLAN_FILE)
            return df.iloc[0]["Daily_Safe_Spend"]
        except: return None
    return None

# --- 4. HERO SECTION ---
st.title("🧭 MoneyQuest")
st.caption("The Financial Survival Tool for Engineering Students")

st.markdown(
    """
    <div class="hero-container">
        <p class="hero-quote">
            <span class="q-mark">&ldquo;</span>
            Stop the Month-End Crisis. Master your daily limit today so you never feel <b>broke</b> in the last 7 days.
            <span class="q-mark">&rdquo;</span>
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# --- 5. NAVIGATION HUB (Simple & Intuitive) ---
st.subheader("🚀 Quick Actions")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.write("### 🛠️ The Plan")
        st.caption("HINT: Set your budget once a month.")
        if st.button("Setup / Change Budget", help="Define your income and bills."):
            st.switch_page("pages/Setup.py") 
        
        if st.button("📊 View Dashboard", help="Check your survival meter and stats."):
            st.switch_page("pages/Dashboard.py")

with col2:
    with st.container(border=True):
        st.write("### 💸 The Spend")
        st.caption("HINT: Log your costs daily.")
        if st.button("➕ Add Expense", help="Log chai, lunch, or Xerox costs."):
            st.switch_page("pages/Expense.py") 
        
        if st.button("📖 How to Use", help="Understand how MoneyQuest works."):
            st.switch_page("pages/How_to_Use.py")

# --- 6. REAL-TIME STATUS (Helpful Hints) ---
st.markdown("<br>", unsafe_allow_html=True)
today = datetime.today()
last_day = calendar.monthrange(today.year, today.month)[1]
days_left = (last_day - today.day) + 1

daily_limit = get_daily_limit()

if daily_limit:
    st.success(f"🎯 **Target:** Stay under **₹{daily_limit:,.0f}/day** to survive the next **{days_left} days**.")
else:
    st.warning(f"📅 **Calendar Check:** {days_left} days remaining. Start by setting a plan above!")

# --- 7. FOOTER ---
st.divider()
st.caption("Built for students who want to eat more than just Maggi in the last week of the month. 🍕")