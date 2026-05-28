import streamlit as st
from html import escape

from date_format import format_date


def apply_app_style():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"],
            [data-testid="collapsedControl"],
            [data-testid="stHeader"] {
                display: none;
            }

            .stApp {
                background: #f5f7fb;
                color: #172033;
                font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }

            .block-container {
                max-width: 1180px;
                padding-top: 36px;
                padding-bottom: 56px;
            }

            h1, h2, h3 {
                color: #111827;
                letter-spacing: 0;
            }

            h1 {
                font-size: 38px;
                font-weight: 800;
                margin-bottom: 4px;
            }

            h2, h3 {
                font-weight: 700;
            }

            p, label, span {
                font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }

            label,
            [data-testid="stWidgetLabel"],
            [data-testid="stWidgetLabel"] p {
                background: transparent !important;
                color: #334155 !important;
                font-weight: 700 !important;
            }

            [data-testid="stVerticalBlockBorderWrapper"] {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
                padding: 2px;
            }

            div.stButton > button {
                border-radius: 8px;
                border: 1px solid #cbd5e1;
                background: #ffffff;
                color: #0f172a;
                font-weight: 700;
                min-height: 42px;
            }

            div.stButton > button:hover {
                border-color: #2563eb;
                color: #1d4ed8;
                background: #eff6ff;
            }

            div.stButton > button[kind="primary"] {
                border: 1px solid #1d4ed8;
                background: #1d4ed8;
                color: #ffffff;
            }

            div.stButton > button[kind="primary"]:hover {
                border-color: #1e40af;
                background: #1e40af;
                color: #ffffff;
            }

            .st-key-add_new_store_button button {
                background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
                border: 1px solid #1d4ed8 !important;
                border-radius: 10px !important;
                box-shadow: 0 10px 22px rgba(37, 99, 235, 0.24) !important;
                color: #ffffff !important;
                font-size: 14px !important;
                font-weight: 800 !important;
                min-height: 44px !important;
            }

            .st-key-add_new_store_button button:hover {
                background: linear-gradient(135deg, #1e40af, #1d4ed8) !important;
                border-color: #1e40af !important;
                box-shadow: 0 12px 26px rgba(37, 99, 235, 0.30) !important;
                color: #ffffff !important;
            }

            [class*="st-key-edit_hire_"] button,
            [class*="st-key-remove_hire_"] button {
                align-items: center !important;
                border-radius: 999px !important;
                box-shadow: none !important;
                display: inline-flex !important;
                gap: 0 !important;
                height: 34px !important;
                justify-content: center !important;
                line-height: 1 !important;
                min-height: 34px !important;
                padding: 0 !important;
                position: relative !important;
                width: 34px !important;
            }

            [class*="st-key-edit_hire_"] button {
                background: #eff6ff !important;
                border: 1px solid #bfdbfe !important;
                color: #1d4ed8 !important;
            }

            [class*="st-key-edit_hire_"] button:hover {
                background: #dbeafe !important;
                border-color: #60a5fa !important;
                color: #1e40af !important;
            }

            [class*="st-key-remove_hire_"] button {
                background: #fef2f2 !important;
                border: 1px solid #fecaca !important;
                color: #dc2626 !important;
            }

            [class*="st-key-remove_hire_"] button:hover {
                background: #fee2e2 !important;
                border-color: #fca5a5 !important;
                color: #b91c1c !important;
            }

            [class*="st-key-edit_hire_"] button > *,
            [class*="st-key-remove_hire_"] button > * {
                display: none !important;
            }

            [class*="st-key-edit_hire_"] button::before,
            [class*="st-key-remove_hire_"] button::before {
                align-items: center !important;
                content: "";
                display: flex !important;
                font-family: "Material Symbols Rounded", "Material Symbols Outlined";
                font-size: 20px;
                font-style: normal;
                font-weight: 400;
                height: 20px !important;
                justify-content: center !important;
                letter-spacing: normal;
                line-height: 20px !important;
                margin: 0 !important;
                padding: 0 !important;
                text-transform: none;
                width: 20px !important;
            }

            [class*="st-key-edit_hire_"] button::before {
                content: "edit";
            }

            [class*="st-key-remove_hire_"] button::before {
                content: "delete";
            }

            [class*="st-key-confirm_remove_hire_"] button {
                background: #dc2626 !important;
                border-color: #dc2626 !important;
                color: #ffffff !important;
            }

            [class*="st-key-confirm_remove_hire_"] button:hover {
                background: #b91c1c !important;
                border-color: #b91c1c !important;
                color: #ffffff !important;
            }

            [class*="st-key-save_hire_"] button {
                background: #1d4ed8 !important;
                border-color: #1d4ed8 !important;
                color: #ffffff !important;
                font-weight: 800 !important;
            }

            [class*="st-key-save_hire_"] button:hover {
                background: #1e40af !important;
                border-color: #1e40af !important;
                color: #ffffff !important;
            }

            [class*="st-key-cancel_hire_"] button,
            [class*="st-key-cancel_remove_hire_"] button {
                background: #ffffff !important;
                border-color: #cbd5e1 !important;
                color: #334155 !important;
                font-weight: 800 !important;
            }

            [class*="st-key-cancel_hire_"] button:hover,
            [class*="st-key-cancel_remove_hire_"] button:hover {
                background: #f8fafc !important;
                border-color: #94a3b8 !important;
                color: #0f172a !important;
            }

            .edit-panel-title {
                color: #64748b;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: .08em;
                margin-bottom: 2px;
                text-transform: uppercase;
            }

            .edit-panel-name {
                color: #111827;
                font-size: 18px;
                font-weight: 800;
                margin-bottom: 14px;
            }

            .confirm-remove-copy {
                color: #111827;
                font-size: 16px;
                line-height: 1.45;
                margin-bottom: 8px;
            }

            .confirm-remove-note {
                background: #fef2f2;
                border: 1px solid #fecaca;
                border-radius: 8px;
                color: #991b1b;
                font-size: 13px;
                font-weight: 700;
                line-height: 1.45;
                margin-bottom: 16px;
                padding: 10px 12px;
            }

            [data-testid="stButtonGroup"] {
                margin-bottom: 2px;
            }

            [data-testid="stButtonGroup"] label p {
                color: #64748b !important;
                font-size: 11px;
                font-weight: 800 !important;
                letter-spacing: .08em;
                line-height: 1.1;
                margin-bottom: 8px;
                text-transform: uppercase;
            }

            [data-testid="stBaseButton-pills"],
            [data-testid="stBaseButton-pillsActive"] {
                border-radius: 999px !important;
                min-height: 34px !important;
                padding: 6px 12px !important;
                font-size: 13px !important;
                font-weight: 800 !important;
                box-shadow: none !important;
            }

            .st-key-status_filter [data-baseweb="button-group"] button:nth-of-type(2) {
                background: #fef2f2 !important;
                border: 1px solid #fecaca !important;
                color: #b91c1c !important;
            }

            .st-key-status_filter [data-baseweb="button-group"] button:nth-of-type(2)[data-testid="stBaseButton-pillsActive"] {
                background: #fee2e2 !important;
                border: 1.5px solid #f87171 !important;
                color: #991b1b !important;
            }

            .st-key-status_filter [data-baseweb="button-group"] button:nth-of-type(3) {
                background: #fffbeb !important;
                border: 1px solid #fde68a !important;
                color: #b45309 !important;
            }

            .st-key-status_filter [data-baseweb="button-group"] button:nth-of-type(3)[data-testid="stBaseButton-pillsActive"] {
                background: #fef3c7 !important;
                border: 1.5px solid #fbbf24 !important;
                color: #92400e !important;
            }

            .st-key-status_filter [data-baseweb="button-group"] button:nth-of-type(4) {
                background: #ecfdf5 !important;
                border: 1px solid #a7f3d0 !important;
                color: #047857 !important;
            }

            .st-key-status_filter [data-baseweb="button-group"] button:nth-of-type(4)[data-testid="stBaseButton-pillsActive"] {
                background: #d1fae5 !important;
                border: 1.5px solid #34d399 !important;
                color: #065f46 !important;
            }

            [data-testid="stBaseButton-pills"] {
                border: 1px solid #cbd5e1 !important;
                background: #ffffff !important;
                color: #334155 !important;
            }

            [data-testid="stBaseButton-pills"]:hover {
                border-color: #2563eb !important;
                background: #eff6ff !important;
                color: #1d4ed8 !important;
            }

            [data-testid="stBaseButton-pillsActive"] {
                border: 1px solid #1d4ed8 !important;
                background: #dbeafe !important;
                color: #1e40af !important;
            }

            [data-testid="stBaseButton-pills"] p,
            [data-testid="stBaseButton-pillsActive"] p {
                margin: 0;
            }

            [data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 18px 18px 14px 18px;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
            }

            [data-testid="stMetricLabel"] {
                color: #64748b;
                font-weight: 700;
            }

            [data-testid="stMetricValue"] {
                color: #0f172a;
                font-weight: 800;
            }

            [data-testid="stTextInputRootElement"],
            [data-testid="stDateInput"] [data-baseweb="input"],
            [data-baseweb="select"] > div {
                border-radius: 8px;
                border: 1px solid #cbd5e1 !important;
                background: #ffffff !important;
                box-shadow: none !important;
                min-height: 42px;
            }

            [data-testid="stTextInputRootElement"]:focus-within,
            [data-testid="stDateInput"] [data-baseweb="input"]:focus-within,
            [data-baseweb="select"] > div:focus-within {
                border-color: #2563eb !important;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14) !important;
                outline: none !important;
            }

            [data-baseweb="base-input"] {
                border: 0 !important;
                background: transparent !important;
                box-shadow: none !important;
                min-height: 40px;
            }

            [data-testid="stTextInput"] input,
            [data-testid="stNumberInput"] input,
            [data-testid="stDateInput"] input {
                border: 0 !important;
                border-color: #cbd5e1 !important;
                background: #ffffff !important;
                color: #0f172a !important;
                caret-color: #1d4ed8 !important;
                box-shadow: none !important;
                outline: none !important;
                min-height: 38px;
            }

            [data-testid="stTextInput"] input:focus,
            [data-testid="stNumberInput"] input:focus,
            [data-testid="stDateInput"] input:focus {
                border: 0 !important;
                box-shadow: none !important;
                outline: none !important;
            }

            [data-baseweb="select"] svg,
            [data-testid="stDateInput"] svg {
                color: #475569 !important;
                fill: #475569 !important;
            }

            [data-baseweb="select"],
            [data-baseweb="select"] *,
            [data-baseweb="input"],
            [data-baseweb="input"] * {
                color: #0f172a !important;
            }

            [data-baseweb="select"] input,
            [data-baseweb="input"] input {
                color: #0f172a !important;
                -webkit-text-fill-color: #0f172a !important;
            }

            [data-baseweb="input"] [data-baseweb] {
                background: #ffffff !important;
            }

            [data-testid="stNumberInput"] button {
                background: #f8fafc !important;
                border-color: #cbd5e1 !important;
                color: #0f172a !important;
            }

            [data-testid="stExpander"] {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
            }

            [data-testid="stExpander"] details,
            [data-testid="stExpander"] summary {
                background: #ffffff !important;
                color: #172033 !important;
            }

            [data-testid="stExpander"] summary p {
                color: #172033 !important;
                font-weight: 800 !important;
            }

            [data-testid="stCheckbox"] label,
            [data-testid="stCheckbox"] p {
                color: #334155 !important;
                font-weight: 700 !important;
            }

            .eyebrow {
                color: #2563eb;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .08em;
                text-transform: uppercase;
                margin-bottom: 6px;
            }

            .page-subtitle {
                color: #64748b;
                font-size: 16px;
                line-height: 1.5;
                margin-bottom: 22px;
            }

            .store-meta {
                color: #111827;
                font-size: 20px;
                font-weight: 700;
                margin: 2px 0;
            }

            .card-label {
                color: #64748b;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: .08em;
                text-transform: uppercase;
                margin-bottom: 2px;
            }

            .section-title {
                color: #111827;
                font-size: 20px;
                font-weight: 800;
                margin: 26px 0 12px 0;
            }

            .section-rule {
                border-top: 1px solid #e2e8f0;
                margin: 18px 0 4px 0;
            }

            .filter-row {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 8px;
                margin: 8px 0 12px 0;
            }

            .filter-label {
                color: #64748b;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .08em;
                text-transform: uppercase;
                margin-right: 4px;
            }

            [data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-status_filter) {
                margin-bottom: 18px !important;
                padding: 18px 20px !important;
            }

            [data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-status_filter) [data-testid="stColumn"]:has(.st-key-country_filter) {
                border-left: 1px solid #e2e8f0;
                padding-left: 24px !important;
            }

            .filter-chip {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                border-radius: 999px;
                border: 1px solid #cbd5e1;
                background: #ffffff;
                color: #334155 !important;
                font-size: 13px;
                font-weight: 800;
                line-height: 1;
                padding: 8px 12px;
                text-decoration: none !important;
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
            }

            .filter-chip:hover {
                border-color: #2563eb;
                color: #1d4ed8 !important;
                background: #eff6ff;
            }

            .filter-chip-active {
                border-color: #1d4ed8;
                background: #dbeafe;
                color: #1e40af !important;
            }

            .status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                display: inline-block;
                background: #94a3b8;
            }

            .status-dot-behind {
                background: #dc2626;
            }

            .status-dot-on-track {
                background: #d97706;
            }

            .status-dot-ready {
                background: #059669;
            }

            .hires-table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                overflow: hidden;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                background: #ffffff;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
            }

            .hires-table-shell {
                border-bottom-left-radius: 0;
                border-bottom-right-radius: 0;
                box-shadow: none;
                margin-bottom: 8px;
            }

            .hires-grid {
                display: grid;
                grid-template-columns: 1.2fr 1.35fr 1.2fr 1.25fr 1fr;
                column-gap: 18px;
                align-items: center;
            }

            .hires-grid-header {
                background: #f8fafc;
                color: #475569;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .06em;
                padding: 13px 14px;
                text-transform: uppercase;
            }

            .hires-table th {
                background: #f8fafc;
                color: #475569;
                font-size: 12px;
                font-weight: 800;
                letter-spacing: .06em;
                text-transform: uppercase;
                text-align: left;
                padding: 13px 14px;
                border-bottom: 1px solid #e2e8f0;
            }

            .hires-table td {
                color: #172033;
                font-size: 14px;
                font-weight: 600;
                padding: 14px;
                border-bottom: 1px solid #eef2f7;
            }

            .hires-table tr:last-child td {
                border-bottom: none;
            }

            .muted-cell {
                color: #94a3b8;
                font-weight: 600;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_intro(eyebrow, title, subtitle):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def labeled_text(label, value):
    st.markdown(
        f"""
        <div class="card-label">{label}</div>
        <div class="store-meta">{value}</div>
        """,
        unsafe_allow_html=True,
    )


def show_headcount_cell(label, hired, needed):
    if needed == 0:
        color = "#94a3b8"
        display = "—"
    elif hired >= needed:
        color = "#047857"
        display = f"{hired} of {needed}"
    elif hired > 0:
        color = "#b45309"
        display = f"{hired} of {needed}"
    else:
        color = "#b91c1c"
        display = f"{hired} of {needed}"
    st.markdown(
        f"""
        <div class="card-label">{label}</div>
        <div style="font-size:22px;font-weight:800;color:{color};margin:3px 0 12px 0;">{display}</div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def show_filter_chips(label, options, active_value, param_name, other_params=None, dot_options=None):
    if other_params is None:
        other_params = {}
    if dot_options is None:
        dot_options = {}

    chips = [f'<span class="filter-label">{label}</span>']
    for option in options:
        params = other_params.copy()
        params[param_name] = option
        query = "&".join(f"{key}={value.replace(' ', '+')}" for key, value in params.items())
        active_class = " filter-chip-active" if option == active_value else ""
        dot_class = dot_options.get(option)
        dot = f'<span class="status-dot {dot_class}"></span>' if dot_class else ""
        chips.append(f'<a class="filter-chip{active_class}" href="?{query}">{dot}{option}</a>')

    st.markdown(
        f'<div class="filter-row">{"".join(chips)}</div>',
        unsafe_allow_html=True,
    )


def show_hires_table(hires):
    rows = []
    for hire in hires:
        start_date = format_date(hire["start_date"]) if hire["start_date"] else '<span class="muted-cell">Not started</span>'
        rows.append(
            f"""
            <tr>
                <td>{escape(hire["role"])}</td>
                <td>{escape(hire["name"])}</td>
                <td>{escape(hire["background"])}</td>
                <td>{start_date}</td>
            </tr>
            """
        )

    st.html(
        f"""
        <table class="hires-table">
            <thead>
                <tr>
                    <th>Role</th>
                    <th>Employee</th>
                    <th>Background</th>
                    <th>Training Start</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """
    )
