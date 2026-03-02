import streamlit as st
import pandas as pd
import os
from datetime import datetime
import calendar

# --- 1. PAGE CONFIG (Consistent Icon: Compass) ---
st.set_page_config(page_title="Setup Budget", page_icon="🧭", layout="centered")

# --- CONFIGURATION ---
PLAN_FILE = "plan.csv"

# --- SETTINGS & LOGIC ---
def get_days_remaining():
    """Calculates days left in the month, including today."""
    today = datetime.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    days = (last_day - today.day) + 1
    return max(days, 1)

def calculate_daily_budget(available_money, days_left):
    """Core logic to determine the safe daily spend."""
    if days_left <= 0: return 0
    return round(available_money / days_left, 2)

def load_existing_plan():
    """Loads plan from CSV if it exists."""
    if os.path.exists(PLAN_FILE):
        try:
            df = pd.read_csv(PLAN_FILE)
            if not df.empty:
                return df.iloc[0]
        except:
            return None
    return None

# --- UI HEADER ---
st.title("🧭 Setup Your Plan")
st.markdown("<p style='color: #888;'>Set your boundaries to avoid the month-end crunch.</p>", unsafe_allow_html=True)

# Load existing data to pre-fill the form
existing_plan = load_existing_plan()

# --- STEP 1: INPUTS ---
with st.container(border=True):
    st.subheader("💰 Monthly Financials")
    st.caption("MoneyQuest saves this to 'plan.csv' so your budget stays locked.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # We pre-fill using existing_plan if available
        default_total = float(existing_plan["Total_Money"]) if existing_plan is not None else 0.0
        total_money = st.number_input(
            "Current Cash (₹)", 
            min_value=0.0, 
            value=default_total,
            help="How much money do you actually have right now?"
        )
    
    with col2:
        default_fixed = float(existing_plan["Fixed_Expenses"]) if existing_plan is not None else 0.0
        fixed_expenses = st.number_input(
            "Upcoming Bills (₹)", 
            min_value=0.0, 
            value=default_fixed,
            help="Rent, Mess bills, or Xerox costs you haven't paid yet."
        )

    st.divider()
    
    days_left = get_days_remaining()
    st.info(f"📅 **Calendar Check:** There are **{days_left} days** left in this month.")

# --- STEP 2: CALCULATE & SAVE ---
if st.button("🚀 Initialize Survival Mode", use_container_width=True):
    available = total_money - fixed_expenses
    
    if available < 0:
        st.error("🚨 **Error:** Your bills exceed your cash. Adjust your numbers!")
    elif total_money == 0:
        st.warning("⚠️ Please enter your current cash amount.")
    else:
        daily_safe = calculate_daily_budget(available, days_left)

        # 1. Save to plan.csv (Provident Storage)
        plan_data = {
            "Total_Money": [total_money],
            "Fixed_Expenses": [fixed_expenses],
            "Available_Money": [available],
            "Daily_Safe_Spend": [daily_safe],
            "Days_At_Setup": [days_left]
        }
        pd.DataFrame(plan_data).to_csv(PLAN_FILE, index=False)

        # 2. Update Session State (for immediate Dashboard use)
        st.session_state["Daily Safe Spend"] = daily_safe
        st.session_state["Available Money"] = available

        st.success("### ✅ Plan Saved to plan.csv!")
        st.balloons()
        
        m1, m2 = st.columns(2)
        m1.metric("Available Pool", f"₹{available:,.0f}")
        m2.metric("Safe Daily Limit", f"₹{daily_safe:,.0f}")

# --- STEP 3: HINTS & NAVIGATION ---
st.markdown("---")

with st.expander("💡 Pro-Tip for Engineering Students"):
    st.write("""
    - **Be Strict:** By setting this plan, you ensure you don't spend your rent money on a midnight pizza.
    - **Persistence:** Even if you close the app, your plan is safe in `plan.csv`.
    """)

c1, c2 = st.columns(2)
with c1:
    if st.button("📊 Go to Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
with c2:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Main.py")