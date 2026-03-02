import streamlit as st
import pandas as pd
import os
from datetime import datetime
import calendar

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="MoneyQuest",
    page_icon="🧭", 
    layout="centered",
)

# --- 2. CUSTOM CSS (Minimalist + Glowing Animations) ---
st.markdown("""
    <style>
    /* Glowing Animation for Reminders */
    @keyframes glowing {
        0% { box-shadow: 0 0 5px #007bff; border-color: #007bff; }
        50% { box-shadow: 0 0 20px #007bff; border-color: #00bfff; }
        100% { box-shadow: 0 0 5px #007bff; border-color: #007bff; }
    }
    
    /* NEW: Specific Glow for Recommended Text */
    @keyframes text-glow {
        0% { color: #ffffff; text-shadow: 0 0 5px #007bff; }
        50% { color: #007bff; text-shadow: 0 0 15px #007bff; }
        100% { color: #ffffff; text-shadow: 0 0 5px #007bff; }
    }
    
    .recommended-tag {
        animation: text-glow 1.5s infinite;
        font-weight: bold;
        font-size: 13px;
        letter-spacing: 1px;
    }

    .glow-reminder {
        animation: glowing 2s infinite;
        border: 2px solid #007bff !important;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: rgba(0, 123, 255, 0.05);
    }
    
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

# --- 3. DATA CHECK ---
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

# --- 5. GLOWING REMINDER (Setup Logic) ---
daily_limit = get_daily_limit()

if not daily_limit:
    st.markdown("""
        <div class="glow-reminder">
            <h4 style='margin:0; color:#007bff;'>🚀 ACTION REQUIRED: Setup Your Plan</h4>
            <p style='margin:0; font-size:14px;'>Welcome! Before using the dashboard, you must <b>Step 1: Setup Budget</b> below.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="glow-reminder">
            <h4 style='margin:0; color:#28a745;'>✅ SYSTEM ACTIVE</h4>
            <p style='margin:0; font-size:14px;'>Your compass is set. Remember to <b>Log Expenses</b> as soon as you spend money.</p>
        </div>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION HUB ---
st.subheader("🚀 Quick Actions")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.write("### 🛠️ 1. The Plan")
        st.caption("📍 Start here to set your survival goals.")
        if st.button("Setup / Change Budget", 
                     help="HINT: Click here to enter your current cash and bills."):
            st.switch_page("pages/Setup.py") 
        
        if st.button("📊 View Dashboard", 
                     help="Open this to see your real-time survival meter."):
            st.switch_page("pages/Dashboard.py")

with col2:
    with st.container(border=True):
        st.write("### 💸 2. The Spend")
        st.caption("📍 Daily Habit: Log every cost immediately.")
        if st.button("➕ Add Expense", 
                     help="Log your Chai, Xerox, or Lunch costs here."):
            st.switch_page("pages/Expense.py") 
        
        # --- ENHANCED FOCUS ON HOW TO USE ---
        st.markdown('<p class="recommended-tag">🌟 RECOMMENDED START</p>', unsafe_allow_html=True)
        if st.button("📖 How to Use", 
                     help="CRITICAL: Read this first to understand how to save your money!"):
            st.switch_page("pages/How_to_Use.py")

# --- 7. REAL-TIME STATUS ---
st.markdown("<br>", unsafe_allow_html=True)
today = datetime.today()
last_day = calendar.monthrange(today.year, today.month)[1]
days_left = (last_day - today.day) + 1

if daily_limit:
    st.success(f"🎯 **Target:** Stay under **₹{daily_limit:,.0f}/day** for the next **{days_left} days**.")
else:
    st.warning(f"📅 **Calendar Check:** {days_left} days remaining. Set your plan to unlock your target.")

# --- 8. FOOTER ---
st.divider()
with st.expander("❓ Where do I write what?"):
    st.write("""
    - **Current Money & Bills:** Go to 'Setup Budget'.
    - **Buying Food/Travel/Books:** Go to 'Add Expense'.
    - **Check if I'm Broke:** Go to 'View Dashboard'.
    """)
st.caption("Built for students who want to eat more than just Maggi in the last week of the month. 🍕")
