import streamlit as st
from fpdf import FPDF

# --- Page Configuration ---
st.set_page_config(page_title="Kalemi Law", layout="centered", page_icon="🏛️")

# --- Auto-detect Light/Dark Mode ---
st.markdown(
    """
    <style>
        @media (prefers-color-scheme: dark) {
            body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
                background-color: black;
                color: white;
            }
            h1, h2, h3, h4, h5, h6, p, div, span, label {
                color: white;
            }
        }
        @media (prefers-color-scheme: light) {
            body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
                background-color: white;
                color: black;
            }
            h1, h2, h3, h4, h5, h6, p, div, span, label {
                color: black;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Toronto Banner Image at Top ---
st.image("static/banner_highrise.png", use_container_width=True)
st.markdown("<h1 style='text-align: center; font-size: 40px;'>Kalemi Law</h1>", unsafe_allow_html=True)

# --- Ontario Cities ---
cities = [
    "Toronto", "Ottawa", "Mississauga", "Brampton", "Hamilton", "London", "Markham",
    "Vaughan", "Kitchener", "Windsor", "Richmond Hill", "Oakville", "Burlington",
    "St. Catharines", "Sudbury", "Guelph", "Kingston", "Ajax", "Whitby", "Barrie"
]

# --- Main Header ---
st.header("Ontario Land Transfer Tax & Legal Fee Calculator")

# --- Session State to manage reset ---
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- User Inputs ---
purchase_price = st.number_input("Enter the purchase price ($):", min_value=0)
city = st.selectbox("Select the City:", cities)
first_time_buyer = st.checkbox("Are you a first-time home buyer?")

# --- Calculation Functions ---
def calculate_ontario_ltt(p):
    if p <= 55000:
        return p * 0.005
    elif p <= 250000:
        return (55000 * 0.005) + (p - 55000) * 0.01
    elif p <= 400000:
        return (55000 * 0.005) + (195000 * 0.01) + (p - 250000) * 0.015
    elif p <= 2000000:
        return (55000 * 0.005) + (195000 * 0.01) + (150000 * 0.015) + (p - 400000) * 0.02
    else:
        return (55000 * 0.005) + (195000 * 0.01) + (150000 * 0.015) + (1600000 * 0.02) + (p - 2000000) * 0.025

def calculate_toronto_ltt(p):
    if p <= 55000:
        return p * 0.005
    elif p <= 250000:
        return (55000 * 0.005) + (p - 55000) * 0.01
    elif p <= 400000:
        return (55000 * 0.005) + (195000 * 0.01) + (p - 250000) * 0.015
    elif p <= 2000000:
        return (55000 * 0.005) + (195000 * 0.01) + (150000 * 0.015) + (p - 400000) * 0.02
    else:
        return (55000 * 0.005) + (195000 * 0.01) + (150000 * 0.015) + (1600000 * 0.02) + (p - 2000000) * 0.025

def first_time_buyer_rebate_ontario(p):
    return min(4000, calculate_ontario_ltt(p))

def first_time_buyer_rebate_toronto(p):
    return min(4475, calculate_toronto_ltt(p))

# --- Main Calculation ---
if st.button("Calculate Costs") or st.session_state.submitted:
    st.session_state.submitted = True
    ontario_tax = calculate_ontario_ltt(purchase_price)
    toronto_tax = 0

    if city == "Toronto":
        toronto_tax = calculate_toronto_ltt(purchase_price)

    if first_time_buyer:
        ontario_tax -= first_time_buyer_rebate_ontario(purchase_price)
        if city == "Toronto":
            toronto_tax -= first_time_buyer_rebate_toronto(purchase_price)

    legal_fee = 1500
    if purchase_price > 2000000:
        extra_millions = (purchase_price - 2000000) // 1000000
        legal_fee += 500 * (extra_millions + 1)

    total_ltt = ontario_tax + toronto_tax

    # --- Display Results ---
    st.divider()
    st.markdown("### Results:")

    st.write(f"Provincial (Ontario) Land Transfer Tax: ${ontario_tax:,.2f}")
    if city == "Toronto":
        st.write(f"Municipal (Toronto) Land Transfer Tax: ${toronto_tax:,.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Legal Fees: ${legal_fee:,.2f} + HST")
    with col2:
        st.markdown("Estimated Disbursements: $300–$500")

    st.header(f"Total Estimated Land Transfer Taxes: ${total_ltt:,.2f}")

    # --- Generate PDF Button ---
    if st.button("Download Summary as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Kalemi Law - Cost Summary", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Purchase Price: ${purchase_price:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"City: {city}", ln=True)
        pdf.cell(200, 10, txt=f"First-Time Buyer: {'Yes' if first_time_buyer else 'No'}", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Provincial (Ontario) LTT: ${ontario_tax:,.2f}", ln=True)
        if city == "Toronto":
            pdf.cell(200, 10, txt=f"Municipal (Toronto) LTT: ${toronto_tax:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Legal Fees: ${legal_fee:,.2f} + HST", ln=True)
        pdf.cell(200, 10, txt="Disbursements Estimate: $300-$500", ln=True)  # <- fixed dash here
        pdf_path = "/mnt/data/kalemi_summary.pdf"
        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button(label="Click to Download PDF", file_name="kalemi_summary.pdf", data=f, mime="application/pdf")

    # --- Reset Button ---
    if st.button("Reset Calculator"):
        st.session_state.submitted = False
        st.rerun()
