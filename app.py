import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="WTM Business Acquisition Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f8fa;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1 {
        font-weight: 800;
        letter-spacing: -1px;
    }

    h2 {
        font-weight: 700;
    }

    h3 {
        font-weight: 650;
    }

    .wtm-header {
        padding: 25px 0 10px 0;
    }

    .wtm-brand {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }

    .wtm-subtitle {
        font-size: 18px;
        color: #667085;
        margin-bottom: 25px;
    }

    .verdict-box {
        padding: 28px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        background: white;
        text-align: center;
        margin-bottom: 20px;
    }

    .verdict-score {
        font-size: 64px;
        font-weight: 850;
        line-height: 1;
    }

    .verdict-label {
        font-size: 30px;
        font-weight: 850;
        margin-top: 10px;
    }

    .small-label {
        color: #667085;
        font-size: 13px;
        font-weight: 600;
    }

    .big-value {
        font-size: 32px;
        font-weight: 800;
    }

    .risk-box {
        padding: 18px;
        border-radius: 12px;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        margin-top: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):
    """Format CAD currency."""
    if value is None or not np.isfinite(value):
        return "$0"

    return f"${value:,.0f}"


def pct(value):
    """Format percentage."""
    if value is None or not np.isfinite(value):
        return "N/A"

    return f"{value:.1%}"


def multiple(value):
    """Format valuation multiple."""
    if value is None or not np.isfinite(value):
        return "N/A"

    return f"{value:.2f}×"


def loan_payment(principal, annual_rate, amortization_years):
    """
    Calculate monthly loan payment using standard
    fully amortizing loan formula.
    """

    if principal <= 0:
        return 0

    months = int(amortization_years * 12)

    if months <= 0:
        return 0

    monthly_rate = annual_rate / 100 / 12

    if monthly_rate == 0:
        return principal / months

    payment = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** months
        / ((1 + monthly_rate) ** months - 1)
    )

    return payment


def amortization_schedule(
    principal,
    annual_rate,
    amortization_years,
    projection_years
):
    """
    Generate monthly amortization schedule.
    """

    if principal <= 0:
        return pd.DataFrame(
            columns=[
                "Month",
                "Beginning Balance",
                "Payment",
                "Interest",
                "Principal",
                "Ending Balance"
            ]
        )

    monthly_payment = loan_payment(
        principal,
        annual_rate,
        amortization_years
    )

    monthly_rate = annual_rate / 100 / 12

    months = int(
        min(
            amortization_years,
            projection_years
        ) * 12
    )

    balance = principal

    rows = []

    for month in range(1, months + 1):

        beginning_balance = balance

        if monthly_rate == 0:

            interest = 0

        else:

            interest = (
                balance * monthly_rate
            )

        principal_payment = (
            monthly_payment - interest
        )

        principal_payment = min(
            principal_payment,
            balance
        )

        payment = (
            interest +
            principal_payment
        )

        balance = max(
            0,
            balance - principal_payment
        )

        rows.append(
            {
                "Month": month,
                "Beginning Balance": beginning_balance,
                "Payment": payment,
                "Interest": interest,
                "Principal": principal_payment,
                "Ending Balance": balance
            }
        )

        if balance <= 0:
            break

    return pd.DataFrame(rows)


def ending_balance(
    principal,
    annual_rate,
    amortization_years,
    months_elapsed
):
    """
    Calculate loan balance after a given number of months.
    """

    if principal <= 0:
        return 0

    if months_elapsed <= 0:
        return principal

    months_elapsed = int(months_elapsed)

    total_months = int(
        amortization_years * 12
    )

    if months_elapsed >= total_months:
        return 0

    payment = loan_payment(
        principal,
        annual_rate,
        amortization_years
    )

    monthly_rate = (
        annual_rate / 100 / 12
    )

    if monthly_rate == 0:

        return max(
            0,
            principal -
            payment * months_elapsed
        )

    balance = (
        principal *
        (1 + monthly_rate) ** months_elapsed
        -
        payment *
        (
            ((1 + monthly_rate) ** months_elapsed - 1)
            / monthly_rate
        )
    )

    return max(0, balance)


