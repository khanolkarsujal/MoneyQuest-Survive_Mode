import streamlit as st
import pandas as pd
import os
from datetime import datetime
import calendar

# --- 1. CONFIGURATION ---
PLAN_FILE = "plan.csv"
DATA_FILE = "data.csv"

st.set_page_config(page_title="Dashboard", page_icon="🧭", layout="wide")

# --- 2. DATA ENGINE ---
def load_plan():
    if os.path.exists(PLAN_FILE):
        try:
            df = pd.read_csv(PLAN_FILE)
            if not df.empty:
                # Standardize column for date check
                df.columns = df.columns.str.strip().str.title()
                return df.iloc[0] 
        except: return None
    return None

def load_expenses():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            df = pd.read_csv(DATA_FILE)
            df.columns = df.columns.str.strip().str.title()
            if "Timestamp" in df.columns: df.rename(columns={"Timestamp": "Date"}, inplace=True)
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
            return df.dropna(subset=["Date"])
        except: return pd.DataFrame()
    return pd.DataFrame()

# --- 3. AUTO-RESET & VALIDATION LOGIC ---
def check_month_reset(plan):
    """Checks if the stored plan belongs to a previous month."""
    if 'Setup_Date' in plan or 'Date' in plan:
        # Get the date the plan was created
        plan_date_str = plan.get('Setup_Date', plan.get('Date'))
        plan_month = pd.to_datetime(plan_date_str).month
        current_month = datetime.now().month
        
        if current_month != plan_month:
            return True # Month has changed!
    return False

# --- MAIN UI ---
st.title("🧭 Survival Dashboard")

plan = load_plan()

# 1. Handle Missing Plan or Month Reset
if plan is None:
    st.warning("### ⚠️ No Budget Plan Found")
    if st.button("🚀 Go to Setup Page"): st.switch_page("pages/Setup.py")
    st.stop()

if check_month_reset(plan):
    st.balloons()
    st.success("🎊 **NEW MONTH DETECTED!** Your previous survival mission is complete.")
    st.info("The month has changed. Please reset your data to start a new MoneyQuest.")
    if st.button("🗑️ Clear Old Data & Reset"):
        if os.path.exists(PLAN_FILE): os.remove(PLAN_FILE)
        if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
        st.rerun()
    st.stop()

# 2. Extract Values
daily_safe = plan["Daily_Safe_Spend"]
available_money = plan["Available_Money"]

# 3. Process Expenses
df_expenses = load_expenses()
today_spent = 0
total_spent = 0
if not df_expenses.empty:
    today = datetime.now().date()
    today_spent = df_expenses[df_expenses["Date"].dt.date == today]["Amount"].sum()
    total_spent = df_expenses["Amount"].sum()

# 4. Math Logic
money_remaining = available_money - total_spent
days_left_cash = int(money_remaining / daily_safe) if daily_safe > 0 else 0
over_by = max(today_spent - daily_safe, 0)
survival_pc = round(max((daily_safe - today_spent) / daily_safe * 100, 0), 1) if daily_safe > 0 else 0

# --- 5. CONGRATULATIONS LOGIC ---
today_day = datetime.now().day
last_day_of_month = calendar.monthrange(datetime.now().year, datetime.now().month)[1]

if today_day >= (last_day_of_month - 3) and over_by == 0:
    st.balloons()
    st.success(f"🎊 **YOU DID IT!** It is the end of the month and you are still in the Safe Zone. Survival accomplished!")

# 6. UI DISPLAY
with st.container(border=True):
    st.caption("📍 **Key Performance Indicators**")
    m1, m2, m3 = st.columns(3)
    m1.metric("Safe Daily Limit", f"₹{daily_safe:,.0f}", help="Your daily allowance.")
    m2.metric("Spent Today", f"₹{today_spent:,.0f}", delta=f"Over by ₹{over_by:,.0f}" if over_by > 0 else None, delta_color="inverse")
    m3.metric("Survival Time", f"{days_left_cash} Days", help="Days until you hit ₹0.")

st.divider()

# 7. SURVIVAL METER
st.subheader(f"Today's Survival Meter: {survival_pc}%")
bar_val = min(float(survival_pc) / 100, 1.0)
st.progress(bar_val)

if over_by > 0:
    st.error(f"🔴 **Danger Zone:** You exceeded your limit. Spend ₹0 tomorrow to recover!")
else:
    st.success(f"🟢 **Safe Zone:** You are currently a Financial Master today.")

st.divider()

# 8. WEEKLY REALITY CHECK (Additional Feature)
with st.expander("📊 Weekly Analytics"):
    if not df_expenses.empty:
        last_7_days = df_expenses[df_expenses["Date"] > (datetime.now() - pd.Timedelta(days=7))]
        weekly_total = last_7_days["Amount"].sum()
        avg_daily = weekly_total / 7
        st.write(f"**Past 7 Days Total:** ₹{weekly_total}")
        st.write(f"**Average Daily Spend:** ₹{avg_daily:,.2f}")
        if avg_daily > daily_safe:
            st.warning(f"⚠️ Your weekly average (₹{avg_daily:,.0f}) is higher than your safe limit!")
    else:
        st.write("Not enough data for weekly analytics.")

# 9. NAVIGATION
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🏠 Home", use_container_width=True): st.switch_page("Main.py")
with c2:
    if st.button("💸 Log Expense", use_container_width=True): st.switch_page("pages/Expense.py")
with c3:
    if st.button("⚙️ Change Plan", use_container_width=True): st.switch_page("pages/Setup.py")

st.caption("MoneyQuest | Your automated financial survival compass. 🍕")