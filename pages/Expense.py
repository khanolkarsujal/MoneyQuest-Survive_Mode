import streamlit as st
import pandas as pd
import os
from datetime import datetime

file_path = "data.csv"

st.title("Add Expense")

amount = st.number_input("Amount: ", min_value=0, step=1)
options = ["", "Food", "Transport", "Entertainment", "Utilities", "Other Expenses"]
category = st.selectbox("Category (Optional)", options)

if st.button("Save"):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=["Amount", "Category", "Timestamp"])

    new_row = {
        "Amount": amount,
        "Category": category,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(file_path, index=False)
    st.success("Saved successfully!")