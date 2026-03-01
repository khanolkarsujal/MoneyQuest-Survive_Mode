import streamlit as st
from datetime import datetime
import calendar

# --- SETTINGS & LOGIC ---
def get_days_remaining():
    """Calculates days left in the month, including today."""
    today = datetime.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    # We add 1 because if today is the 10th and the month has 30 days, 
    # there are 21 days of spending left (including today)
    days = (last_day - today.day) + 1
    return max(days, 1) # Ensure we never return 0 to avoid division errors

def calculate_daily_budget(available_money, days_left):
    """Core logic to determine the safe daily spend."""
    if days_left <= 0:
        return 0
    return round(available_money / days_left, 2)

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Monthly Setup", page_icon="⚙️", layout="centered")

st.title("⚙️ Budget Setup")
st.markdown("Set your financial boundaries for the remainder of the month.")

# --- INPUT SECTION ---
# We use columns to make the form look more organized
with st.container(border=True):
    st.subheader("Monthly Financials")
    
    col1, col2 = st.columns(2)
    with col1:
        # Load from session state if it exists, otherwise default to 0
        total_money = st.number_input(
            "Total Monthly Income (₹)", 
            min_value=0, 
            value=st.session_state.get("Total Money", 0),
            help="Total cash you have for this month."
        )
    with col2:
        fixed_expenses = st.number_input(
            "Fixed Expenses (₹)", 
            min_value=0, 
            value=st.session_state.get("Fixed Expenses", 0),
            help="Rent, bills, and other non-negotiable costs."
        )

    st.divider()
    
    # Calculate days remaining once
    days_left = get_days_remaining()
    st.info(f"📅 **Days Remaining in Month:** {days_left} (including today)")

# --- CALCULATION LOGIC ---
if st.button("✅ Initialize Budget", use_container_width=True):
    available = total_money - fixed_expenses
    
    if available < 0:
        st.error("🚨 **Error:** Fixed expenses exceed your total money. Please adjust your numbers.")
    elif total_money == 0:
        st.warning("⚠️ Please enter your total income to proceed.")
    else:
        daily_safe = calculate_daily_budget(available, days_left)

        # Store values in session state for use in Dashboard.py
        st.session_state["Daily Safe Spend"] = daily_safe
        st.session_state["Available Money"] = available
        st.session_state["Days Remaining"] = days_left
        st.session_state["Total Money"] = total_money
        st.session_state["Fixed Expenses"] = fixed_expenses

        # Display Result
        st.success("### Configuration Saved!")
        
        m1, m2 = st.columns(2)
        m1.metric("Available Pool", f"₹{available:,.2f}")
        m2.metric("Daily Safe Limit", f"₹{daily_safe:,.2f}")
        
        st.balloons()

# --- NAVIGATION ---
st.markdown("---")
if "Daily Safe Spend" in st.session_state:
    if st.button("📊 Go to Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
else:
    st.caption("Complete the setup above to unlock the dashboard.")