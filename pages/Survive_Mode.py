import streamlit as st

st.title("Setup Your Month ")

total_money = st.number_input("Total Money: ", min_value=0)
st.write('$',total_money)

fixed_expenses = st.number_input("Fixed Expenses:", min_value=0)
st.write('$',fixed_expenses)

days_remaining = 30
st.write('Days Remaining:  ',days_remaining)


calculate_survival = int(total_money/days_remaining)
st.session_state["Daily Safe Spend"]  = calculate_survival


st.write('Daily Safe Spend: ',calculate_survival )

