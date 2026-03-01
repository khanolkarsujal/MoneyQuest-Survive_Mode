import streamlit as st
import calendar
from datetime import datetime

st.title("Setup Your Month")

today = datetime.today()
last_day = calendar.monthrange(today.year, today.month)[1]
days_remaining = last_day - today.day

total_money = st.number_input("Total Money: ", min_value=0)
fixed_expenses = st.number_input("Fixed Expenses: ", min_value=0)
current_daily_spend = st.number_input("Current Daily Spending: ", min_value=0)

st.write(f"Days Remaining in Month: {days_remaining}")

def survive_mode(available, days_remaining):
    return round(available / days_remaining, 2) if days_remaining > 0 else 0

if st.button("Calculate Survival"):
    available = total_money - fixed_expenses
    if available < 0:
        st.error("Fixed expenses cannot be greater than total money.")
    else:
        calculate_survival = survive_mode(available, days_remaining)
        # Store in session state
        st.session_state["Daily Safe Spend"] = calculate_survival
        st.session_state["Available Money"] = available
        st.session_state["Days Remaining"] = days_remaining
        st.session_state["Current Daily Spend"] = current_daily_spend
        st.success(f"You can safely spend ₹{calculate_survival} per day.")