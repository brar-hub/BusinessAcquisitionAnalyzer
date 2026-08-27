# ============================================================
# CUSTOM CSS —  WTM FINANCIAL CALCULATOR STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif !important;
        color: #000000;
    }

    .stApp {
        background: #ffffff;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 0.5rem;
        padding-bottom: 2rem;
    }

    /* =====================================================
       HEADINGS
       ===================================================== */

    h1 {
        color: #003366 !important;
        font-size: 26px !important;
        font-weight: bold !important;
        margin: 12px 0 !important;
    }

    h2 {
        color: #003366 !important;
        font-size: 22px !important;
        font-weight: bold !important;
        margin-bottom: 2px !important;
    }

    h3 {
        color: #000000 !important;
        font-size: 19px !important;
        font-weight: bold !important;
    }

    p {
        margin: 5px 0 8px 0;
    }

    /* =====================================================
       WTM HEADER
       ===================================================== */

    .wtm-header {
        background: #003366;
        color: #ffffff;
        margin-left: -1rem;
        margin-right: -1rem;
        padding: 15px 25px;
        margin-bottom: 12px;
    }

    .wtm-brand {
        color: #ffffff;
        font-size: 18px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 2px;
    }

    .wtm-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: bold;
        margin: 0;
    }

    .wtm-tagline {
        color: #dddddd;
        font-size: 16px;
        margin-top: 5px;
    }

    /* =====================================================
       SECTION HEADERS
       ===================================================== */

    .section-title {
        background: #336699;
        color: #ffffff;
        padding: 6px 8px;
        font-size: 18px;
        font-weight: bold;
        margin-top: 12px;
        margin-bottom: 8px;
        border: 1px solid #114477;
    }

    /* =====================================================
       INPUT PANELS
       ===================================================== */

    .input-panel {
        background: #eeeeee;
        border: 1px solid #bbbbbb;
        padding: 10px;
        margin-bottom: 8px;
    }

    /* =====================================================
       STREAMLIT INPUTS
       ===================================================== */

    div[data-baseweb="input"] {
        border: 1px solid #044284 !important;
        border-radius: 2px !important;
        box-shadow: 1px 1px 2px #666666 !important;
        background: #ffffff !important;
    }

    div[data-baseweb="select"] {
        border: 1px solid #044284 !important;
        border-radius: 2px !important;
        box-shadow: 1px 1px 2px #666666 !important;
        background: #ffffff !important;
    }

    input {
        color: #000000 !important;
        background: #ffffff !important;
        font-size: 16px !important;
    }

    label {
        color: #000000 !important;
        font-size: 15px !important;
        font-weight: normal !important;
    }

    /* =====================================================
       METRICS
       ===================================================== */

    div[data-testid="stMetric"] {
        background: #eeeeee;
        border: 1px solid #bbbbbb;
        border-radius: 0px;
        padding: 8px 10px;
    }

    div[data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-size: 14px !important;
    }

    div[data-testid="stMetricValue"] {
        color: #003366 !important;
        font-size: 24px !important;
        font-weight: bold !important;
    }

    /* =====================================================
       RESULT BOX
       ===================================================== */

    .result-box {
        background: #e3edda;
        border: 1px solid #8db46d;
        padding: 10px;
        text-align: center;
        margin: 8px 0;
    }

    .result-title {
        background: #518428;
        color: #ffffff;
        border: 1px solid #518428;
        padding: 5px;
        margin-top: 3px;
        font-size: 22px;
        font-weight: normal;
    }

    .result-value {
        font-size: 30px;
        font-weight: bold;
        color: #23832b;
    }

    /* =====================================================
       VERDICT
       ===================================================== */

    .verdict-box {
        border: 1px solid #336699;
        background: #eeeeee;
        padding: 12px;
        margin: 10px 0;
        text-align: center;
    }

    .verdict-label {
        font-size: 28px;
        font-weight: bold;
        color: #003366;
    }

    .verdict-score {
        font-size: 34px;
        font-weight: bold;
        color: #518428;
    }

    /* =====================================================
       TABLES
       ===================================================== */

    table {
        border-collapse: collapse !important;
        border-spacing: 0 !important;
    }

    th {
        background-color: #336699 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: 1px solid #114477 !important;
    }

    td {
        border: 1px solid #cccccc !important;
        color: #000000 !important;
    }

    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border: 0;
        color: #aaaaaa;
        background-color: #aaaaaa;
        height: 1px;
        margin: 12px 0;
    }

    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 2px !important;
    }

    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border: 0;
        border-radius: 2px;
        color: #ffffff;
        padding: 10px 18px;
        font-size: 16px;
        font-weight: bold;
        background-color: #4c7b25;
    }

    .stButton > button:hover {
        background-color: #444444;
        color: #ffffff;
    }

    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background: #eeeeee;
        border-right: 1px solid #bbbbbb;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #003366 !important;
    }

    /* =====================================================
       FOOTER
       ===================================================== */

    .wtm-footer {
        background: #e1e1e1;
        padding: 20px;
        margin-top: 30px;
        text-align: center;
        font-size: 13px;
        color: #555555;
        border-top: 1px solid #bbbbbb;
    }

    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 720px) {

        .block-container {
            padding-left: 10px;
            padding-right: 10px;
        }

        .wtm-header {
            margin-left: -10px;
            margin-right: -10px;
            padding: 12px 15px;
        }

        .wtm-title {
            font-size: 22px;
        }

        .wtm-tagline {
            font-size: 14px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 20px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)
