import streamlit as st
from database import get_all_stores, get_hires
from date_format import format_date
from navigation import hide_sidebar
from readiness import get_readiness
from status_badge import show_status_badge, show_summary_box
from ui import labeled_text, page_intro, section_title


hide_sidebar()
page_intro(
    "People Readiness",
    "All Stores",
    "Track hiring, training completion, and opening risk across stores.",
)

stores = get_all_stores()

if not stores:
    st.info("No stores yet. Add one from the New Store page.")
else:
    section_title("Store Portfolio")
    for store in stores:
        readiness = get_readiness(store, get_hires(store["store_name"]))
        with st.container(border=True):
            name_col, market_col, date_col, status_col, summary_col, action_col = st.columns([2, 1.2, 1.4, 1.2, 3, 1])
            with name_col:
                st.markdown(f"### {store['store_name']}")
            with market_col:
                labeled_text("Market", store["country"])
            with date_col:
                labeled_text("Target Open", format_date(store["target_open"]))
            with status_col:
                show_status_badge(readiness["status"])
            with summary_col:
                show_summary_box(readiness)
            with action_col:
                st.write("")
                if st.button("Open", key=f"open_{store['store_name']}", use_container_width=True):
                    st.session_state.selected_store = store["store_name"]
                    st.switch_page("pages/3_Store_Detail.py")
