from datetime import date

import streamlit as st

from database import add_hire, get_hires, get_store, update_hired_counts
from date_format import format_date
from navigation import hide_sidebar
from readiness import get_readiness
from status_badge import show_status_badge, show_summary_box
from ui import labeled_text, page_intro, show_headcount_cell, show_hires_table

st.set_page_config(page_title="NSO Readiness")
hide_sidebar()


def read_date(date_text):
    if not date_text:
        return date.today()
    return date.fromisoformat(date_text)


def hire_inputs(role, amount, key_prefix):
    hires = []
    if amount == 0:
        return hires

    with st.expander(f"New {role} hires", expanded=True):
        for i in range(amount):
            st.markdown(f"**{role} #{i + 1}**")
            name = st.text_input("Name", key=f"{key_prefix}_{i}_name")
            background = st.selectbox(
                "Background",
                ["Retail", "F&B", "Cafe", "None"],
                key=f"{key_prefix}_{i}_background",
            )
            start_date = None
            training_started = st.checkbox(
                "Training Started?",
                key=f"{key_prefix}_{i}_started",
            )
            if training_started:
                start_date = st.date_input(
                    "Training Start Date",
                    max_value="today",
                    key=f"{key_prefix}_{i}_start",
                )

            hires.append({
                "role": role,
                "name": name,
                "background": background,
                "start_date": start_date,
            })

    return hires


selected_store = st.session_state.get("selected_store")

if not selected_store:
    st.warning("Open a store from the All Stores page first.")
    st.stop()

store = get_store(selected_store)

if store is None:
    st.error("This store was not found.")
    st.stop()

top_col, back_col = st.columns([4, 1])
with top_col:
    page_intro(
        "Store Detail",
        store["store_name"],
        "Review opening readiness and add newly hired employees to the plan.",
    )
with back_col:
    st.write("")
    st.write("")
    if st.button("Back to Stores", use_container_width=True):
        st.switch_page("app.py")

with st.container(border=True):
    st.subheader("Store details")
    detail_1, detail_2, detail_3 = st.columns(3)
    with detail_1:
        labeled_text("Store", store["store_name"])
    with detail_2:
        labeled_text("Market", store["country"])
    with detail_3:
        labeled_text("Target Open", format_date(store["target_open"]))

with st.container(border=True):
    st.subheader("Headcount")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        show_headcount_cell("RGM", store["hired_rgm"], store["need_rgm"])
    with c2:
        show_headcount_cell("ARGM", store["hired_argm"], store["need_argm"])
    with c3:
        show_headcount_cell("Supervisor", store["hired_sup"], store["need_sup"])
    with c4:
        show_headcount_cell("Team Member", store["hired_tm"], store["need_tm"])

existing_hires = get_hires(store["store_name"])
readiness = get_readiness(store, existing_hires)

with st.container(border=True):
    st.subheader("Opening readiness")
    show_status_badge(readiness["status"])
    show_summary_box(readiness)
    with st.expander("Progress details"):
        for detail in readiness["details"]:
            st.write(detail)

if existing_hires:
    st.subheader("Current hires")
    show_hires_table(existing_hires)

st.subheader("Add more hired employees")
remaining_rgm = max(0, store["need_rgm"] - store["hired_rgm"])
remaining_argm = max(0, store["need_argm"] - store["hired_argm"])
remaining_sup = max(0, store["need_sup"] - store["hired_sup"])
remaining_tm = max(0, store["need_tm"] - store["hired_tm"])

a1, a2, a3, a4 = st.columns(4)
add_rgm = a1.selectbox("RGM", range(remaining_rgm + 1), key="add_rgm")
add_argm = a2.selectbox("ARGM", range(remaining_argm + 1), key="add_argm")
add_sup = a3.selectbox("Supervisor", range(remaining_sup + 1), key="add_sup")
add_tm = a4.selectbox("Team Member", range(remaining_tm + 1), key="add_tm")

new_hires = []
new_hires += hire_inputs("RGM", add_rgm, "new_rgm")
new_hires += hire_inputs("ARGM", add_argm, "new_argm")
new_hires += hire_inputs("Supervisor", add_sup, "new_sup")
new_hires += hire_inputs("Team Member", add_tm, "new_tm")

if st.button("Save New Hires", type="primary"):
    errors = []
    if add_rgm + add_argm + add_sup + add_tm == 0:
        errors.append("Choose at least one employee to add.")

    for hire in new_hires:
        if hire["name"] == "":
            errors.append("Every new hire needs a name.")
            break

    if errors:
        for error in errors:
            st.error(error)
    else:
        for hire in new_hires:
            add_hire(
                store["store_name"],
                hire["role"],
                hire["name"],
                hire["background"],
                hire["start_date"],
            )

        update_hired_counts(
            store["store_name"],
            store["hired_rgm"] + add_rgm,
            store["hired_argm"] + add_argm,
            store["hired_sup"] + add_sup,
            store["hired_tm"] + add_tm,
        )
        st.success("New hires saved.")
        st.rerun()
