import streamlit as st
import pandas as pd 

st.title("💰 MoneyQuest")
st.subheader("Will your money survive this month?")

if st.button("Start Survival Mode"):
    st.switch_page("pages/Survive_Mode.py")

if st.button("+ Add Expense"):
    st.switch_page("pages/Expense.py")  