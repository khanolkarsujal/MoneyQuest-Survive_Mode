import streamlit as st

# --- 1. PAGE CONFIG (Consistent Icon: Compass) ---
st.set_page_config(page_title="User Guide", page_icon="🧭", layout="centered")

# --- 2. HEADER ---
st.title("🧭 MoneyQuest: Mission Briefing")
st.caption("How to beat the month-end crisis and survive until next payday.")

st.markdown("---")

# --- 3. THE MISSION (THE WHY) ---
with st.container(border=True):
    st.subheader("🎯 The Mission")
    st.write("""
    Most students feel broke in the last 7 days of the month. MoneyQuest changes that by calculating 
    your **Safe Daily Limit** in real-time. 
    
    If you spend less than your limit today, you'll have more money tomorrow. It's that simple.
    """)

# --- 4. THE 3-STEP SURVIVAL PROCESS ---
st.write("### 🚀 The 3-Step Process")

# STEP 1: SETUP
with st.expander("⚙️ Step 1: Set Your Plan", expanded=True):
    st.write("""
    - **Go to:** The **Setup Budget** page.
    - **Action:** Enter your **Current Cash** (what you have right now) and your **Upcoming Bills** (Rent, Mess, Xerox).
    - **Result:** We save your budget to `plan.csv`. This is your foundation.
    """)

# STEP 2: LOGGING
with st.expander("💸 Step 2: Log as You Spend", expanded=True):
    st.write("""
    - **Go to:** The **Log Expense** page.
    - **Action:** Every time you buy a Chai, Samosa, or Bus ticket, record the amount immediately.
    - **Result:** We append your spending to `data.csv`. Your survival meter updates instantly.
    """)

# STEP 3: DASHBOARD
with st.expander("📊 Step 3: Check Your Compass", expanded=True):
    st.write("""
    - **Go to:** The **Dashboard**.
    - **Safe Zone (Green):** You're on track! You can spend your remaining daily limit safely.
    - **Danger Zone (Red):** You overspent. You must spend less tomorrow to get back to the Green zone.
    - **Survival Time:** See exactly how many days your cash will last at your current rate.
    """)

# --- 5. PRO-TIP FOR STUDENTS ---
st.info("""
💡 **Pro-Tip:** The last 7 days are the hardest. If you stay in the **Green Zone** for the first 20 days, 
the last 7 days will feel like a breeze instead of a crisis!
""")

# --- 6. WHERE IS MY DATA? ---
with st.container(border=True):
    st.subheader("📂 Where is my data?")
    st.write("MoneyQuest is private and runs locally on your machine. We store your data in two files:")
    st.markdown("""
    - `plan.csv`: Stores your budget settings and income.
    - `data.csv`: Stores your full list of logged expenses.
    """)
    st.caption("⚠️ **HINT:** Do not delete these files, or you will lose your history and budget settings!")

# --- 7. NAVIGATION ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home", use_container_width=True): st.switch_page("Main.py")
with col2:
    if st.button("⚙️ Setup", use_container_width=True): st.switch_page("pages/Setup.py")
with col3:
    if st.button("📊 Dashboard", use_container_width=True): st.switch_page("pages/Dashboard.py")

# --- 8. FOOTER ---
st.markdown("---")
st.caption("MoneyQuest | Built by students, for students. 🍕")