def calculate_irr(cash_flows):
    """
    Calculate IRR using numpy financial-style
    polynomial root approach.
    """

    if len(cash_flows) < 2:
        return np.nan

    try:

        irr = npf_irr(cash_flows)

        if np.isfinite(irr):
            return irr

    except Exception:
        pass

    return np.nan


def npf_irr(cash_flows):
    """
    IRR calculation using Newton-Raphson.
    """

    rate = 0.10

    for _ in range(100):

        npv = 0
        derivative = 0

        for period, cash_flow in enumerate(
            cash_flows
        ):

            denominator = (
                (1 + rate) ** period
            )

            npv += (
                cash_flow /
                denominator
            )

            if period > 0:

                derivative -= (
                    period *
                    cash_flow /
                    ((1 + rate) ** (period + 1))
                )

        if abs(derivative) < 1e-12:
            break

        new_rate = (
            rate -
            npv / derivative
        )

        if not np.isfinite(new_rate):
            break

        if new_rate <= -0.99:
            new_rate = -0.99

        if abs(new_rate - rate) < 1e-8:
            return new_rate

        rate = new_rate

    return rate


def calculate_deal(inputs):
    """
    Main acquisition model.
    """

    purchase_price = inputs["purchase_price"]
    revenue = inputs["revenue"]
    sde = inputs["sde"]
    ebitda = inputs["ebitda"]

    replacement_salary = inputs[
        "replacement_salary"
    ]

    capex = inputs["capex"]

    working_capital = inputs[
        "working_capital"
    ]

    buyer_equity = inputs[
        "buyer_equity"
    ]

    bank_debt = inputs[
        "bank_debt"
    ]

    bank_rate = inputs[
        "bank_rate"
    ]

    bank_amortization = inputs[
        "bank_amortization"
    ]

    seller_financing = inputs[
        "seller_financing"
    ]

    seller_rate = inputs[
        "seller_rate"
    ]

    seller_amortization = inputs[
        "seller_amortization"
    ]

    revenue_growth = inputs[
        "revenue_growth"
    ]

    holding_period = inputs[
        "holding_period"
    ]

    exit_multiple = inputs[
        "exit_multiple"
    ]

    # --------------------------------------------------------
    # TRANSACTION SOURCES & USES
    # --------------------------------------------------------

    total_debt = (
        bank_debt +
        seller_financing
    )

    total_sources = (
        buyer_equity +
        total_debt
    )

    total_uses = (
        purchase_price +
        working_capital
    )

    funding_gap = (
        total_sources -
        total_uses
    )

    # --------------------------------------------------------
    # VALUATION
    # --------------------------------------------------------

    sde_multiple = (
        purchase_price / sde
        if sde > 0
        else np.nan
    )

    ebitda_multiple = (
        purchase_price / ebitda
        if ebitda > 0
        else np.nan
    )

    # --------------------------------------------------------
    # DEBT SERVICE
    # --------------------------------------------------------

    monthly_bank_payment = loan_payment(
        bank_debt,
        bank_rate,
        bank_amortization
    )

    monthly_seller_payment = loan_payment(
        seller_financing,
        seller_rate,
        seller_amortization
    )

    annual_bank_debt_service = (
        monthly_bank_payment * 12
    )

    annual_seller_debt_service = (
        monthly_seller_payment * 12
    )

    total_annual_debt_service = (
        annual_bank_debt_service +
        annual_seller_debt_service
    )

    # --------------------------------------------------------
    # OPERATING CASH FLOW
    # --------------------------------------------------------

    adjusted_ebitda = (
        ebitda -
        replacement_salary
    )

    adjusted_cash_flow = (
        adjusted_ebitda -
        capex
    )

    cash_flow_after_debt = (
        adjusted_cash_flow -
        total_annual_debt_service
    )

    # --------------------------------------------------------
    # DSCR
    # --------------------------------------------------------

    if total_annual_debt_service > 0:

        dscr = (
            adjusted_cash_flow /
            total_annual_debt_service
        )

    else:

        dscr = np.inf

    # --------------------------------------------------------
    # CASH ON CASH
    # --------------------------------------------------------

    if buyer_equity > 0:

        cash_on_cash = (
            cash_flow_after_debt /
            buyer_equity
        )

    else:

        cash_on_cash = np.nan

    # --------------------------------------------------------
    # PROJECTION
    # --------------------------------------------------------

    years = list(
        range(
            1,
            holding_period + 1
        )
    )

    projection_rows = []

    bank_balances = []
    seller_balances = []

    for year in years:

        revenue_year = (
            revenue *
            (1 + revenue_growth / 100)
            ** year
        )

        ebitda_year = (
            ebitda *
            (1 + revenue_growth / 100)
            ** year
        )

        replacement_cost_year = (
            replacement_salary *
            (1.03 ** (year - 1))
        )

        capex_year = (
            capex *
            (1.03 ** (year - 1))
        )

        adjusted_cash_flow_year = (
            ebitda_year -
            replacement_cost_year -
            capex_year
        )

        bank_balance = ending_balance(
            bank_debt,
            bank_rate,
            bank_amortization,
            year * 12
        )

        seller_balance = ending_balance(
            seller_financing,
            seller_rate,
            seller_amortization,
            year * 12
        )

        total_debt_balance = (
            bank_balance +
            seller_balance
        )

        debt_service = (
            total_annual_debt_service
        )

        cash_after_debt = (
            adjusted_cash_flow_year -
            debt_service
        )

        dscr_year = (
            adjusted_cash_flow_year /
            debt_service
            if debt_service > 0
            else np.inf
        )

        projection_rows.append(
            {
                "Year": year,
                "Revenue": revenue_year,
                "EBITDA": ebitda_year,
                "Adjusted Cash Flow":
                    adjusted_cash_flow_year,
                "Debt Service":
                    debt_service,
                "Cash Flow After Debt":
                    cash_after_debt,
                "DSCR": dscr_year,
                "Remaining Debt":
                    total_debt_balance
            }
        )

        bank_balances.append(
            bank_balance
        )

        seller_balances.append(
            seller_balance
        )

    projection = pd.DataFrame(
        projection_rows
    )

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    exit_year_ebitda = (
        projection.iloc[-1]["EBITDA"]
    )

    exit_enterprise_value = (
        exit_year_ebitda *
        exit_multiple
    )

    remaining_bank_debt = (
        bank_balances[-1]
        if bank_balances
        else bank_debt
    )

    remaining_seller_debt = (
        seller_balances[-1]
        if seller_balances
        else seller_financing
    )

    remaining_total_debt = (
        remaining_bank_debt +
        remaining_seller_debt
    )

    exit_equity_value = (
        exit_enterprise_value -
        remaining_total_debt
    )

    # --------------------------------------------------------
    # IRR / MOIC
    # --------------------------------------------------------

    cash_flows = [
        -buyer_equity
    ]

    for index, row in projection.iterrows():

        annual_cash_flow = max(
            0,
            row["Cash Flow After Debt"]
        )

        if index == len(projection) - 1:

            annual_cash_flow += (
                exit_equity_value
            )

        cash_flows.append(
            annual_cash_flow
        )

    irr = calculate_irr(
        cash_flows
    )

    total_cash_received = sum(
        cash_flows[1:]
    )

    total_cash_invested = (
        buyer_equity
    )

    moic = (
        total_cash_received /
        total_cash_invested
        if total_cash_invested > 0
        else np.nan
    )

    # --------------------------------------------------------
    # MAXIMUM OFFER
    # --------------------------------------------------------

    target_dscr = 1.50

    annual_cash_available_for_debt = (
        adjusted_cash_flow /
        target_dscr
    )

    maximum_total_debt = (
        annual_cash_available_for_debt /
        (
            (
                annual_bank_debt_service +
                annual_seller_debt_service
            )
            / total_debt
        )
        if total_debt > 0
        else 0
    )

    debt_capacity_offer = (
        buyer_equity +
        maximum_total_debt -
        working_capital
    )

    # Valuation cross-check using SDE and EBITDA.

    valuation_from_sde = (
        sde * 3.5
        if sde > 0
        else 0
    )

    valuation_from_ebitda = (
        ebitda * 4.0
        if ebitda > 0
        else 0
    )

    valuation_cross_check = (
        valuation_from_sde +
        valuation_from_ebitda
    ) / 2

    if debt_capacity_offer > 0:

        maximum_offer = min(
            debt_capacity_offer,
            valuation_cross_check
        )

    else:

        maximum_offer = valuation_cross_check

    # --------------------------------------------------------
    # DOWNSIDE
    # --------------------------------------------------------

    downside_10_cash_flow = (
        adjusted_cash_flow * 0.90
    )

    downside_20_cash_flow = (
        adjusted_cash_flow * 0.80
    )

    downside_10_dscr = (
        downside_10_cash_flow /
        total_annual_debt_service
        if total_annual_debt_service > 0
        else np.inf
    )

    downside_20_dscr = (
        downside_20_cash_flow /
        total_annual_debt_service
        if total_annual_debt_service > 0
        else np.inf
    )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    score = 50

    # DSCR
    if dscr >= 1.75:
        score += 20
    elif dscr >= 1.50:
        score += 15
    elif dscr >= 1.25:
        score += 5
    elif dscr >= 1.00:
        score -= 10
    else:
        score -= 25

    # Purchase multiple
    if sde_multiple <= 3.0:
        score += 10
    elif sde_multiple <= 4.0:
        score += 5
    elif sde_multiple > 5.0:
        score -= 10

    # IRR
    if np.isfinite(irr):

        if irr >= 0.25:
            score += 15
        elif irr >= 0.20:
            score += 10
        elif irr >= 0.15:
            score += 5
        elif irr < 0.10:
            score -= 15

    # Downside
    if downside_20_dscr >= 1.25:
        score += 5
    elif downside_20_dscr < 1.0:
        score -= 10

    # Funding
    if funding_gap < -1:
        score -= 20

    score = max(
        0,
        min(
            100,
            int(round(score))
        )
    )

    if score >= 75:

        verdict = "BUY"

    elif score >= 55:

        verdict = "NEGOTIATE"

    else:

        verdict = "PASS"

    return {
        "total_debt": total_debt,
        "total_sources": total_sources,
        "total_uses": total_uses,
        "funding_gap": funding_gap,

        "sde_multiple": sde_multiple,
        "ebitda_multiple": ebitda_multiple,

        "annual_bank_debt_service":
            annual_bank_debt_service,

        "annual_seller_debt_service":
            annual_seller_debt_service,

        "total_annual_debt_service":
            total_annual_debt_service,

        "adjusted_ebitda":
            adjusted_ebitda,

        "adjusted_cash_flow":
            adjusted_cash_flow,

        "cash_flow_after_debt":
            cash_flow_after_debt,

        "dscr": dscr,

        "cash_on_cash":
            cash_on_cash,

        "projection":
            projection,

        "exit_enterprise_value":
            exit_enterprise_value,

        "remaining_total_debt":
            remaining_total_debt,

        "exit_equity_value":
            exit_equity_value,

        "irr":
            irr,

        "moic":
            moic,

        "maximum_offer":
            maximum_offer,

        "debt_capacity_offer":
            debt_capacity_offer,

        "valuation_cross_check":
            valuation_cross_check,

        "downside_10_dscr":
            downside_10_dscr,

        "downside_20_dscr":
            downside_20_dscr,

        "score":
            score,

        "verdict":
            verdict
    }


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="wtm-header">

    <div class="wtm-brand">
    WEALTH THAT MATTERS
    </div>

    <h1>Business Acquisition Analyzer</h1>

    <div class="wtm-subtitle">
    Analyze the price. Model the financing. Stress-test the deal.
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR — BUSINESS INPUTS
# ============================================================

