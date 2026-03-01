import streamlit as st
from datetime import datetime
import calendar

# --- 1. PAGE CONFIG (MUST BE FIRST) ---
st.set_page_config(
    page_title="MoneyQuest",
    page_icon="💰",
    layout="centered",
)

# --- 2. CUSTOM CSS FOR BLUE ACCENTS & BIG TEXT ---
st.markdown("""
    <style>
    /* Hero Quote Container with Blue Left Bar */
    .hero-container {
        background-color: #1E1E1E; /* Dark gray for high contrast */
        padding: 40px;
        border-radius: 15px;
        border-left: 8px solid #007bff; /* The Blue Bar */
        margin: 30px 0;
        text-align: left;
    }

    /* The Quote Text - Big and White */
    .hero-quote {
        font-size: 34px !important; 
        font-weight: 700;
        color: #FFFFFF !important;
        line-height: 1.3;
        margin: 0;
    }

    /* Blue Quotation Marks */
    .q-mark {
        color: #007bff;
        font-size: 45px;
        font-weight: 800;
        line-height: 0;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HERO SECTION ---
st.title("💰 MoneyQuest")

# BIG HERO QUOTE WITH BLUE MARKS
st.markdown(
    """
    <div class="hero-container">
        <p class="hero-quote">
            <span class="q-mark">&ldquo;</span>
            Most engineering students don&rsquo;t feel poor at the beginning of the month&hellip; 
            They feel <b>broke</b> in the last 7 days.
            <span class="q-mark">&rdquo;</span>
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

st.write("### Predict your financial survival in real time.")
st.caption("MoneyQuest helps you avoid running out of money before month-end.")

st.divider()

# --- 4. ACTION CENTER ---
col1, col2 = st.columns(2)

with col1:
    st.write("#### 🛠️ The Plan")
    if st.button("Start Survival Mode"):
        st.switch_page("pages/Setup.py") 

with col2:
    st.write("#### 💸 The Spend")
    if st.button("Add Expense"):
        st.switch_page("pages/Expense.py") 

# --- 5. CALENDAR STATUS ---
st.markdown("<br>", unsafe_allow_html=True)
today = datetime.today()
last_day = calendar.monthrange(today.year, today.month)[1]
days_left = (last_day - today.day) + 1

st.info(f"📅 **Calendar Check:** There are **{days_left} days** left in this month. Will your money last?")

# --- 6. FOOTER ---
st.caption("Built for students who want to eat more than just Maggi in the last week of the month.")