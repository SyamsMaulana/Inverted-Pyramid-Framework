import streamlit as st

st.set_page_config(page_title="RYL Protocol", page_icon="⚡", layout="centered")

st.title("⚡ RYL: Ran Your Life")
st.subheader("Sovereignty, Movement, and Grounded Community")

st.markdown("""
**The RYL Protocol** shifts your trajectory from passive endurance to active command. 
No fog of the void can dictate your day when anchored by micro-commitments and shared presence.
""")

tab1, tab2, tab3 = st.tabs(["Somatic Reset", "Daily Ledger", "Protocol Guide"])

with tab1:
    st.markdown("### Physical-Somatic Reset")
    step1 = st.checkbox("Changed clothes & stepped outside")
    step2 = st.checkbox("Hydration & joint mobility completed")
    step3 = st.checkbox("Engaged in shared movement session")
    if step1 and step2 and step3:
        st.success("Somatic baseline secured. You are actively running your life.")

with tab2:
    st.markdown("### Daily Habit Tracker")
    habit = st.text_input("Log today's physical anchor step:")
    if st.button("Record Step"):
        if habit:
            st.success(f"Locked in: '{habit}'. Trajectory updated.")
        else:
            st.warning("Please enter a valid micro-commitment.")

with tab3:
    st.markdown("### Core Pillars")
    st.markdown("- **Sovereignty Over Autonomy:** Taking back the wheel step by step.")
    st.markdown("- **Radical Free Access:** Zero financial barriers or administrative walls.")
    st.markdown("- **Post-Movement Grounding:** Authentic dialogue around the shared table.")

st.sidebar.markdown("### Status")
st.sidebar.info("Operational Status: Live & Active")