with st.sidebar:

    st.header("Deal Inputs")

    st.subheader("Business")

    purchase_price = st.number_input(
        "Purchase Price ($)",
        min_value=0.0,
        value=1_200_000.0,
        step=25_000.0
    )

    revenue = st.number_input(
        "Annual Revenue ($)",
        min_value=0.0,
        value=2_500_000.0,
        step=50_000.0
    )

    sde = st.number_input(
        "SDE ($)",
        min_value=0.0,
        value=350_000.0,
        step=10_000.0
    )

    ebitda = st.number_input(
        "EBITDA ($)",
        min_value=0.0,
        value=300_000.0,
        step=10_000.0
    )

    st.divider()

    st.subheader("Operations")

    replacement_salary = st.number_input(
        "Replacement Manager Salary ($)",
        min_value=0.0,
        value=90_000.0,
        step=5_000.0
    )

    capex = st.number_input(
        "Annual Maintenance CapEx ($)",
        min_value=0.0,
        value=25_000.0,
        step=5_000.0
    )

    working_capital = st.number_input(
        "Additional Working Capital ($)",
        min_value=0.0,
        value=50_000.0,
        step=5_000.0
    )

    revenue_growth = st.number_input(
        "Annual Revenue Growth (%)",
        min_value=-50.0,
        max_value=100.0,
        value=3.0,
        step=0.5
    )

    st.divider()

    st.subheader("Senior Debt")

    bank_debt = st.number_input(
        "Bank / Senior Debt ($)",
        min_value=0.0,
        value=800_000.0,
        step=25_000.0
    )

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

    st.divider()

    st.subheader("Seller Financing")

    seller_financing = st.number_input(
        "Seller Financing ($)",
        min_value=0.0,
        value=100_000.0,
        step=10_000.0
    )

    seller_rate = st.number_input(
        "Seller Financing Rate (%)",
        min_value=0.0,
        max_value=30.0,
        value=5.0,
        step=0.25
    )

    seller_amortization = st.number_input(
        "Seller Amortization (Years)",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )

    st.divider()

    st.subheader("Buyer Equity")

    buyer_equity = st.number_input(
        "Buyer Equity ($)",
        min_value=0.0,
        value=300_000.0,
        step=25_000.0
    )

    st.divider()

    st.subheader("Exit")

    holding_period = st.number_input(
        "Holding Period (Years)",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )

    exit_multiple = st.number_input(
        "Exit EBITDA Multiple",
        min_value=0.5,
        max_value=20.0,
        value=4.0,
        step=0.25
    )


