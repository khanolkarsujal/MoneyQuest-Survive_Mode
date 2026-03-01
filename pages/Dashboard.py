import streamlit as st



st.title(" Month Survival Dashboard ")



if "Daily Safe Spend" in st.session_state:
    st.write('Daily Safe Spend: ',st.session_state["Daily Safe Spend"] )

else: 
    st.write("Daily Safe Spend is not calulated yet")


st.write(" Survival Meter Bar" )

         