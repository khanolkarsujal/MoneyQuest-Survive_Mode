import streamlit as st
import pandas as pd
import os

file_path = "data.csv"

st.title("📊 Month Survival Dashboard")

# Check session state
daily_safe = st.session_state.get("Daily Safe Spend")
available_money = st.session_state.get("Available Money")
days_remaining = st.session_state.get("Days Remaining")
current_daily_spend = st.session_state.get("Current Daily Spend")

if daily_safe is None:
    st.warning("Daily Safe Spend is not calculated yet. Go to Setup page.")
else:
    st.metric("Daily Safe Spend", f"₹{daily_safe}")

    # Calculate today's spending
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        today_spent = df[df["Timestamp"].dt.date == pd.Timestamp.today().date()]["Amount"].sum()
    else:
        today_spent = 0

    over_by = max(today_spent - daily_safe, 0)
    survival_percentage = round(max((daily_safe - today_spent) / daily_safe * 100, 0), 2) if daily_safe > 0 else 0

    money_remaining = available_money - df["Amount"].sum() if os.path.exists(file_path) else available_money
    money_last_days = int(money_remaining / daily_safe) if daily_safe > 0 else 0

    # Display metrics
    st.subheader("🟢 Overspending State")
    st.markdown(f"**Daily Safe Spend:** ₹{daily_safe}")
    st.markdown(f"**Today Spent:** ₹{today_spent}")
    st.markdown(f"**Over by:** ₹{over_by} {'⚠' if over_by>0 else '✅'}")
    st.markdown("---")
    st.subheader(f"Survival Meter: {survival_percentage}%")
    st.progress(min(int(survival_percentage), 100))
    st.markdown("---")
    st.metric("Money will last", f"{money_last_days} days")