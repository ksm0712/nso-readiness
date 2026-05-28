from datetime import date
from html import escape

import streamlit as st

from database import get_all_stores, get_hires, init_db
from date_format import format_date
from navigation import hide_sidebar
from readiness import get_readiness
from status_badge import show_status_badge, show_summary_box
from ui import labeled_text, page_intro, section_title


st.set_page_config(page_title="NSO Readiness")
hide_sidebar()
init_db()

STATUS_ORDER = {
    "Behind": 0,
    "On Track": 1,
    "Ready": 2,
}


def read_date(date_text):
    if not date_text:
        return date.today()
    return date.fromisoformat(date_text)


def _days_label(days):
    if days < 0:
        n = -days
        return f"Opened {n} day{'s' if n != 1 else ''} ago"
    if days == 0:
        return "Opens today"
    if days == 1:
        return "Opens tomorrow"
    return f"Opens in {days} day{'s' if days != 1 else ''}"


def show_executive_summary(items):
    today = date.today()
    behind = sorted(
        [item for item in items if item["readiness"]["status"] == "Behind"],
        key=lambda item: item["target_open"],
    )
    watching = sorted(
        [
            item for item in items
            if item["readiness"]["status"] == "On Track"
            and 0 <= (item["target_open"] - today).days <= 60
        ],
        key=lambda item: item["target_open"],
    )

    if not behind and not watching:
        return

    if behind:
        n = len(behind)
        hl = f"{n} store{'s' if n > 1 else ''} {'are' if n > 1 else 'is'} behind and need{'s' if n == 1 else ''} immediate attention."
        if watching:
            w = len(watching)
            hl += f"  {w} more opening within 60 days."
        hl_color = "#b91c1c"
        hl_bg = "#fff5f5"
        hl_border = "#fecaca"
    else:
        w = len(watching)
        hl = f"No stores are behind. {w} store{'s' if w > 1 else ''} opening within 60 days — monitor closely."
        hl_color = "#b45309"
        hl_bg = "#fffbeb"
        hl_border = "#fde68a"

    rows_html = []

    for item in behind:
        store = item["store"]
        readiness = item["readiness"]
        days = (item["target_open"] - today).days
        rows_html.append(
            f'<div style="display:flex;align-items:flex-start;border-left:4px solid #dc2626;background:#fef9f9;border-radius:0 8px 8px 0;padding:13px 15px;margin-bottom:10px;">'
            f'<div style="flex:1;min-width:0;">'
            f'<div style="display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:5px;">'
            f'<span style="background:#fef2f2;border:1px solid #fecaca;color:#b91c1c;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border-radius:999px;">Behind</span>'
            f'<span style="font-size:15px;font-weight:800;color:#111827;">{escape(store["store_name"])}</span>'
            f'<span style="color:#94a3b8;font-size:13px;">·</span>'
            f'<span style="color:#475569;font-size:13px;font-weight:600;">{escape(store["country"])}</span>'
            f'<span style="margin-left:auto;font-size:12px;font-weight:800;color:#dc2626;white-space:nowrap;">{_days_label(days)}</span>'
            f'</div>'
            f'<div style="color:#334155;font-size:13px;line-height:1.55;">{escape(readiness["summary"])}</div>'
            f'</div></div>'
        )

    if watching:
        watch_rows = []
        for item in watching:
            store = item["store"]
            days = (item["target_open"] - today).days
            watch_rows.append(
                f'<div style="display:flex;align-items:center;gap:10px;padding:10px 15px;border-left:4px solid #d97706;background:#fffdf7;border-radius:0 8px 8px 0;margin-bottom:10px;">'
                f'<span style="background:#fffbeb;border:1px solid #fde68a;color:#b45309;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border-radius:999px;white-space:nowrap;">On Track</span>'
                f'<span style="font-size:14px;font-weight:800;color:#111827;">{escape(store["store_name"])}</span>'
                f'<span style="color:#94a3b8;font-size:13px;">·</span>'
                f'<span style="color:#475569;font-size:13px;font-weight:600;">{escape(store["country"])}</span>'
                f'<span style="margin-left:auto;font-size:12px;font-weight:700;color:#b45309;white-space:nowrap;">{_days_label(days)}</span>'
                f'</div>'
            )
        section_label = "Also Opening Within 60 Days" if behind else "Opening Within 60 Days — Monitor Closely"
        top_margin = "14px" if behind else "0"
        rows_html.append(
            f'<div style="font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#64748b;margin:{top_margin} 0 8px 0;">{section_label}</div>'
            + "".join(watch_rows)
        )

    rows_joined = "".join(rows_html)
    st.html(
        f'<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;box-shadow:0 10px 28px rgba(15,23,42,0.06);margin:24px 0 4px 0;overflow:hidden;">'
        f'<div style="background:{hl_bg};border-bottom:1px solid {hl_border};padding:14px 20px;">'
        f'<div style="color:#64748b;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;margin-bottom:5px;">Executive Summary</div>'
        f'<div style="color:{hl_color};font-size:15px;font-weight:800;line-height:1.4;">{hl}</div>'
        f'</div>'
        f'<div style="padding:16px 16px 6px 16px;">{rows_joined}</div>'
        f'</div>'
    )


header_col, action_col = st.columns([4, 1])
with header_col:
    page_intro(
        "People Readiness",
        "Store Opening Dashboard",
        "Track hiring, training completion, and launch risk across upcoming stores.",
    )
with action_col:
    st.write("")
    st.write("")
    if st.button("Add New Store", type="primary", use_container_width=True):
        st.switch_page("pages/1_New_Store.py")

stores = get_all_stores()
store_readiness = []
for store in stores:
    readiness = get_readiness(store, get_hires(store["store_name"]))
    store_readiness.append({
        "store": store,
        "readiness": readiness,
        "target_open": read_date(store["target_open"]),
    })

if not stores:
    st.info("No stores yet. Add one using the button above.")
else:
    ready_count = sum(1 for item in store_readiness if item["readiness"]["status"] == "Ready")
    on_track_count = sum(1 for item in store_readiness if item["readiness"]["status"] == "On Track")
    behind_count = sum(1 for item in store_readiness if item["readiness"]["status"] == "Behind")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Stores", len(stores))
    m2.metric("Ready", ready_count)
    m3.metric("On Track", on_track_count)
    m4.metric("Behind", behind_count)

    show_executive_summary(store_readiness)

    countries = sorted({item["store"]["country"] for item in store_readiness})

    section_title("Store Portfolio")

    status_options = ["All", "Behind", "On Track", "Ready"]
    country_options = ["All"] + countries
    with st.container(border=True):
        f_left, f_right = st.columns([1, 2])
        with f_left:
            st.pills("Readiness", status_options, key="status_filter", selection_mode="single", default="All")
        with f_right:
            st.pills("Market", country_options, key="country_filter", selection_mode="single", default="All")

    status_filter = st.session_state.get("status_filter") or "All"
    country_filter = st.session_state.get("country_filter") or "All"

    filtered_stores = []
    for item in store_readiness:
        store = item["store"]
        readiness = item["readiness"]

        if status_filter != "All" and readiness["status"] != status_filter:
            continue
        if country_filter != "All" and store["country"] != country_filter:
            continue

        filtered_stores.append(item)

    filtered_stores.sort(
        key=lambda item: (
            STATUS_ORDER[item["readiness"]["status"]],
            item["target_open"],
            item["store"]["store_name"],
        )
    )

    if not filtered_stores:
        st.info("No stores match these filters.")

    for item in filtered_stores:
        store = item["store"]
        readiness = item["readiness"]
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
