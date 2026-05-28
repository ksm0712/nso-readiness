import streamlit as st
from database import init_db, store_exists, add_store, add_hire
from navigation import hide_sidebar
from ui import page_intro


st.set_page_config(page_title="NSO Readiness")
init_db()
hide_sidebar()

top_col, back_col = st.columns([4, 1])
with top_col:
    page_intro(
        "New Store Setup",
        "Create Store Opening Plan",
        "Add the store profile, required staffing levels, and any employees already hired.",
    )
with back_col:
    st.write("")
    st.write("")
    if st.button("Back to Stores", use_container_width=True):
        st.switch_page("app.py")

store_name = st.text_input("Store Name")
country = st.selectbox("Country", ["Malaysia", "Indonesia", "Philippines", "Thailand", "Singapore"])
target_open = st.date_input("Target Opening Date")

st.subheader("Headcount needed")
c1, c2, c3, c4 = st.columns(4)
need_rgm = c1.selectbox("RGM", range(51), key="need_rgm")
need_argm = c2.selectbox("ARGM", range(51), key="need_argm")
need_sup = c3.selectbox("Supervisor", range(51), key="need_sup")
need_tm = c4.selectbox("Team Member", range(51), key="need_tm")

st.subheader("Hired so far")
h1, h2, h3, h4 = st.columns(4)
hired_rgm = h1.selectbox("RGM", range(need_rgm + 1), key="hired_rgm")
hired_argm = h2.selectbox("ARGM", range(need_argm + 1), key="hired_argm")
hired_sup = h3.selectbox("Supervisor", range(need_sup + 1), key="hired_sup")
hired_tm = h4.selectbox("Team Member", range(need_tm + 1), key="hired_tm")
rgm_list = []
if hired_rgm > 0:
    with st.expander(f"RGM Hires"):
        st.caption("Add each RGM's background and training start date below.")
        for i in range(hired_rgm):
            st.markdown(f"**RGM #{i+1}**")
            rgm_name = st.text_input("Name", key=f"rgm_{i+1}_name")
            rgm_bg = st.selectbox("Background", ["Retail", "F&B", "Cafe", "None"], key=f"rgm_{i+1}_bg")
            rgm_start_date = None
            rgm_started = st.checkbox("Training Started?", key=f"rgm_{i+1}_started")
            if rgm_started:
                rgm_start_date = st.date_input("Training Start Date", key=f"rgm_start_{i+1}", max_value="today")
            rgm_list.append({
                "role": "RGM",
                "name": rgm_name,
                "background": rgm_bg,
                "start_date": rgm_start_date
            })

argm_list = []
if hired_argm > 0:
    with st.expander(f"ARGM Hires"):
        st.caption("Add each ARGM's background and training start date below.")
        for i in range(hired_argm):
            st.markdown(f"**ARGM #{i+1}**")
            argm_name = st.text_input("Name", key=f"argm_{i+1}_name")
            argm_bg = st.selectbox("Background", ["Retail", "F&B", "Cafe", "None"], key=f"argm_{i+1}_bg")
            argm_start_date = None
            argm_started = st.checkbox("Training Started?", key=f"argm_{i+1}_started")
            if argm_started:
                argm_start_date = st.date_input("Training Start Date", key=f"argm_start_{i+1}", max_value="today")

            argm_list.append({
                "role": "ARGM",
                "name": argm_name,
                "background": argm_bg,
                "start_date": argm_start_date
            })

sup_list = []
if hired_sup > 0:
    with st.expander(f"Supervisor Hires"):
        st.caption("Add each Supervisor's background and training start date below.")
        for i in range(hired_sup):
            st.markdown(f"**Supervisor #{i+1}**")
            sup_name = st.text_input("Name", key=f"sup_{i+1}_name")
            sup_bg = st.selectbox("Background", ["Retail", "F&B", "Cafe", "None"], key=f"sup_{i+1}_bg")
            sup_start_date = None
            sup_started = st.checkbox("Training Started?", key=f"sup_{i+1}_started")
            if sup_started:
                sup_start_date = st.date_input("Training Start Date", key=f"sup_start_{i+1}", max_value="today")
            sup_list.append({
                "role": "Supervisor",
                "name": sup_name,
                "background": sup_bg,
                "start_date": sup_start_date
            })

tm_list = []
if hired_tm > 0:
    with st.expander(f"Team Member Hires"):
        st.caption("Add each Team Member's background and training start date below.")
        for i in range(hired_tm):
            st.markdown(f"**Team Member #{i+1}**")
            tm_name = st.text_input("Name", key=f"tm_{i+1}_name")
            tm_bg = st.selectbox("Background", ["Retail", "F&B", "Cafe", "None"], key=f"tm_{i+1}_bg")
            tm_start_date = None
            tm_started = st.checkbox("Training Started?", key=f"tm_{i+1}_started")
            if tm_started:
                tm_start_date = st.date_input("Training Start Date", key=f"tm_start_{i+1}", max_value="today")
            tm_list.append({
                "role": "Team Member",
                "name": tm_name,
                "background": tm_bg,
                "start_date": tm_start_date
            })

all_employees = rgm_list + argm_list + sup_list + tm_list

if st.button("Submit New Store", type="primary"):
    errors = []                                   
    if store_name == "":
        errors.append("Store name is required.")
    if need_rgm + need_argm + need_sup + need_tm == 0:
        errors.append("Enter how many staff are needed.")
    if store_name != "" and store_exists(store_name):
        errors.append("A store with this name already exists.")

    for emp in all_employees:
        if emp["name"] == "":
            errors.append("Every hire needs a name.")
            break                                 
   

    if errors:                                    
        for e in errors:
            st.error(e)
    else:
        add_store(store_name, country, target_open,
                  need_rgm, need_argm, need_sup, need_tm,
                  hired_rgm, hired_argm, hired_sup, hired_tm)
        for emp in all_employees:
            add_hire(store_name, emp["role"], emp["name"],
                     emp["background"], emp["start_date"])
        st.success(f"Store '{store_name}' created!")
        st.switch_page("app.py")
