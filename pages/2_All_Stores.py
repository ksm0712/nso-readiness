import streamlit as st
from database import get_all_stores

st.title("All Stores")

stores = get_all_stores()

if not stores:
    st.info("No stores yet. Add one from the New Store page.")
else:
    for store in stores:
        st.subheader(store["store_name"])
        st.write(f"Country: {store['country']}  |  Opens: {store['target_open']}")