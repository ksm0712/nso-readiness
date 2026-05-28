import streamlit as st

st.title("New Store - Manager Form")
store_name = st.text_input("Store Name")
country = st.selectbox("Country", ["Malaysia", "Indonesia", "Philippines", "Thailand", "Singapore"])
target_open = st.date_input("Target Opening Date")
rgm_needed = st.number_input("RGM Needed", min_value=0, step=1)
argm_needed = st.number_input("ARGM Needed", min_value=0, step=1)
supervisor_needed = st.number_input("Supervisor Needed", min_value=0, step=1)
members_needed = st.number_input("Team Members Needed", min_value=0, step=1)