# ============================================================
# INPUT DICTIONARY
# ============================================================

inputs = {

    "purchase_price":
        purchase_price,

    "revenue":
        revenue,

    "sde":
        sde,

    "ebitda":
        ebitda,

    "replacement_salary":
        replacement_salary,

    "capex":
        capex,

    "working_capital":
        working_capital,

    "revenue_growth":
        revenue_growth,

    "buyer_equity":
        buyer_equity,

    "bank_debt":
        bank_debt,

    "bank_rate":
        bank_rate,

    "bank_amortization":
        bank_amortization,

    "seller_financing":
        seller_financing,

    "seller_rate":
        seller_rate,

    "seller_amortization":
        seller_amortization,

    "holding_period":
        holding_period,

    "exit_multiple":
        exit_multiple
}


# ============================================================
# RUN MODEL
# ============================================================

results = calculate_deal(inputs)


# ============================================================
# TOP-LEVEL VERDICT
# ============================================================

st.subheader("WTM Deal Verdict")

verdict = results["verdict"]
score = results["score"]

if verdict == "BUY":

    verdict_message = (
        "The deal shows attractive financial characteristics "
        "under the current assumptions."
    )

elif verdict == "NEGOTIATE":

    verdict_message = (
        "The deal may work, but price or financing terms "
        "should be improved before proceeding."
    )

