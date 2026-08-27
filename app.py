# ============================================================
# CUSTOM CSS — WTM BLUE FINANCIAL CALCULATOR STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 16px;
        color: #000000;
    }

    .stApp {
        background-color: #d1dde9;
    }

    .main {
        background-color: #d1dde9;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       TOP HEADER
       ======================================================== */

    .wtm-header {
        background: #003366;
        padding: 18px 25px 20px 25px;
        margin-bottom: 15px;
        border-radius: 0px;
    }

    .wtm-brand {
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 3px;
        margin-bottom: 6px;
    }

    .wtm-header h1 {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: bold !important;
        margin: 4px 0 5px 0 !important;
        letter-spacing: 0px;
    }

    .wtm-subtitle {
        color: #dce8f3;
        font-size: 17px;
        margin-bottom: 0px;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1 {
        color: #003366;
        font-size: 26px;
        font-weight: bold;
    }

    h2 {
        color: #003366;
        font-size: 22px;
        font-weight: bold;
    }

    h3 {
        color: #003366;
        font-size: 19px;
        font-weight: bold;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #eeeeee;
        border-right: 1px solid #bbbbbb;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #003366 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stNumberInput"] {
        margin-bottom: 5px;
    }


    /* ========================================================
       INPUT FIELDS
       ======================================================== */

    input[type="number"],
    input[type="text"] {
        border: 1px solid #044284 !important;
        border-radius: 2px !important;
        box-shadow: 1px 1px 2px #666 !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        font-size: 16px !important;
    }

    input:focus {
        border-color: #003366 !important;
        box-shadow: 0 0 0 1px #003366 !important;
    }


    /* ========================================================
       STREAMLIT NUMBER INPUT
       ======================================================== */

    div[data-testid="stNumberInput"] label {
        color: #000000 !important;
        font-weight: bold;
    }


    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .wtm-section {
        background-color: #336699;
        padding: 7px 10px;
        color: #ffffff;
        font-size: 19px;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 8px;
    }


    /* ========================================================
       VERDICT BOX
       ======================================================== */

    .verdict-box {
        padding: 25px;
        border: 1px solid #8db46d;
        background: #e3edda;
        border-radius: 2px;
        text-align: center;
        margin-bottom: 15px;
    }

    .verdict-score {
        color: #003366;
        font-size: 58px;
        font-weight: bold;
        line-height: 1;
    }

    .verdict-label {
        color: #003366;
        font-size: 28px;
        font-weight: bold;
        margin-top: 8px;
    }

    .small-label {
        color: #555555;
        font-size: 13px;
        font-weight: bold;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #bbbbbb;
        border-radius: 2px;
        padding: 12px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.15);
    }

    div[data-testid="stMetricLabel"] {
        color: #555555 !important;
        font-size: 13px !important;
        font-weight: bold !important;
    }

    div[data-testid="stMetricValue"] {
        color: #003366 !important;
        font-size: 26px !important;
        font-weight: bold !important;
    }


    /* ========================================================
       DATA TABLES
       ======================================================== */

    div[data-testid="stDataFrame"] {
        background: #ffffff;
        border: 1px solid #336699;
    }

    [data-testid="stDataFrame"] th {
        background-color: #336699 !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }


    /* ========================================================
       SUCCESS / WARNING / ERROR
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 2px;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    button[kind="primary"] {
        background-color: #518428 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 2px !important;
        font-weight: bold !important;
    }

    button[kind="primary"]:hover {
        background-color: #417516 !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border: 0;
        height: 1px;
        background-color: #aaaaaa;
        margin: 18px 0;
    }


    /* ========================================================
       CHART CONTAINERS
       ======================================================== */

    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border: 1px solid #bbbbbb;
        padding: 5px;
    }


    /* ========================================================
       CAPTION / DISCLAIMER
       ======================================================== */

    .stCaption {
        font-size: 13px;
        color: #555555;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 720px) {

        .block-container {
            padding-left: 10px;
            padding-right: 10px;
        }

        .wtm-header {
            padding: 15px;
        }

        .wtm-header h1 {
            font-size: 23px !important;
        }

        .wtm-subtitle {
            font-size: 15px;
        }

        .verdict-score {
            font-size: 48px;
        }

        .verdict-label {
            font-size: 24px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)
