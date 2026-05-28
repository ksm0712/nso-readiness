import streamlit as st


STATUS_COLORS = {
    "Ready": {
        "text": "#047857",
        "background": "#ecfdf5",
        "border": "#a7f3d0",
    },
    "On Track": {
        "text": "#b45309",
        "background": "#fffbeb",
        "border": "#fde68a",
    },
    "Behind": {
        "text": "#b91c1c",
        "background": "#fef2f2",
        "border": "#fecaca",
    },
}


def show_status_badge(status):
    colors = STATUS_COLORS[status]
    st.markdown(
        f"""
        <div style="
            display: inline-block;
            padding: 5px 11px;
            border-radius: 999px;
            border: 1px solid {colors["border"]};
            background: {colors["background"]};
            color: {colors["text"]};
            font-size: 12px;
            font-weight: 800;
            letter-spacing: .04em;
            text-transform: uppercase;
            margin: 4px 0 8px 0;
        ">
            {status}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_summary_box(readiness):
    colors = STATUS_COLORS[readiness["status"]]
    st.markdown(
        f"""
        <div style="
            border: 1px solid {colors["border"]};
            border-left: 5px solid {colors["text"]};
            background: #ffffff;
            color: #334155;
            padding: 13px 14px;
            border-radius: 8px;
            line-height: 1.45;
            margin: 4px 0 16px 0;
            font-size: 14px;
        ">
            {readiness["summary"]}
        </div>
        """,
        unsafe_allow_html=True,
    )