else:

    verdict_message = (
        "The current price and financing structure do not "
        "provide enough margin of safety."
    )


st.markdown(
    f"""
    <div class="verdict-box">

    <div class="small-label">
    WTM DEAL SCORE
    </div>

    <div class="verdict-score">
    {score}<span style="font-size:20px;">/100</span>
    </div>

    <div class="verdict-label">
    {verdict}
    </div>

    <p>
    {verdict_message}
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KEY METRICS
# ============================================================

st.subheader("Key Acquisition Metrics")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:

    st.metric(
        "SDE Multiple",
        multiple(
            results["sde_multiple"]
        )
    )

with col2:

    st.metric(
        "EBITDA Multiple",
        multiple(
            results["ebitda_multiple"]
        )
    )

with col3:

    st.metric(
        "DSCR",
        multiple(
            results["dscr"]
        )
    )

with col4:

    st.metric(
        "Cash-on-Cash",
        pct(
            results["cash_on_cash"]
        )
    )

with col5:

    st.metric(
        "5-Year IRR",
        pct(
            results["irr"]
        )
    )

with col6:

    st.metric(
        "MOIC",
        multiple(
            results["moic"]
        )
    )


# ============================================================
# MAXIMUM OFFER
# ============================================================

st.divider()

st.subheader("WTM Maximum Offer")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Current Asking Price",
        money(
            purchase_price
        )
    )

with col2:

    st.metric(
        "WTM Maximum Offer",
        money(
            results["maximum_offer"]
        )
    )

with col3:

    difference = (
        results["maximum_offer"] -
        purchase_price
    )

    st.metric(
        "Offer vs Asking",
        money(difference)
    )


if results["maximum_offer"] < purchase_price:

    st.warning(
        f"The current asking price is "
        f"{money(purchase_price - results['maximum_offer'])} "
        f"above the WTM estimated maximum offer."
    )

else:

    st.success(
        "The asking price is within the current "
        "WTM maximum-offer estimate."
    )


# ============================================================
# SOURCES & USES
# ============================================================

st.divider()

st.subheader("Sources & Uses")

sources_uses = pd.DataFrame(
    {
        "Sources": [
            "Buyer Equity",
            "Bank / Senior Debt",
            "Seller Financing",
            "Total Sources"
        ],

        "Amount": [
            buyer_equity,
            bank_debt,
            seller_financing,
            results["total_sources"]
        ]
    }
)

uses = pd.DataFrame(
    {
        "Uses": [
            "Purchase Price",
            "Working Capital",
            "Total Uses"
        ],

        "Amount": [
            purchase_price,
            working_capital,
            results["total_uses"]
        ]
    }
)

col1, col2 = st.columns(2)

with col1:

    st.dataframe(
        sources_uses,
        hide_index=True,
        use_container_width=True
    )

with col2:

    st.dataframe(
        uses,
        hide_index=True,
        use_container_width=True
    )


if abs(results["funding_gap"]) > 1:

    if results["funding_gap"] < 0:

        st.error(
            f"Funding shortfall: "
            f"{money(abs(results['funding_gap']))}"
        )

    else:

        st.info(
            f"Excess funding: "
            f"{money(results['funding_gap'])}"
        )

else:

    st.success(
        "Sources and uses are balanced."
    )


# ============================================================
# CASH FLOW ANALYSIS
# ============================================================

st.divider()

st.subheader("Cash Flow & Debt Service")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Adjusted EBITDA",
        money(
            results["adjusted_ebitda"]
        )
    )

with col2:

    st.metric(
        "Adjusted Cash Flow",
        money(
            results["adjusted_cash_flow"]
        )
    )

with col3:

    st.metric(
        "Annual Debt Service",
        money(
            results[
                "total_annual_debt_service"
            ]
        )
    )

with col4:

    st.metric(
        "Cash Flow After Debt",
        money(
            results[
                "cash_flow_after_debt"
            ]
        )
    )


# ============================================================
# DSCR RISK
# ============================================================

st.subheader("Debt Service Coverage")

dscr = results["dscr"]

if dscr >= 1.50:

    st.success(
        f"DSCR of {dscr:.2f}× indicates strong "
        "debt-service coverage."
    )

elif dscr >= 1.25:

    st.warning(
        f"DSCR of {dscr:.2f}× is acceptable, "
        "but downside testing is important."
    )

elif dscr >= 1.00:

    st.warning(
        f"DSCR of {dscr:.2f}× provides limited "
        "margin for operating weakness."
    )

else:

    st.error(
        f"DSCR of {dscr:.2f}× indicates the business "
        "does not generate enough adjusted cash flow "
        "to cover the proposed debt service."
    )


# ============================================================
# 5-YEAR PROJECTION
# ============================================================

st.divider()

st.subheader(
    f"{holding_period}-Year Operating Projection"
)

projection = results["projection"].copy()

display_projection = projection.copy()

for column in [
    "Revenue",
    "EBITDA",
    "Adjusted Cash Flow",
    "Debt Service",
    "Cash Flow After Debt",
    "Remaining Debt"
]:

    display_projection[column] = (
        display_projection[column]
        .map(money)
    )


display_projection["DSCR"] = (
    display_projection["DSCR"]
    .map(
        lambda x:
        "N/A"
        if not np.isfinite(x)
        else f"{x:.2f}×"
    )
)

st.dataframe(
    display_projection,
    hide_index=True,
    use_container_width=True
)


# ============================================================
# CHART — REVENUE & EBITDA
# ============================================================

st.subheader("Operating Growth")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=projection["Year"],
        y=projection["Revenue"],
        mode="lines+markers",
        name="Revenue"
    )
)

fig.add_trace(
    go.Scatter(
        x=projection["Year"],
        y=projection["EBITDA"],
        mode="lines+markers",
        name="EBITDA"
    )
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="CAD",
    hovermode="x unified",
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CHART — DEBT PAYDOWN
# ============================================================

st.subheader("Debt Paydown")

fig_debt = go.Figure()

fig_debt.add_trace(
    go.Scatter(
        x=projection["Year"],
        y=projection["Remaining Debt"],
        mode="lines+markers",
        name="Remaining Debt"
    )
)

fig_debt.update_layout(
    xaxis_title="Year",
    yaxis_title="Remaining Debt",
    hovermode="x unified",
    height=350
)

st.plotly_chart(
    fig_debt,
    use_container_width=True
)


# ============================================================
# EXIT ANALYSIS
# ============================================================

st.divider()

st.subheader("Exit Analysis")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Exit EBITDA",
        money(
            projection.iloc[-1]["EBITDA"]
        )
    )

with col2:

    st.metric(
        "Exit Enterprise Value",
        money(
            results[
                "exit_enterprise_value"
            ]
        )
    )

with col3:

    st.metric(
        "Remaining Debt",
        money(
            results[
                "remaining_total_debt"
            ]
        )
    )

with col4:

    st.metric(
        "Exit Equity Value",
        money(
            results[
                "exit_equity_value"
            ]
        )
    )


# ============================================================
# RETURN ANALYSIS
# ============================================================

st.subheader("Buyer Returns")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Initial Buyer Equity",
        money(
            buyer_equity
        )
    )

with col2:

    st.metric(
        "MOIC",
        multiple(
            results["moic"]
        )
    )

with col3:

    st.metric(
        "IRR",
        pct(
            results["irr"]
        )
    )


# ============================================================
# DOWNSIDE TESTING
# ============================================================

st.divider()

st.subheader("Downside Stress Test")

downside_data = pd.DataFrame(
    {
        "Scenario": [
            "Base Case",
            "Cash Flow -10%",
            "Cash Flow -20%"
        ],

        "Adjusted Cash Flow": [
            results["adjusted_cash_flow"],
            results["adjusted_cash_flow"] * 0.90,
            results["adjusted_cash_flow"] * 0.80
        ],

        "DSCR": [
            results["dscr"],
            results["downside_10_dscr"],
            results["downside_20_dscr"]
        ]
    }
)

display_downside = downside_data.copy()

display_downside[
    "Adjusted Cash Flow"
] = (
    display_downside[
        "Adjusted Cash Flow"
    ]
    .map(money)
)

display_downside["DSCR"] = (
    display_downside["DSCR"]
    .map(
        lambda x:
        "N/A"
        if not np.isfinite(x)
        else f"{x:.2f}×"
    )
)

st.dataframe(
    display_downside,
    hide_index=True,
    use_container_width=True
)

if results["downside_20_dscr"] < 1.0:

    st.error(
        "⚠️ At a 20% cash-flow decline, the deal "
        "falls below 1.00× DSCR."
    )

elif results["downside_20_dscr"] < 1.25:

    st.warning(
        "⚠️ At a 20% cash-flow decline, debt coverage "
        "becomes thin."
    )

else:

    st.success(
        "The deal maintains strong debt coverage "
        "even under the 20% downside scenario."
    )


# ============================================================
# INVESTMENT CONCLUSION
# ============================================================

st.divider()

st.subheader("WTM Investment Conclusion")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        "### What looks good"
    )

    positive_points = []

    if dscr >= 1.50:

        positive_points.append(
            f"Strong DSCR of {dscr:.2f}×."
        )

    if np.isfinite(results["irr"]) and results["irr"] >= 0.20:

        positive_points.append(
            f"Projected IRR of {pct(results['irr'])}."
        )

    if results["sde_multiple"] <= 4:

        positive_points.append(
            f"Reasonable SDE multiple of "
            f"{multiple(results['sde_multiple'])}."
        )

    if results["downside_20_dscr"] >= 1.25:

        positive_points.append(
            "Strong resilience in the 20% downside case."
        )

    if not positive_points:

        positive_points.append(
            "No major positive signal meets the current WTM thresholds."
        )

    for point in positive_points:

        st.markdown(
            f"✓ {point}"
        )


with col2:

    st.markdown(
        "### What needs attention"
    )

    risk_points = []

    if dscr < 1.50:

        risk_points.append(
            f"Base-case DSCR is only "
            f"{dscr:.2f}×."
        )

    if results["sde_multiple"] > 4:

        risk_points.append(
            f"SDE multiple is elevated at "
            f"{multiple(results['sde_multiple'])}."
        )

    if np.isfinite(results["irr"]) and results["irr"] < 0.15:

        risk_points.append(
            f"Projected IRR is only "
            f"{pct(results['irr'])}."
        )

    if results["downside_20_dscr"] < 1.25:

        risk_points.append(
            "The deal becomes weak under a 20% downside."
        )

    if results["maximum_offer"] < purchase_price:

        risk_points.append(
            f"Asking price exceeds WTM maximum offer "
            f"by {money(purchase_price - results['maximum_offer'])}."
        )

    if not risk_points:

        risk_points.append(
            "No major risk flag triggered under the current assumptions."
        )

    for point in risk_points:

        st.markdown(
            f"⚠ {point}"
        )


# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.caption(
    """
    WTM Business Acquisition Analyzer is an educational
    financial modeling tool. It does not constitute financial,
    investment, accounting, tax, legal, lending or valuation advice.

    Results are entirely dependent on the assumptions entered
    and should be independently verified before making an
    acquisition or investment decision.
    """
)
