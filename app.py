import streamlit as st

st.title("💰 MoneyQuest")
st.subheader("Will your money survive this month?")

if st.button("Start Survival Mode"):
    st.switch_page("Survive_Mode")

if st.button("+ Add Expense"):
    st.switch_page("Expense")