import streamlit as st
from database import get_all_stores

st.title("All Stores")

stores = get_all_stores()

if not stores:
    st.info("No stores yet. Add one from the New Store page.")
else:
    cols_per_row = 3
    for i in range(0, len(stores), cols_per_row):
        row_stores = stores[i:i + cols_per_row]   # this row's batch of stores
        cols = st.columns(cols_per_row)
        for col, store in zip(cols, row_stores):
            with col:
                with st.container(border=True):
                    st.markdown(f"### {store['store_name']}")
                    st.write(f"📍 {store['country']}")
                    st.write(f"🗓️ Opens {store['target_open']}")
                    if st.button("Open", key=f"open_{store['store_name']}", use_container_width=True):
                        st.session_state.selected_store = store["store_name"]
                        st.switch_page("pages/3_Store_Detail.py")