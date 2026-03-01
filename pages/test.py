import streamlit as st
import plotly.graph_objects as go

survival_percentage = 78

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=survival_percentage,
    title={'text': "Survival Meter"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "green"}
    }
))

st.plotly_chart(fig)