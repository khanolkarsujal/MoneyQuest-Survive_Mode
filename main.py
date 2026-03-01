import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 

st.title("MoneyQuest")

st.subheader("Will your money survive?")


if st.button("Start Survival Mode"):
    st.switch_page("pages/Survive_Mode.py")



