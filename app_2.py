import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
import streamlit.components.v1 as components
import html
import math

st.set_page_config(
    page_title="Virginia Housing Dashboard",
    page_icon="🏠",
    layout="wide"
)

# ---------------- GLOBAL CSS ---------------- 

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&display=swap');

    header {visibility: hidden;}


    .stApp {
        background: white;
        color: #202124;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    div[data-testid="stHorizontalBlock"] {
        background: #fafaf9 !important; 
        border-bottom: 1px solid #e7e7e7;
        align-items: center !important;
        gap: 4px !important;
        padding: 4px 12px !important;
    }

    div[data-testid="stHorizontalBlock"] > div {
        min-width: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:nth-of-type(2) {
        background: #fafaf9 !important;
        padding-top: 4px !important;
        padding-bottom: 4px !important;
    }


    .app-title {
        font-size: 15px;
        font-weight: 600;
        color: #1f2933;
        white-space: nowrap;
        line-height: 32px;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-top: -15px;
        padding-left: 20px;
    }

    .total {
        text-align: right;
        font-size: 12px;
        color: #5f6368;
        white-space: nowrap;
        line-height: 32px;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .total b {
        color: #202124;
        font-weight: 700;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stTextInput"] label {
        display: none !important;
    }

    div[data-testid="stTextInput"] input {
        font-family: "Littera Text Book", sans-serif !important;
        margin-top: 4px;
        height: 30px !important;
        width: 350px !important;
        min-height: 30px !important;
        border-radius: 999px !important;
        background: white !important;
        border: 1px solid #ddddd !important;
        color: #202124 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding-left: 18px !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #aaaaaa !important;
    }
    
    div[data-testid="stTextInput"] {
        position: relative;
        left: -80px;
    }

    div[data-baseweb="select"] > div {
        min-height: 32px !important;
        height: 32px !important;
        background: white !important;
        border: 1px solid #dedede !important;
        border-radius: 999px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
        padding-left: 10px !important;
        padding-right: 6px !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] div {
        color: #3c4043 !important;
        opacity: 1 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] input::placeholder {
        color: #3c4043 !important;
        opacity: 1 !important;
    }

    div[data-baseweb="select"] svg {
        color: #9aa0a6 !important;
        fill: #9aa0a6 !important;
        width: 14px !important;
        height: 14px !important;
    }

    ul[role="listbox"] {
        border-radius: 18px !important;
        box-shadow: 0 10px 24px rgba(0,0,0,0.14) !important;
        padding: 6px !important;
    }

    li[aria-selected="true"] {
        background: #202124 !important;
        border-radius: 12px !important;
    }

    li[aria-selected="true"] * {
        color: white !important;
    }

    button[kind="secondary"],
    button[kind="primary"] {
        border-radius: 999px !important;
        min-height: 32px !important;
        height: 32px !important;
        padding: 0 11px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        white-space: nowrap !important;
        min-width: 58px !important;
    }

    button[kind="secondary"] {
        background: white !important;
        color: #6f7275 !important;
        border: 1px solid #dedede !important;
    }

    button[kind="secondary"]:hover {
        background: white !important;
        color: #202124 !important;
        border-color: #cfcfcf !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    }

    button[kind="primary"] {
        background: #1f1f1f !important;
        color: white !important;
        border: 1px solid #1f1f1f !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }

    button[kind="primary"] * {
        color: white !important;
    }

    div[data-testid="stElementContainer"] {
        margin: 0 !important;
        padding-bottom: 0 !important;
    }

    div[data-testid="stForm"] {
        border: none !important;
    }

    /* Keep popover panels readable */
    div[data-testid="stPopover"] > div {
        min-width: 390px !important;
    }

    div[data-testid="stPopover"] div[data-testid="stHorizontalBlock"] {
        background: transparent !important;
        border-bottom: none !important;
        padding: 0 !important;
        gap: 10px !important;
    }

    div[data-testid="stPopover"] button[kind="secondary"],
    div[data-testid="stPopover"] button[kind="primary"] {
        min-height: 40px !important;
        height: 40px !important;
        font-size: 15px !important;
        padding: 0 16px !important;
        min-width: 110px !important;
    }

    .stDeployButton, footer {
        display: none !important;
    }

    /* Map Marker */
    
    div[data-testid="stElementContainer"]:has(.map-button-marker) {
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Move only the Map button */
    div[data-testid="stElementContainer"]:has(.map-button-marker)
    + div[data-testid="stElementContainer"] button {
        transform: translateX(-280px) !important;

        height: 30px !important;
        min-height: 30px !important;

        font-family: "DM Sans", sans-serif !important;
        font-size: 14px !important;
    }

    div[data-testid="stElementContainer"]:has(.map-button-marker)
    + div[data-testid="stElementContainer"] button * {
        font-family: "DM Sans", sans-serif !important;
        font-size: 14px !important;
    }

    /* Table Marker */

    div[data-testid="stElementContainer"]:has(.table-button-marker) {
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stElementContainer"]:has(.table-button-marker)
    + div[data-testid="stElementContainer"] button {
        transform: translateX(-310px) !important;

        height: 30px !important;
        min-height: 30px !important;

        font-family: "DM Sans", sans-serif !important;
        font-size: 14px !important;
    }

    div[data-testid="stElementContainer"]:has(.table-button-marker)
    + div[data-testid="stElementContainer"] button * {
        font-family: "DM Sans", sans-serif !important;
        font-size: 14px !important;
    }

        /* Stat Marker */

    div[data-testid="stElementContainer"]:has(.stat-button-marker) {
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stElementContainer"]:has(.stat-button-marker)
    + div[data-testid="stElementContainer"] button {
        transform: translateX(-350px) !important;

        height: 30px !important;
        min-height: 30px !important;

        font-family: "DM Sans", sans-serif !important;
        font-size: 14px !important;
    }

    div[data-testid="stElementContainer"]:has(.stat-button-marker)
    + div[data-testid="stElementContainer"] button * {
        font-family: "DM Sans", sans-serif !important;
        font-size: 14px !important;
    }


    /* ALL FILTER BUTTONS */

    div[data-testid="stPopover"] button {
        width: auto !important;
        min-width: 120px !important;

        height: 34px !important;
        min-height: 34px !important;

        padding: 0 10px !important;

        font-size: 13px !important;
        font-weight: 400 !important;

        border-radius: 999px !important;
    }

    div[data-testid="stPopover"] button * {
        font-size: 13px !important;
    }

    /* =========================
    Clusters Selectbox
    ========================= */

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        width: 110px !important;
        min-width: 110px !important;
        max-width: 110px !important;

        height: 40px !important;
        min-height: 40px !important;

        padding: 0 2px !important;

        border-radius: 999px !important;
        border: 1px solid #d6d6d6 !important;
        background: white !important;

        box-shadow: 0 1px 4px rgba(0,0,0,.06) !important;
    }

            /* Arrow container */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div:last-child {
        margin-right: 12px !important;
        padding-right: 0 !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        font-family: "DM Sans", sans-serif !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        color: #707174 !important;
    }

    /* Move ONLY the dropdown arrow left */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {
        width: 14px !important;
        height: 14px !important;

        transform: translateX(-8px) !important;
    }

    /* Price boxes */

    div[data-testid="stNumberInput"] label {
        display: none !important;
    }

    div[data-testid="stNumberInput"] input {
        height: 36px !important;

        border-radius: 999px !important;
        border: 1px solid #d6d6d6 !important;

        text-align: center !important;

        font-family: "DM Sans", sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    div[data-testid="stNumberInput"] {
        margin-top: 2px !important;
    }

    html, body, .stApp, p, div:not([data-testid="stIconMaterial"]), button, input, label {
        font-family: "DM Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }

    /* Keep Streamlit icons working */
    span[data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded" !important;
        font-weight: normal !important;
        font-style: normal !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data(ttl=86400)   # 24 hours
def load_data():
    return pd.read_csv("data/virginia_housing_raw.csv")

df = load_data()
original_df = df.copy()

if "page" not in st.session_state:
    st.session_state.page = "Map"

# ---------------- TOP BAR ----------------
title_col, search_col, map_col, table_col, stats_col, total_col = st.columns(
    [2.15, 3.95, 0.65, 0.70, 0.70, 1.55]
)

with title_col:
    st.markdown('<div class="app-title">🏠 Virginia Housing Tracker</div>', unsafe_allow_html=True)

with search_col:
    search_text = st.text_input(
        "Search",
        placeholder="Search city, county, or neighborhood...",
        key="search_text"
    )

with map_col:
    st.markdown('<span class="map-button-marker"></span>', unsafe_allow_html=True)

    if st.button(
        "Map",
        key="nav_map",
        type="primary" if st.session_state.page == "Map" else "secondary"
    ):
        st.session_state.page = "Map"
        st.rerun()

    with table_col:
        st.markdown('<div class="table-button-marker"></div>', unsafe_allow_html=True)

        if st.button(
            "Table",
            type="primary" if st.session_state.page == "Table" else "secondary"
        ):
            st.session_state.page = "Table"
            st.rerun()

with stats_col:
    st.markdown(
        '<div class="stat-button-marker"></div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Stats",
        key="nav_stats",
        type="primary" if st.session_state.page == "Stats" else "secondary"
    ):
        st.session_state.page = "Stats"
        st.rerun()

with total_col:
    st.markdown(f'<div class="total"><b>TOTAL</b> listings: <b>{len(original_df):,}</b></div>', unsafe_allow_html=True)

page = st.session_state.page

# ---------------- FILTER HELPERS ----------------
def multi_filter_popover(label, options, key, marker_class=None):
    """Scrollable multi-select filter with Clear and Apply buttons."""
    applied_key = key
    draft_key = f"{key}_draft"

    if applied_key not in st.session_state:
        st.session_state[applied_key] = []

    if draft_key not in st.session_state:
        st.session_state[draft_key] = list(st.session_state[applied_key])

    selected = st.session_state[applied_key]
    button_label = label if not selected else f"{label}: {len(selected)}"

    if marker_class:
        st.markdown(f'<div class="{marker_class}"></div>', unsafe_allow_html=True)

    # Important: keep use_container_width=False so the button does not stretch weirdly.
    with st.popover(f"{button_label}", use_container_width=False):
        st.markdown(f"### {label.upper()}")

        with st.container(height=280, border=True):
            draft_selection = []

            for option in options:
                checkbox_key = f"{key}_check_{str(option).replace(' ', '_')}"

                if checkbox_key not in st.session_state:
                    st.session_state[checkbox_key] = option in st.session_state[draft_key]

                checked = st.checkbox(
                    str(option),
                    key=checkbox_key
                )

                if checked:
                    draft_selection.append(option)

            st.session_state[draft_key] = draft_selection

        c1, c2 = st.columns(2, gap="small")

        with c1:
            if st.button("Clear", key=f"clear_{key}", use_container_width=True):
                st.session_state[applied_key] = []
                st.session_state[draft_key] = []

                for option in options:
                    checkbox_key = f"{key}_check_{str(option).replace(' ', '_')}"
                    if checkbox_key in st.session_state:
                        st.session_state[checkbox_key] = False

                st.rerun()

        with c2:
            if st.button("Apply", key=f"apply_{key}", type="primary", use_container_width=True):
                st.session_state[applied_key] = list(st.session_state[draft_key])
                st.rerun()

    return st.session_state[applied_key]


# ---------------- FILTER ROW ----------------
f1, f2, f3, f4, f5, price_col, spacer, f6 = st.columns(
    [0.60, 0.60, 0.60, 0.60, 0.75, 1.8, 1.8, 0.6]
)

with f1:
    selected_counties = multi_filter_popover(
        "County",
        sorted(df["county"].dropna().unique()),
        "selected_counties",
        marker_class="county-marker"
    )

with f2:
    selected_cities = multi_filter_popover(
        "City",
        sorted(df["city"].dropna().unique()),
        "selected_cities"
    )

with f3:
    selected_beds = multi_filter_popover(
        "Beds",
        [1, 2, 3, 4, 5, 6],
        "selected_beds"
    )

with f4:
    selected_baths = multi_filter_popover(
        "Baths",
        [1, 2, 3, 4, 5, 6],
        "selected_baths"
    )

with f5:
    map_mode = st.selectbox(
        "Style",
        ["Clusters", "Dots", "Heat"],
        key="map_mode"
    )

with price_col:

    price_min = int(original_df["list_price"].min())
    price_max = int(original_df["list_price"].max())

    if "price_min_input" not in st.session_state:
        st.session_state.price_min_input = price_min

    if "price_max_input" not in st.session_state:
        st.session_state.price_max_input = price_max

    c1, c2 = st.columns(2, gap="small")

    with c1:
        st.session_state.price_min_input = st.number_input(
            "Min",
            min_value=price_min,
            max_value=price_max,
            value=st.session_state.price_min_input,
            step=25000,
            format="%d",
            key="price_min_box",
        )

    with c2:
        st.session_state.price_max_input = st.number_input(
            "Max",
            min_value=price_min,
            max_value=price_max,
            value=st.session_state.price_max_input,
            step=25000,
            format="%d",
            key="price_max_box",
        )

    selected_price_range = (
        st.session_state.price_min_input,
        st.session_state.price_max_input,
    )

with f6:
    if st.button("× Clear", use_container_width=True):
        prefixes_to_clear = [
            "search_text",
            "selected_counties",
            "selected_cities",
            "selected_beds",
            "selected_baths",
            "price_range",
            "selected_counties_draft",
            "selected_cities_draft",
            "selected_beds_draft",
            "selected_baths_draft",
            "map_mode"
        ]

        for clear_key in list(st.session_state.keys()):
            if clear_key in prefixes_to_clear or clear_key.startswith((
                "selected_counties_check_",
                "selected_cities_check_",
                "selected_beds_check_",
                "selected_baths_check_"
            )):
                del st.session_state[clear_key]

        st.session_state.page = "Map"
        st.rerun()


# ---------------- APPLY FILTERS ----------------
if selected_counties:
    df = df[df["county"].isin(selected_counties)]

if selected_cities:
    df = df[df["city"].isin(selected_cities)]

if selected_beds and "beds" in df.columns:
    df = df[df["beds"].isin(selected_beds)]

if selected_baths and "full_baths" in df.columns:
    df = df[df["full_baths"].isin(selected_baths)]

if "list_price" in df.columns:
    df = df[
        (df["list_price"] >= selected_price_range[0]) &
        (df["list_price"] <= selected_price_range[1])
    ]

if search_text:
    search_text_lower = search_text.lower()
    mask = pd.Series(False, index=df.index)

    for col in ["city", "county", "neighborhood"]:
        if col in df.columns:
            mask = mask | df[col].astype(str).str.lower().str.contains(
                search_text_lower,
                na=False
            )

    df = df[mask]

# ---------------- COLORS ----------------
def price_color(price):
    if pd.isna(price):
        return "#6b7280"
    if price < 300000:
        return "#93c5fd"
    elif price < 600000:
        return "#3b82f6"
    elif price < 1000000:
        return "#1d4ed8"
    else:
        return "#0f172a"


def clean_value(value, default="Unknown"):
    if pd.isna(value):
        return default
    text = str(value).strip()
    if text.lower() in ["nan", "none", ""]:
        return default
    return text

def money_value(value):
    if pd.isna(value):
        return "Unknown"
    try:
        return f"${float(value):,.0f}"
    except Exception:
        return clean_value(value)

def number_value(value, default="Unknown"):
    if pd.isna(value):
        return default
    try:
        return f"{float(value):,.0f}"
    except Exception:
        return clean_value(value, default)

def short_text(value, max_chars=260):
    text = clean_value(value, "")
    if not text:
        return ""
    text = " ".join(text.split())
    return text if len(text) <= max_chars else text[:max_chars].rsplit(" ", 1)[0] + "..."

def make_home_popup(row):
    price = money_value(row.get("list_price"))
    address = clean_value(row.get("formatted_address"), "")
    if not address:
        street = clean_value(row.get("full_street_line"), "")
        city = clean_value(row.get("city"), "")
        state = clean_value(row.get("state"), "")
        zip_code = clean_value(row.get("zip_code"), "")
        address = ", ".join([x for x in [street, city, state, zip_code] if x and x != "Unknown"])

    city = clean_value(row.get("city"))
    county = clean_value(row.get("county"))
    status = clean_value(row.get("status"))
    beds = number_value(row.get("beds"))
    baths = number_value(row.get("full_baths"))
    sqft = number_value(row.get("sqft"))
    year_built = number_value(row.get("year_built"))
    days_on_mls = number_value(row.get("days_on_mls"))
    price_sqft = money_value(row.get("price_per_sqft"))
    hoa = money_value(row.get("hoa_fee"))
    lot_sqft = number_value(row.get("lot_sqft"))
    agent = clean_value(row.get("agent_name"), "")
    broker = clean_value(row.get("broker_name"), "")
    listing_text = short_text(row.get("text"), 120)

    url = clean_value(row.get("property_url"), "")
    if not url:
        url = clean_value(row.get("permalink"), "")

    safe_price = html.escape(price)
    safe_address = html.escape(address or "Address not available")
    safe_city_county = html.escape(f"{city}, {county} County")
    safe_status = html.escape(status.replace("_", " ").title())
    safe_agent = html.escape(agent)
    safe_broker = html.escape(broker)
    safe_text = html.escape(listing_text)

    detail_rows = [
        ("Beds", beds),
        ("Baths", baths),
        ("Sqft", sqft),
        ("$/Sqft", price_sqft),
        ("Year Built", year_built),
        ("Days on MLS", days_on_mls),
        ("Lot Sqft", lot_sqft),
        ("HOA", hoa),
    ]

    detail_html = ""
    for label, value in detail_rows:
        detail_html += f"""
        <div class="detail">
            <span>{html.escape(label)}</span>
            <b>{html.escape(str(value))}</b>
        </div>
        """

    agent_html = ""
    if agent or broker:
        agent_html = f"""
        <div class="section">
            <div class="section-title">Listing Contact</div>
            <div>{safe_agent}</div>
            <div class="muted">{safe_broker}</div>
        </div>
        """

    desc_html = ""
    if listing_text:
        desc_html = f"""
        <div class="section">
            <div class="section-title">Description</div>
            <div class="description">{safe_text}</div>
        </div>
        """

    link_html = ""
    if url and url != "Unknown":
        safe_url = html.escape(url, quote=True)
        link_html = f'<a class="open-link" href="{safe_url}" target="_blank">Open Listing</a>'

    popup_html = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            font-family: "DM Sans", Arial, sans-serif;
            color: #111827;
        }}
        .card {{
            width: 360px;
            padding: 18px 20px;
            border-radius: 18px;
            background: white;
        }}
        .price {{
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 6px;
        }}
        .address {{
            font-size: 15px;
            font-weight: 700;
            line-height: 1.35;
            margin-bottom: 4px;
        }}
        .muted {{
            color: #6b7280;
            font-size: 13px;
        }}
        .status {{
            display: inline-block;
            margin: 10px 0 12px 0;
            padding: 5px 11px;
            border-radius: 999px;
            background: #eef2ff;
            color: #3730a3;
            font-weight: 700;
            font-size: 12px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px 12px;
            margin-top: 8px;
        }}
        .detail {{
            border-bottom: 1px solid #eef0f2;
            padding-bottom: 6px;
            font-size: 13px;
        }}
        .detail span {{
            color: #6b7280;
            display: block;
        }}
        .detail b {{
            color: #111827;
            font-size: 14px;
        }}
        .section {{
            margin-top: 14px;
            font-size: 13px;
            line-height: 1.45;
        }}
        .section-title {{
            color: #6b7280;
            font-weight: 800;
            letter-spacing: .05em;
            text-transform: uppercase;
            font-size: 11px;
            margin-bottom: 4px;
        }}
        .description {{
            color: #374151;
        }}
        .open-link {{
            display: block;
            margin-top: 14px;
            text-align: center;
            background: #1f1f1f;
            color: white !important;
            text-decoration: none;
            border-radius: 999px;
            padding: 9px 14px;
            font-weight: 800;
            font-size: 14px;
        }}
    </style>
    </head>
    <body>
        <div class="card">
            <div class="price">{safe_price}</div>
            <div class="address">{safe_address}</div>
            <div class="muted">{safe_city_county}</div>
            <div class="status">{safe_status}</div>
            <div class="grid">{detail_html}</div>
            {agent_html}
            {desc_html}
            {link_html}
        </div>
    </body>
    </html>
    """
    iframe = folium.IFrame(html=popup_html, width=410, height=520)
    return folium.Popup(iframe, max_width=430)


# ---------------- MAP ----------------
if page == "Map":
    map_df = df.dropna(subset=["latitude", "longitude"]).copy()

    focus_home = st.session_state.get("focus_home")
    focused_property_id = focus_home.get("property_id") if focus_home else None

    if (
        focus_home
        and pd.notna(focus_home.get("lat"))
        and pd.notna(focus_home.get("lon"))
    ):
        map_location = [focus_home["lat"], focus_home["lon"]]
        map_zoom = 15
    else:
        map_location = [37.6, -78.2]
        map_zoom = 7

    m = folium.Map(
        location=map_location,
        zoom_start=map_zoom,
        tiles="CartoDB positron",
        control_scale=True,
        scrollWheelZoom=True,
        dragging=True,
        zoom_control=True
    )

    if map_mode == "Clusters":
        cluster = MarkerCluster().add_to(m)

        for _, row in map_df.iterrows():
            price = row.get("list_price", None)

            is_focused = (
                focused_property_id is not None
                and row.get("property_id") == focused_property_id
            )

            popup = make_home_popup(row)

            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=6,
                color="white",
                weight=1,
                fill=True,
                fill_color=price_color(price),
                fill_opacity=0.85,
                popup=popup
            ).add_to(cluster)

    elif map_mode == "Heat":
        heat_df = map_df.dropna(subset=["list_price"]).copy()

        if len(heat_df) > 0:
            price_cap = heat_df["list_price"].quantile(0.99)

            if price_cap and price_cap > 0:
                heat_df["weight"] = heat_df["list_price"].clip(upper=price_cap) / price_cap
            else:
                heat_df["weight"] = 1

            heat_data = heat_df[["latitude", "longitude", "weight"]].values.tolist()

            HeatMap(
                heat_data,
                radius=18,
                blur=20,
                max_zoom=10
            ).add_to(m)

    else:
        for _, row in map_df.iterrows():
            price = row.get("list_price", None)

            is_focused = (
                focused_property_id is not None
                and row.get("property_id") == focused_property_id
            )

            popup = make_home_popup(row)

            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=5,
                color="white",
                weight=1,
                fill=True,
                fill_color=price_color(price),
                fill_opacity=0.75,
                popup=popup
            ).add_to(m)

    if focus_home and pd.notna(focus_home.get("lat")) and pd.notna(focus_home.get("lon")):
        focused_row = None

        if focused_property_id is not None and "property_id" in map_df.columns:
            matches = map_df[map_df["property_id"] == focused_property_id]
            if len(matches) > 0:
                focused_row = matches.iloc[0]

        focused_popup = make_home_popup(focused_row) if focused_row is not None else "Selected home"

        folium.Marker(
            location=[focus_home["lat"], focus_home["lon"]],
            popup=focused_popup,
            icon=folium.Icon(color="red", icon="home", prefix="fa")
        ).add_to(m)

    legend_html = """
    <div style="
        position: fixed;
        bottom: 140px;
        left: 24px;
        z-index: 999999;
        background: rgba(255,255,255,0.96);
        padding: 14px 18px;
        border-radius: 14px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.18);
        font-size: 14px;
        color: #111827;
        line-height: 1.45;
    ">
        <div style="
            font-weight:700;
            margin-bottom:8px;
            font-size:17px;
        ">
            Listing Price
        </div>

        <div style="margin-bottom:4px;">
            <span style="color:#93c5fd; font-size:18px;">●</span>
            Under $300k
        </div>

        <div style="margin-bottom:4px;">
            <span style="color:#3b82f6; font-size:18px;">●</span>
            $300k–$600k
        </div>

        <div style="margin-bottom:4px;">
            <span style="color:#1d4ed8; font-size:18px;">●</span>
            $600k–$1M
        </div>

        <div>
            <span style="color:#0f172a; font-size:18px;">●</span>
            Over $1M
        </div>
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))
    map_html = m.get_root().render()

    components.html(
        map_html,
        height=790,
        scrolling=False
    )

# ---------------- TABLE ----------------
elif page == "Table":
    table_source = df.copy()

    display_cols = [
        "status", "list_price", "city", "county",
        "beds", "full_baths", "sqft",
        "latitude", "longitude", "property_id"
    ]

    available_cols = [col for col in display_cols if col in table_source.columns]
    table_df = table_source[available_cols].copy()

    if "list_price" in table_df.columns:
        table_df = table_df.sort_values("list_price", ascending=False)

    table_df = table_df.reset_index(drop=True)

    # ---------- TABLE PAGINATION ----------
    ROWS_PER_PAGE = 20

    if "table_page" not in st.session_state:
        st.session_state.table_page = 1

    total_rows = len(table_df)
    total_pages = max(1, math.ceil(total_rows / ROWS_PER_PAGE))

    if st.session_state.table_page > total_pages:
        st.session_state.table_page = total_pages

    start_idx = (st.session_state.table_page - 1) * ROWS_PER_PAGE
    end_idx = start_idx + ROWS_PER_PAGE

    page_df = table_df.iloc[start_idx:end_idx]

    st.markdown("""
    <style>
    .housing-table-row {
        display: grid;
        grid-template-columns: 1.1fr 1.2fr 1.4fr 1.4fr .6fr .6fr .8fr .7fr;
        align-items: center;
        min-height: 62px;
        border-bottom: 1px solid #eeeeee;
        padding: 0 22px;
        font-size: 17px;
        font-weight: 500;
        color: #202124;
    }

    .housing-table-header {
        color: #a3a3a3;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: .06em;
        text-transform: uppercase;
    }

    .status-pill {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 999px;
        font-size: 15px;
        font-weight: 800;
    }

    .for-sale {
        color: #057a3d;
        background: #e8f7ee;
        border: 1px solid #bde8cc;
    }

    .pending {
        color: #b45309;
        background: #fff4df;
        border: 1px solid #f6d399;
    }

    .go-map-box {
        display: flex;
        align-items: center;
        color: #6b7280;
        font-size: 16px;
        padding-left: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="housing-table-row housing-table-header">
        <div>STATUS</div>
        <div>LIST PRICE</div>
        <div>CITY</div>
        <div>COUNTY</div>
        <div>BEDS</div>
        <div>BATHS</div>
        <div>SQFT</div>
        <div>VIEW</div>
    </div>
    """, unsafe_allow_html=True)

    for i, row in page_df.iterrows():
        status = clean_value(row.get("status"), "--")

        if status == "FOR_SALE":
            status_html = '<span class="status-pill for-sale">For Sale</span>'
        elif status == "PENDING":
            status_html = '<span class="status-pill pending">Pending</span>'
        else:
            status_html = html.escape(status.replace("_", " ").title())

        price = money_value(row.get("list_price"))
        city = clean_value(row.get("city"), "--")
        county = clean_value(row.get("county"), "--")
        beds = number_value(row.get("beds"), "--")
        baths = number_value(row.get("full_baths"), "--")
        sqft = number_value(row.get("sqft"), "--")

        cols = st.columns([1.1, 1.2, 1.4, 1.4, .6, .6, .8, .7])

        with cols[0]:
            st.markdown(status_html, unsafe_allow_html=True)
        with cols[1]:
            st.markdown(price)
        with cols[2]:
            st.markdown(city)
        with cols[3]:
            st.markdown(county)
        with cols[4]:
            st.markdown(beds)
        with cols[5]:
            st.markdown(baths)
        with cols[6]:
            st.markdown(sqft)
        with cols[7]:
            if st.button("🔍", key=f"view_home_{i}"):
                st.session_state.focus_home = {
                    "lat": row.get("latitude"),
                    "lon": row.get("longitude"),
                    "property_id": row.get("property_id"),
                }
                st.session_state.page = "Map"
                st.rerun()

    # ---------- PAGINATION CONTROLS ----------
    st.divider()

    p1, p2, p3, p4, p5 = st.columns([3, 1, 1, 1, 3])

    with p1:
        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                height:38px;
                color:#9ca3af;
                font-size:15px;
            ">
                Showing {start_idx + 1}-{min(end_idx, total_rows)} of {total_rows:,}
            </div>
            """,
            unsafe_allow_html=True
        )

    with p2:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button(
            "‹ Prev",
            disabled=st.session_state.table_page == 1,
            use_container_width=True,
        ):
            st.session_state.table_page -= 1
            st.session_state.selected_home_index = None
            st.rerun()

    with p3:
        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:center;
                align-items:center;
                height:38px;
                color:#6b7280;
                font-size:18px;
                font-weight:700;
            ">
                {st.session_state.table_page}
            </div>
            """,
            unsafe_allow_html=True
        )

    with p4:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button(
            "Next ›",
            disabled=st.session_state.table_page >= total_pages,
            use_container_width=True,
        ):
            st.session_state.table_page += 1
            st.session_state.selected_home_index = None
            st.rerun()

    with p5:
        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:flex-end;
                align-items:center;
                height:38px;
                color:#9ca3af;
                font-size:15px;
            ">
                Page {st.session_state.table_page:,} of {total_pages:,}
            </div>
            """,
            unsafe_allow_html=True
        )
# ---------------- STATS ----------------
elif page == "Stats":
    import altair as alt

    stats_df = df.copy()

    total_listings = len(stats_df)
    pending_count = (stats_df["status"] == "PENDING").sum() if "status" in stats_df.columns else 0
    median_price = stats_df["list_price"].median() if "list_price" in stats_df.columns else 0
    median_sqft = stats_df["sqft"].median() if "sqft" in stats_df.columns else 0

    valid_ppsf = stats_df[
        stats_df["list_price"].notna()
        & stats_df["sqft"].notna()
        & (stats_df["sqft"] > 0)
    ].copy()

    median_ppsf = (valid_ppsf["list_price"] / valid_ppsf["sqft"]).median() if len(valid_ppsf) else 0
    pending_pct = pending_count / total_listings * 100 if total_listings > 0 else 0

    st.markdown("""
    <style>
    .block-container {
        background: #f7f7f6 !important;
    }

    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        min-height: 102px;
    }

    .filter-card {
        background: #fff8e6;
        border: 1px solid #fbbf24;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 6px;
    }

    .metric-label {
        font-size: 13px;
        color: #6b7280;
        font-weight: 500;
    }

    .filter-title {
        font-size: 12px;
        font-weight: 800;
        color: #8a6a00;
        letter-spacing: .08em;
        margin-bottom: 10px;
    }

    .filter-pill {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        border: 1px solid #f59e0b;
        background: white;
        color: #7c4a03;
        font-weight: 700;
        font-size: 12px;
        margin-bottom: 10px;
    }
                
    div[data-testid="stVegaLiteChart"] {
    margin-top: 14px !important;
    margin-bottom: 34px !important;
}

    .chart-title {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px 18px 0 0;

        padding: 22px 28px;

        color: #a3a3a3;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: .09em;
        text-transform: uppercase;

        margin-top: -10px;          /* was 24px */
        margin-bottom: 5px;       /* pulls chart closer */
        width: calc(100% - 46px);  /* shorten from the right */
    }
    </style>
    """, unsafe_allow_html=True)

    c0, c1, c2, c3, c4, c5, c6 = st.columns(7)

    active_filters = []

    if selected_counties:
        active_filters.append(
            "County: " +
            ", ".join(map(str, selected_counties[:2])) +
            ("..." if len(selected_counties) > 2 else "")
        )

    if selected_cities:
        active_filters.append(
            "City: " +
            ", ".join(map(str, selected_cities[:2])) +
            ("..." if len(selected_cities) > 2 else "")
        )

    if selected_beds:
        active_filters.append(
            "Beds: " + ", ".join(map(str, selected_beds))
        )

    if selected_baths:
        active_filters.append(
            "Baths: " + ", ".join(map(str, selected_baths))
        )

    filter_label = "Virginia" if not active_filters else " | ".join(active_filters)

    cards = [
        ("FILTERED VIEW", filter_label, f"{total_listings:,} listings", "filter"),
        (f"{total_listings:,}", "Visible listings", "", ""),
        (f"${median_price:,.0f}", "Median price", "", ""),
        (f"${median_ppsf:,.0f}", "Median price / sqft", "", ""),
        (f"{pending_count:,}", "Pending listings", "", ""),
        (f"{pending_pct:.1f}%", "Pending share", "", ""),
        (f"{median_sqft:,.0f}", "Median sqft", "", ""),
    ]

    for col, card in zip([c0, c1, c2, c3, c4, c5, c6], cards):
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        with col:
            if card[3] == "filter":
                st.markdown(f"""
                <div class="metric-card filter-card">
                    <div class="filter-title">{card[0]}</div>
                    <div class="filter-pill">{card[1]}</div>
                    <div class="metric-label"><b>{card[2]}</b></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{card[0]}</div>
                    <div class="metric-label">{card[1]}</div>
                </div>
                """, unsafe_allow_html=True)

    axis_main = alt.Axis(labelFontSize=15, titleFontSize=17)

    # STATUS BREAKDOWN
    if "status" in stats_df.columns:
        status_counts = (
            stats_df["status"]
            .fillna("UNKNOWN")
            .value_counts()
            .reset_index()
        )
        status_counts.columns = ["Status", "Listings"]
        status_chart = (
            alt.Chart(status_counts)
            .mark_bar(cornerRadius=8)
            .encode(
                x=alt.X("Listings:Q", title=None, axis=alt.Axis(labelFontSize=15)),
                y=alt.Y(
                    "Status:N",
                    sort="-x",
                    title=None,
                    axis=alt.Axis(
                        labelFontSize=15,
                        labelPadding=8,
                        labelLimit=120,
                        offset=0
                    )
                ),
                color=alt.Color(
                    "Status:N",
                    scale=alt.Scale(
                        domain=["FOR_SALE", "PENDING", "CONTINGENT"],
                        range=["#16a34a", "#f59e0b", "#6366f1"]
                    ),
                    legend=None
                ),
                tooltip=["Status", "Listings"]
            )
            .properties(width=1350, height=400)
            .configure_view(strokeWidth=0)
        )

        left, middle, right = st.columns([0.01, 9.99, 0.01])

        with middle:
            st.markdown(
                '<div class="chart-title">Listing Status Breakdown</div>',
                unsafe_allow_html=True
            )

            st.altair_chart(
                status_chart,
                use_container_width=False
            )


    # COUNTY MEDIAN PRICE
    if "county" in stats_df.columns and "list_price" in stats_df.columns:
        county_chart_df = stats_df.copy()
        
        county_chart_df["county"] = (
            county_chart_df["county"]
            .fillna("")
            .astype(str)
            .str.strip()
            )
        
        county_chart_df = county_chart_df[
            ~county_chart_df["county"].str.lower().isin(
                ["", "nan", "none", "beds", "baths", "dots", "style"]
                )
            ]
        
        county_stats = (
            county_chart_df.groupby("county", dropna=True)
            .agg(
                Listings=("list_price", "size"),
                Median_Price=("list_price", "median")
                )
            .reset_index()
            .sort_values("Median_Price", ascending=False)
            .head(10)
            
            )

        county_chart = (
            alt.Chart(county_stats)
            .mark_bar(cornerRadius=8)
            .encode(
                x=alt.X(
                    "Median_Price:Q",
                    title="Median Listing Price",
                    axis=alt.Axis(format="$,.0f", labelFontSize=15, titleFontSize=17)
                ),
                y=alt.Y("county:N", sort="-x", title=None, axis=alt.Axis(labelFontSize=15)),
                color=alt.Color("Median_Price:Q", scale=alt.Scale(scheme="tealblues"), legend=None),
                tooltip=[
                    alt.Tooltip("county:N", title="County"),
                    alt.Tooltip("Listings:Q", title="Listings"),
                    alt.Tooltip("Median_Price:Q", title="Median Price", format="$,.0f")
                ]
            )
            .properties(
                width=1350,
                height=400)
        )

        left, middle, right = st.columns([0.01, 9.99, 0.01])

        with middle:
            st.markdown(
                '<div class="chart-title">Top Counties by Median Listing Price</div>',
                unsafe_allow_html=True
            )

            st.altair_chart(
                county_chart,
                use_container_width=False
            )

    # PRICE DISTRIBUTION
    if "list_price" in stats_df.columns:
        price_df = stats_df[stats_df["list_price"].notna()].copy()

        price_chart = (
            alt.Chart(price_df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color="#7c3aed")
            .encode(
                x=alt.X(
                    "list_price:Q",
                    bin=alt.Bin(maxbins=40),
                    title="Listing Price",
                    axis=alt.Axis(format="$,.0f", labelFontSize=15, titleFontSize=17)
                ),
                y=alt.Y("count():Q", title="Listings", axis=alt.Axis(labelFontSize=15, titleFontSize=17)),
                tooltip=["count()"]
            )
            .properties(
                width=1350,
                height=400)
        )

        left, middle, right = st.columns([0.01, 9.99, 0.01])

        with middle:
            st.markdown(
                '<div class="chart-title">Listing Price Distribution</div>',
                unsafe_allow_html=True
            )

            st.altair_chart(
                price_chart,
                use_container_width=False
            )
