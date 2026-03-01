import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION & CONSTANTS ---
FILE_PATH = "data.csv"
REQUIRED_COLUMNS = ["Amount", "Category", "Date"] # Standardized names

def load_and_clean_data(path):
    """Loads CSV, handles column naming issues, and returns a clean DataFrame."""
    if not os.path.exists(path):
        return pd.DataFrame()

    try:
        df = pd.read_csv(path)
        if df.empty:
            return df

        # 1. Clean column names (strip spaces and handle case-sensitivity)
        df.columns = df.columns.str.strip().str.title() 
        # Note: .str.title() makes 'date' -> 'Date', 'timestamp' -> 'Timestamp'

        # 2. Handle 'Timestamp' vs 'Date' naming conflict
        if "Timestamp" in df.columns and "Date" not in df.columns:
            df.rename(columns={"Timestamp": "Date"}, inplace=True)

        # 3. Validate required columns exist
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            st.error(f"Missing columns in CSV: {missing}")
            return pd.DataFrame()

        # 4. Standardize Date format
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df = df.dropna(subset=["Date"])
        
        return df
    except Exception as e:
        st.error(f"Critical Error loading data: {e}")
        return pd.DataFrame()

def display_metrics(daily_safe, today_spent, money_remaining, money_last_days):
    """Renders the dashboard UI components."""
    st.subheader("📊 Performance Overview")
    
    # Row 1: Key Metrics
    m1, m2, m3 = st.columns(3)
    
    over_by = max(today_spent - daily_safe, 0)
    
    m1.metric("Daily Safe Spend", f"₹{daily_safe:,.2f}")
    m2.metric("Today Spent", f"₹{today_spent:,.2f}", 
              delta=f"₹{over_by:,.2f}" if over_by > 0 else None, 
              delta_color="inverse")
    m3.metric("Survival Time", f"{money_last_days} Days")

    st.divider()

    # Row 2: Survival Meter
    survival_percentage = 0
    if daily_safe > 0:
        survival_percentage = round(max((daily_safe - today_spent) / daily_safe * 100, 0), 2)
    
    st.write(f"**Survival Meter: {survival_percentage}%**")
    progress_color = "green" if survival_percentage > 50 else "orange" if survival_percentage > 20 else "red"
    st.progress(min(float(survival_percentage) / 100, 1.0))
    
    st.divider()
    
    # Row 3: Financial Health
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Money Remaining:** ₹{money_remaining:,.2f}")
    with c2:
        if over_by > 0:
            st.warning("Status: You have exceeded today's safe limit.")
        else:
            st.success("Status: You are within your budget today!")

def main():
    st.set_page_config(page_title="Month Survival", layout="wide")
    st.title("📊 Month Survival Dashboard")

    # 1. Session State Check
    daily_safe = st.session_state.get("Daily Safe Spend")
    available_money = st.session_state.get("Available Money")

    if daily_safe is None or available_money is None:
        st.warning("⚠️ Setup data not found. Please go to the **Setup** page to initialize your budget.")
        st.stop()

    # 2. Data Processing
    df = load_and_clean_data(FILE_PATH)
    
    today_spent = 0
    total_spent = 0
    
    if not df.empty:
        today = datetime.now().date()
        today_spent = df[df["Date"].dt.date == today]["Amount"].sum()
        total_spent = df["Amount"].sum()

    # 3. Calculations
    money_remaining = available_money - total_spent
    money_last_days = int(money_remaining / daily_safe) if daily_safe > 0 else 0

    # 4. UI Rendering
    display_metrics(daily_safe, today_spent, money_remaining, money_last_days)

    # 5. Data History
    if not df.empty:
        with st.expander("📝 View Recent Expenses"):
            st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()