from datetime import date
from html import escape

import streamlit as st

from database import add_hire, delete_hire, get_hires, get_store, sync_hired_counts, update_hire
from date_format import format_date
from navigation import hide_sidebar
from readiness import get_readiness
from status_badge import show_status_badge, show_summary_box
from ui import labeled_text, page_intro, show_headcount_cell

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


def option_index(options, value):
    if value in options:
        return options.index(value)
    return 0


ROLE_LIMIT_FIELDS = {
    "RGM": "need_rgm",
    "ARGM": "need_argm",
    "Supervisor": "need_sup",
    "Team Member": "need_tm",
}


def role_counts_without_hire(hires, hire_id):
    counts = {role: 0 for role in ROLE_LIMIT_FIELDS}
    for hire in hires:
        if hire["id"] == hire_id:
            continue
        counts[hire["role"]] = counts.get(hire["role"], 0) + 1
    return counts


def available_roles_for_hire(store, hires, hire):
    counts = role_counts_without_hire(hires, hire["id"])
    available = []
    for role, need_field in ROLE_LIMIT_FIELDS.items():
        has_open_seat = counts.get(role, 0) < store[need_field]
        if role == hire["role"] or has_open_seat:
            available.append(role)
    return available


def edit_hire_form(store, hires, hire):
    hire_id = hire["id"]
    roles = available_roles_for_hire(store, hires, hire)
    backgrounds = ["Retail", "F&B", "Cafe", "None"]

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="edit-panel-title">Edit employee</div>
            <div class="edit-panel-name">{escape(hire["name"])}</div>
            """,
            unsafe_allow_html=True,
        )
        with st.form(f"edit_hire_form_{hire_id}"):
            top_left, top_right = st.columns(2)
            with top_left:
                role = st.selectbox(
                    "Role",
                    roles,
                    index=option_index(roles, hire["role"]),
                    key=f"edit_{hire_id}_role",
                )
            with top_right:
                background = st.selectbox(
                    "Background",
                    backgrounds,
                    index=option_index(backgrounds, hire["background"]),
                    key=f"edit_{hire_id}_background",
                )

            name = st.text_input("Name", value=hire["name"], key=f"edit_{hire_id}_name")

            date_left, date_right = st.columns([1, 2])
            with date_left:
                training_started = st.checkbox(
                    "Training Started?",
                    value=hire["start_date"] is not None,
                    key=f"edit_{hire_id}_started",
                )
            start_date = None
            with date_right:
                if training_started:
                    start_date = st.date_input(
                        "Training Start Date",
                        value=read_date(hire["start_date"]) or date.today(),
                        max_value="today",
                        key=f"edit_{hire_id}_start",
                    )

            save_col, cancel_col, spacer = st.columns([1, 1, 4])
            save = save_col.form_submit_button(
                "Save",
                key=f"save_hire_{hire_id}",
                type="primary",
                icon=":material/check:",
                use_container_width=True,
            )
            cancel = cancel_col.form_submit_button(
                "Cancel",
                key=f"cancel_hire_{hire_id}",
                icon=":material/close:",
                use_container_width=True,
            )

    if save:
        if name.strip() == "":
            st.error("Employee name cannot be blank.")
            return
        counts = role_counts_without_hire(hires, hire_id)
        if counts.get(role, 0) >= store[ROLE_LIMIT_FIELDS[role]]:
            st.error(f"{role} is already fully staffed for this store.")
            return
        update_hire(hire_id, role, name.strip(), background, start_date)
        sync_hired_counts(hire["store_name"])
        st.session_state.edit_hire_id = None
        st.success("Employee updated.")
        st.rerun()

    if cancel:
        st.session_state.edit_hire_id = None
        st.rerun()


@st.dialog("Confirm remove employee")
def confirm_remove_employee(hire):
    st.markdown(
        f"""
        <div class="confirm-remove-copy">
            Remove <strong>{escape(hire["name"])}</strong> from this store's hiring plan?
        </div>
        <div class="confirm-remove-note">
            This will update the store headcount and readiness status immediately.
        </div>
        """,
        unsafe_allow_html=True,
    )
    remove_col, cancel_col = st.columns([1, 1])
    if remove_col.button(
        "Remove employee",
        key=f"confirm_remove_hire_{hire['id']}",
        type="primary",
        icon=":material/delete:",
        use_container_width=True,
    ):
        delete_hire(hire["id"])
        sync_hired_counts(hire["store_name"])
        st.session_state.remove_hire_id = None
        st.success("Employee removed.")
        st.rerun()
    if cancel_col.button(
        "Cancel",
        key=f"cancel_remove_hire_{hire['id']}",
        icon=":material/close:",
        use_container_width=True,
    ):
        st.session_state.remove_hire_id = None
        st.rerun()


def show_editable_hires(store, hires):
    st.html(
        """
        <div class="hires-table hires-table-shell">
            <div class="hires-grid hires-grid-header">
                <div>Role</div>
                <div>Employee</div>
                <div>Background</div>
                <div>Training Start</div>
                <div>Actions</div>
            </div>
        </div>
        """
    )

    for hire in hires:
        with st.container(border=True):
            role_col, name_col, background_col, start_col, actions_col = st.columns([1.2, 1.35, 1.2, 1.25, 0.8])
            with role_col:
                st.markdown(f"**{hire['role']}**")
            with name_col:
                st.markdown(f"**{hire['name']}**")
            with background_col:
                st.markdown(f"**{hire['background']}**")
            with start_col:
                if hire["start_date"]:
                    st.markdown(f"**{format_date(hire['start_date'])}**")
                else:
                    st.markdown('<span class="muted-cell">Not started</span>', unsafe_allow_html=True)
            with actions_col:
                edit_col, remove_col = st.columns([1, 1])
                if edit_col.button(
                    "Edit",
                    key=f"edit_hire_{hire['id']}",
                    help=f"Edit {hire['name']}",
                ):
                    st.session_state.edit_hire_id = hire["id"]
                    st.rerun()
                if remove_col.button(
                    "Remove",
                    key=f"remove_hire_{hire['id']}",
                    help=f"Remove {hire['name']}",
                ):
                    st.session_state.remove_hire_id = hire["id"]
                    st.rerun()

        if st.session_state.get("edit_hire_id") == hire["id"]:
            edit_hire_form(store, hires, hire)
        if st.session_state.get("remove_hire_id") == hire["id"]:
            confirm_remove_employee(hire)


selected_store = st.query_params.get("store") or st.session_state.get("selected_store")

if not selected_store:
    st.switch_page("app.py")
    st.stop()

st.session_state.selected_store = selected_store

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
    show_editable_hires(store, existing_hires)

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

        sync_hired_counts(store["store_name"])
        st.success("New hires saved.")
        st.rerun()
