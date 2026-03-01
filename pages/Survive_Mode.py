import streamlit as st
from  datetime import datetime
import calendar

today = datetime.today()

last_day = calendar.monthrange(today.year, today.month)[1]
days_remaining = last_day - today.day 


def survive_mode(remaining_money , days_remaining):

    return remaining_money /days_remaining


st.title("Setup Your Month ")

total_money = st.number_input("Total Money: ₹____ ", min_value=0)

fixed_expenses = st.number_input("Fixed Expenses: ₹____", min_value=0)

st.write('Days Remaining:  ',days_remaining)


if st.button("Calculate Survival"): 

    calculate_survival = survive_mode(total_money-fixed_expenses, days_remaining)

    st.session_state["Daily Safe Spend"]  = calculate_survival


    st.write('Daily Safe Spend: ',calculate_survival )

