import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. CONFIGURATION ---
PLAN_FILE = "plan.csv"
DATA_FILE = "data.csv"

# Consistent Icon: Compass
st.set_page_config(page_title="Dashboard", page_icon="🧭", layout="wide")

# --- 2. DATA ENGINE (FIXED & ROBUST) ---
def load_plan():
    """Reads the budget plan from plan.csv safely."""
    if os.path.exists(PLAN_FILE):
        try:
            df = pd.read_csv(PLAN_FILE)
            if not df.empty:
                return df.iloc[0] 
        except Exception:
            return None
    return None

def load_expenses():
    """Reads logged expenses from data.csv and cleans columns."""
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            df = pd.read_csv(DATA_FILE)
            # Standardize: Trim spaces and Capitalize
            df.columns = df.columns.str.strip().str.title()
            
            # Handle naming conflicts (Timestamp vs Date)
            if "Timestamp" in df.columns:
                df.rename(columns={"Timestamp": "Date"}, inplace=True)
            
            # Convert to Datetime safely
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
            return df.dropna(subset=["Date"])
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

# --- 3. MAIN UI ---
st.title("🧭 Survival Dashboard")
st.caption("Your real-time financial health and month-end prediction.")

# 1. Load Plan from CSV
plan = load_plan()

if plan is None:
    st.warning("### ⚠️ No Budget Plan Found")
    st.write("MoneyQuest needs a plan to guide you. Please set your budget first.")
    if st.button("🚀 Go to Setup Page"):
        st.switch_page("pages/Setup.py")
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
# Prediction: How many days will the cash last?
days_left_cash = int(money_remaining / daily_safe) if daily_safe > 0 else 0
over_by = max(today_spent - daily_safe, 0)

# Survival Meter % (How much of today's budget is left?)
survival_pc = round(max((daily_safe - today_spent) / daily_safe * 100, 0), 1) if daily_safe > 0 else 0

# 5. UI DISPLAY (Metrics)
with st.container(border=True):
    m1, m2, m3 = st.columns(3)
    m1.metric("Safe Daily Limit", f"₹{daily_safe:,.0f}", help="HINT: This is your daily 'Safe Zone'. Spend less than this.")
    
    # Delta turns RED if overspending
    m2.metric("Spent Today", f"₹{today_spent:,.0f}", 
              delta=f"Over by ₹{over_by:,.0f}" if over_by > 0 else None, 
              delta_color="inverse",
              help="HINT: Your total spending today. Delta shows how much you exceeded your limit.")
    
    m3.metric("Survival Time", f"{days_left_cash} Days", help="HINT: At this rate, your money will last this many days.")

st.divider()

# 6. SURVIVAL METER
st.subheader(f"Today's Survival Meter: {survival_pc}%")
# Ensure bar is between 0 and 1
bar_val = min(float(survival_pc) / 100, 1.0)
st.progress(bar_val)

if over_by > 0:
    st.error(f"🔴 **Danger Zone:** You are ₹{over_by:,.0f} over your limit today. Expect a 'Broke Week' if you don't cut back!")
else:
    st.success(f"🟢 **Safe Zone:** You have ₹{daily_safe - today_spent:,.0f} remaining for today.")

st.divider()

# 7. RECENT TRANSACTIONS (Added for User Friendliness)
with st.expander("📝 View Recent Spending"):
    if not df_expenses.empty:
        st.dataframe(
            df_expenses.sort_values(by="Date", ascending=False), 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.info("No expenses logged yet. Your history will appear here.")

# 8. NAVIGATION
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🏠 Home", use_container_width=True): st.switch_page("Main.py")
with c2:
    if st.button("💸 Log Expense", use_container_width=True): st.switch_page("pages/Expense.py")
with c3:
    if st.button("⚙️ Change Plan", use_container_width=True): st.switch_page("pages/Setup.py")