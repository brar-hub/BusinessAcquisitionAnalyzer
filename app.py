import streamlit as st

st.set_page_config(
    page_title="WTM Business Acquisition Analyzer",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# WTM BRANDING
# ---------------------------------------------------------

st.title("WTM Business Acquisition Analyzer")

st.markdown(
    """
    ### Analyze the price. Model the financing. Stress-test the deal.

    Evaluate a business acquisition before you make an offer.
    """
)

st.divider()

# ---------------------------------------------------------
# BUSINESS INFORMATION
# ---------------------------------------------------------

st.header("1. Business Information")

col1, col2 = st.columns(2)

with col1:

    purchase_price = st.number_input(
        "Purchase Price ($)",
        min_value=0.0,
        value=1_200_000.0,
        step=25_000.0
    )

    annual_revenue = st.number_input(
        "Annual Revenue ($)",
        min_value=0.0,
        value=2_500_000.0,
        step=50_000.0
    )

    sde = st.number_input(
        "Seller Discretionary Earnings — SDE ($)",
        min_value=0.0,
        value=350_000.0,
        step=10_000.0
    )

with col2:

    ebitda = st.number_input(
        "EBITDA ($)",
        min_value=0.0,
        value=300_000.0,
        step=10_000.0
    )

    owner_compensation = st.number_input(
        "Current Owner Compensation ($)",
        min_value=0.0,
        value=100_000.0,
        step=10_000.0
    )

    replacement_salary = st.number_input(
        "Replacement Manager Salary ($)",
        min_value=0.0,
        value=90_000.0,
        step=5_000.0
    )

# ---------------------------------------------------------
# OPERATING ASSUMPTIONS
# ---------------------------------------------------------

st.header("2. Operating Assumptions")

col1, col2, col3 = st.columns(3)

with col1:

    capex = st.number_input(
        "Annual Maintenance CapEx ($)",
        min_value=0.0,
        value=25_000.0,
        step=5_000.0
    )

with col2:

    working_capital = st.number_input(
        "Additional Working Capital ($)",
        min_value=0.0,
        value=50_000.0,
        step=5_000.0
    )

with col3:

    revenue_growth = st.number_input(
        "Annual Revenue Growth (%)",
        min_value=-50.0,
        max_value=100.0,
        value=3.0,
        step=0.5
    )

# ---------------------------------------------------------
# FINANCING
# ---------------------------------------------------------

st.header("3. Acquisition Financing")

col1, col2 = st.columns(2)

with col1:

    buyer_equity = st.number_input(
        "Buyer Equity ($)",
        min_value=0.0,
        value=300_000.0,
        step=25_000.0
    )

    bank_debt = st.number_input(
        "Bank / Senior Debt ($)",
        min_value=0.0,
        value=800_000.0,
        step=25_000.0
    )

with col2:

    bank_rate = st.number_input(
        "Bank Interest Rate (%)",
        min_value=0.0,
        max_value=30.0,
        value=7.5,
        step=0.25
    )

    bank_amortization = st.number_input(
        "Bank Amortization (Years)",
        min_value=1,
        max_value=30,
        value=10,
        step=1
    )

# ---------------------------------------------------------
# SELLER FINANCING
# ---------------------------------------------------------

st.subheader("Seller Financing")

col1, col2, col3 = st.columns(3)

with col1:

    seller_financing = st.number_input(
        "Seller Financing ($)",
        min_value=0.0,
        value=100_000.0,
        step=10_000.0
    )

with col2:

    seller_rate = st.number_input(
        "Seller Financing Rate (%)",
        min_value=0.0,
        max_value=30.0,
        value=5.0,
        step=0.25
    )

with col3:

    seller_amortization = st.number_input(
        "Seller Amortization (Years)",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )

# ---------------------------------------------------------
# EXIT ASSUMPTIONS
# ---------------------------------------------------------

st.header("4. Exit Assumptions")

col1, col2 = st.columns(2)

with col1:

    holding_period = st.number_input(
        "Holding Period (Years)",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )

with col2:

    exit_multiple = st.number_input(
        "Exit EBITDA Multiple",
        min_value=0.5,
        max_value=20.0,
        value=4.0,
        step=0.25
    )

# ---------------------------------------------------------
# CURRENT INPUT SUMMARY
# ---------------------------------------------------------

st.divider()

st.header("Deal Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Purchase Price",
        f"${purchase_price:,.0f}"
    )

with col2:
    st.metric(
        "Revenue",
        f"${annual_revenue:,.0f}"
    )

with col3:
    st.metric(
        "SDE",
        f"${sde:,.0f}"
    )

with col4:
    st.metric(
        "EBITDA",
        f"${ebitda:,.0f}"
    )

st.divider()

st.info(
    "WTM Business Acquisition Analyzer is an educational "
    "financial modeling tool. Results depend on the accuracy "
    "of the assumptions entered."
)
