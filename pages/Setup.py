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
st.caption("📍 **STEP 1:** Tell MoneyQuest about your finances to build your survival compass.")
st.markdown("<p style='color: #888;'>Set your boundaries to avoid the month-end crunch.</p>", unsafe_allow_html=True)

# Load existing data to pre-fill the form
existing_plan = load_existing_plan()

# --- STEP 1: INPUTS (Enhanced with User Hints) ---
st.info("💡 **Hint:** Be honest with these numbers. We subtract your bills first so you don't accidentally spend your rent money.")

with st.container(border=True):
    st.subheader("💰 Monthly Financials")
    st.caption("📍 **Action:** Enter your current cash and upcoming mandatory bills.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # We pre-fill using existing_plan if available
        default_total = float(existing_plan["Total_Money"]) if existing_plan is not None else 0.0
        total_money = st.number_input(
            "Current Cash (₹)", 
            min_value=0.0, 
            value=default_total,
            help="POP-UP HINT: Enter ALL the money you have right now (Bank balance + Cash in hand + GPay balance). This is your starting point."
        )
    
    with col2:
        default_fixed = float(existing_plan["Fixed_Expenses"]) if existing_plan is not None else 0.0
        fixed_expenses = st.number_input(
            "Upcoming Bills (₹)", 
            min_value=0.0, 
            value=default_fixed,
            help="POP-UP HINT: Enter costs you MUST pay before the month ends (e.g., Room Rent, Mess bill, Wi-Fi, or Exam fees). We hide this money so you don't spend it."
        )

    st.divider()
    
    days_left = get_days_remaining()
    st.info(f"📅 **Calendar Check:** There are **{days_left} days** left in this month.")
    st.caption("HINT: We use this to divide your available money equally across the remaining days.")

# --- STEP 2: CALCULATE & SAVE (Enhanced Tooltips) ---
if st.button("🚀 Initialize Survival Mode", 
             use_container_width=True, 
             help="POP-UP HINT: Click this to lock in your numbers and calculate your 'Daily Safe Limit'."):
    
    available = total_money - fixed_expenses
    
    if available < 0:
        st.error("🚨 **Error:** Your bills exceed your cash. You are already in the negative! Please adjust your numbers.")
    elif total_money == 0:
        st.warning("⚠️ **Expected Action:** Please enter your current cash amount to start the calculation.")
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
        m1.metric("Available Pool", f"₹{available:,.0f}", help="This is what you have left to spend on Food, Travel, and fun.")
        m2.metric("Safe Daily Limit", f"₹{daily_safe:,.0f}", help="HINT: If you spend EXACTLY this much every day, you will reach the end of the month with ₹0. Spend less to save more!")

# --- STEP 3: HINTS & NAVIGATION ---
st.markdown("---")

with st.expander("💡 Pro-Tip for Engineering Students"):
    st.write("""
    - **Be Strict:** By setting this plan, you ensure you don't spend your rent money on a midnight pizza.
    - **Persistence:** Even if you close the app, your plan is safe.
    - **Update Often:** If you get extra cash mid-month, come back here and update your 'Current Cash'.
    """)

c1, c2 = st.columns(2)
with c1:
    if st.button("📊 Go to Dashboard", 
                 type="primary", 
                 use_container_width=True,
                 help="HINT: Click here to see your Survival Meter and real-time status."):
        if "Daily_Safe_Spend" in locals() or load_existing_plan() is not None:
            st.switch_page("pages/Dashboard.py")
        else:
            st.error("Action Required: Please click 'Initialize Survival Mode' above first!")
with c2:
    if st.button("🏠 Home", 
                 use_container_width=True,
                 help="HINT: Go back to the main landing page."):
        st.switch_page("Main.py")



st.markdown("---")
st.subheader("🗑️ Danger Zone")
with st.expander("Reset All MoneyQuest Data"):
    st.warning("This will permanently delete your 'plan' and all logged expenses in 'data'.")
    if st.button("Delete All Data & Start Fresh"):
        if os.path.exists("plan.csv"): os.remove("plan.csv")
        if os.path.exists("data.csv"): os.remove("data.csv")
        st.success("All data deleted! Please refresh the page.")
        st.balloons()