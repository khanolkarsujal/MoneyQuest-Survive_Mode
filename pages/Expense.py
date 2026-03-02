import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# --- 1. PAGE CONFIG (Consistent Icon: Compass) ---
st.set_page_config(page_title="Log Expense", page_icon="🧭", layout="centered")

# --- CONFIGURATION ---
FILE_PATH = "data.csv"
COLUMNS = ["Amount", "Category", "Date"]

# --- DATA ENGINE ---
def save_expense(amount, category):
    """Appends a single expense to data.csv without loading the whole file."""
    new_data = {
        "Amount": [amount],
        "Category": [category],
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    df_new = pd.DataFrame(new_data)

    # Check if file exists to decide if we need a header
    file_exists = os.path.isfile(FILE_PATH) and os.path.getsize(FILE_PATH) > 0

    try:
        # mode='a' is the professional way to append data (fast and safe)
        df_new.to_csv(FILE_PATH, mode='a', index=False, header=not file_exists)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# --- UI HEADER ---
st.title("🧭 Log an Expense")
st.caption("Quickly record your spending to stay on track.")

# --- INPUT SECTION (Minimalist Box) ---
with st.container(border=True):
    # We use a form to prevent double-submitting on page refresh
    with st.form("expense_form", clear_on_submit=True):
        st.subheader("💸 Quick Entry")
        
        amount = st.number_input(
            "Amount (₹)", 
            min_value=0, 
            step=10, 
            help="HINT: How much did you just spend?"
        )
        
        options = ["Food & Drinks", "Transport", "Stationery", "Rent/Bills", "Shopping", "Entertainment", "Other"]
        category = st.selectbox(
            "Category", 
            options, 
            index=0,
            help="HINT: Categorizing helps you see where your money goes."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        save_btn = st.form_submit_button("🚀 Record Expense", use_container_width=True)

    # --- ACTION LOGIC ---
    if save_btn:
        if amount <= 0:
            st.warning("⚠️ Please enter an amount greater than 0.")
        else:
            if save_expense(amount, category):
                st.toast(f"Saved: ₹{amount} for {category} ✅")
                st.success(f"Done! ₹{amount} logged.")
                # Small pause to let the user see the success before the UI resets
                time.sleep(1) 
                # This ensures the 'survival meter' updates in the background
                st.info("Survival Meter updated. Check the Dashboard!")

# --- NAVIGATION & HISTORY ---
st.divider()

col_a, col_b = st.columns(2)
with col_a:
    st.write("#### 🧭 Shortcuts")
    if st.button("📊 View Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Main.py")

with col_b:
    with st.expander("📝 View Today's Logs"):
        if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
            df_view = pd.read_csv(FILE_PATH)
            # Standardize column naming just in case
            df_view.columns = df_view.columns.str.strip().str.title()
            # Show last 5, newest first
            st.dataframe(df_view.tail(5).iloc[::-1], use_container_width=True, hide_index=True)
        else:
            st.write("No logs yet.")

# --- FOOTER ---
st.markdown("---")
st.caption("MoneyQuest | Making sure you don't run out of money. 🍕")