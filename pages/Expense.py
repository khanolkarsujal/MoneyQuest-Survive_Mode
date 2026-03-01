import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
FILE_PATH = "data.csv"
COLUMNS = ["Amount", "Category", "Date"]

def save_expense(amount, category):
    """Appends a single expense to the CSV file safely."""
    # Create the data record
    new_data = {
        "Amount": [amount],
        "Category": [category if category else "Other"],
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    df_new = pd.DataFrame(new_data)

    # Check if file exists to determine if we need to write the header
    file_exists = os.path.isfile(FILE_PATH) and os.path.getsize(FILE_PATH) > 0

    try:
        # mode='a' appends to the file instead of overwriting it
        # header=not file_exists only writes the header the very first time
        df_new.to_csv(FILE_PATH, mode='a', index=False, header=not file_exists)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# --- UI LOGIC ---
st.set_page_config(page_title="Add Expense", page_icon="💸")
st.title("💸 Add New Expense")

# Professional form layout
with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("Amount (₹)", min_value=0, step=1, help="Enter the total amount spent.")
    
    with col2:
        options = ["Food", "Transport", "Entertainment", "Utilities", "Shopping", "Other"]
        category = st.selectbox("Category", options, index=5)

    notes = st.text_input("Note (Optional)", placeholder="e.g. Lunch with friends")

    # Center the button
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        save_btn = st.button("🚀 Save Expense", use_container_width=True)

# --- ACTION LOGIC ---
if save_btn:
    if amount <= 0:
        st.warning("Please enter an amount greater than 0.")
    else:
        # Use our standardized function
        success = save_expense(amount, category)
        
        if success:
            st.balloons()
            st.success(f"Successfully recorded ₹{amount} for {category}!")
            
            # Optional: Show a quick summary of recent spending
            st.info("Tip: Go to the Dashboard to see your updated survival meter.")

# --- RECENT LOGS ---
if os.path.exists(FILE_PATH):
    with st.expander("View Recent Entries"):
        df_view = pd.read_csv(FILE_PATH)
        st.dataframe(df_view.tail(5), use_container_width=True)