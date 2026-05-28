from datetime import date

import pandas as pd
import streamlit as st

from database import add_hire, get_hires, get_store, update_hired_counts

COUNTRIES = ["Malaysia", "Indonesia", "Philippines", "Thailand", "Singapore"]


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
            training_started = st.toggle(
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

st.title(store["store_name"])

st.subheader("Store details")
st.text_input("Store Name", value=store["store_name"], disabled=True)
st.selectbox(
    "Country",
    COUNTRIES,
    index=COUNTRIES.index(store["country"]) if store["country"] in COUNTRIES else 0,
    disabled=True,
)
st.date_input(
    "Target Opening Date",
    value=read_date(store["target_open"]),
    disabled=True,
)

st.subheader("Headcount needed")
c1, c2, c3, c4 = st.columns(4)
c1.number_input("RGM", value=store["need_rgm"], disabled=True)
c2.number_input("ARGM", value=store["need_argm"], disabled=True)
c3.number_input("Supervisor", value=store["need_sup"], disabled=True)
c4.number_input("Team Member", value=store["need_tm"], disabled=True)

st.subheader("Hired so far")
h1, h2, h3, h4 = st.columns(4)
h1.number_input("RGM", value=store["hired_rgm"], disabled=True)
h2.number_input("ARGM", value=store["hired_argm"], disabled=True)
h3.number_input("Supervisor", value=store["hired_sup"], disabled=True)
h4.number_input("Team Member", value=store["hired_tm"], disabled=True)

existing_hires = get_hires(store["store_name"])
if existing_hires:
    st.subheader("Current hires")
    st.dataframe(pd.DataFrame(existing_hires), use_container_width=True)

st.subheader("Add more hired employees")
remaining_rgm = max(0, store["need_rgm"] - store["hired_rgm"])
remaining_argm = max(0, store["need_argm"] - store["hired_argm"])
remaining_sup = max(0, store["need_sup"] - store["hired_sup"])
remaining_tm = max(0, store["need_tm"] - store["hired_tm"])

a1, a2, a3, a4 = st.columns(4)
add_rgm = a1.number_input("RGM", min_value=0, max_value=remaining_rgm, step=1, key="add_rgm")
add_argm = a2.number_input("ARGM", min_value=0, max_value=remaining_argm, step=1, key="add_argm")
add_sup = a3.number_input("Supervisor", min_value=0, max_value=remaining_sup, step=1, key="add_sup")
add_tm = a4.number_input("Team Member", min_value=0, max_value=remaining_tm, step=1, key="add_tm")

new_hires = []
new_hires += hire_inputs("RGM", add_rgm, "new_rgm")
new_hires += hire_inputs("ARGM", add_argm, "new_argm")
new_hires += hire_inputs("Supervisor", add_sup, "new_sup")
new_hires += hire_inputs("Team Member", add_tm, "new_tm")

if st.button("Save New Hires"):
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
