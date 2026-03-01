import streamlit as st



st.title(" Month Survival Dashboard ")



if "Daily Safe Spend" in st.session_state:
    st.metric("Daily Safe Spend", f"₹{st.session_state['Daily Safe Spend']}")

else: 
    st.write("Daily Safe Spend is not calulated yet")


st.write(" Survival Meter Bar" )


if "Available Money" in st.session_state and "Daily Safe Spend" in st.session_state:

    available = st.session_state["Available Money"]
    daily_safe = st.session_state["Daily Safe Spend"]
    days_remaining = st.session_state["Days Remaining"]
    current_daily_spend = st.session_state["Current Daily Spend"]


    if current_daily_spend > 0 and days_remaining > 0:
        survival_days = available / current_daily_spend
        survival_percentage = round((survival_days / days_remaining) * 100, 2)
    
    st.progress(min(int(survival_percentage), 100))
    st.write(" Survival percentage", survival_percentage,"%")