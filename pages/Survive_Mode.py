import streamlit as st
from  datetime import datetime
import calendar

today = datetime.today()

last_day = calendar.monthrange(today.year, today.month)[1]
days_remaining = last_day - today.day 


def survive_mode(Available, days_remaining):
    if days_remaining > 0:
        return round(Available / days_remaining, 2)
    else:
        return 0        


st.title("Setup Your Month ")

total_money = st.number_input("Total Money: ", min_value=0)

fixed_expenses = st.number_input("Fixed Expenses: ", min_value=0)

current_daily_spend = st.number_input("Current Daily Spending", min_value=0) 

st.write('Days Remaining:  ',days_remaining)


if st.button("Calculate Survival"): 

    Available = total_money - fixed_expenses

    if Available < 0:
        st.error("Fixed expenses cannot be greater than total money.")
    else:
        calculate_survival = survive_mode(Available, days_remaining)

        st.session_state["Daily Safe Spend"] = calculate_survival
        st.session_state["Available Money"] = Available
        st.session_state["Days Remaining"] = days_remaining
        st.session_state["Current Daily Spend"] = current_daily_spend


        st.write('You can spend ₹', calculate_survival, 'per day to survive.')

