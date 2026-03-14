"""
FBO Pitch Deck Generator — Streamlit App
Fill in your deal details and download a ready-to-present PPTX in one click.
"""

import os
import streamlit as st
from generate_deck import generate_deck

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FBO Pitch Deck Generator | Funded By Others",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Branding — Google Fonts + custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800&family=Lato:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Lato', sans-serif;
    }

    /* Page headings */
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 800 !important;
        color: #2C3E50 !important;
    }

    /* Sidebar header */
    section[data-testid="stSidebar"] h2 {
        font-family: 'Montserrat', sans-serif !important;
        color: #4CAF50 !important;
    }

    /* Brand header bar */
    .vgs-header {
        background-color: #2C3E50;
        padding: 18px 28px;
        border-radius: 8px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .vgs-header-brand {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 1.5rem;
        color: #4CAF50;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .vgs-header-tagline {
        font-family: 'Lato', sans-serif;
        font-size: 0.95rem;
        color: #F2EFE8;
        margin-top: 2px;
    }
    .vgs-divider {
        border: none;
        border-top: 3px solid #4CAF50;
        margin: 0 0 20px 0;
    }

    /* Primary button */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #4CAF50 !important;
        border: none !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: 0.05em !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #E67E22 !important;
    }

    /* Download button */
    div[data-testid="stDownloadButton"] > button {
        background-color: #2C3E50 !important;
        color: #F2EFE8 !important;
        border: none !important;
        font-family: 'Lato', sans-serif !important;
        font-weight: 700 !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #E67E22 !important;
    }

    /* Tab styling */
    button[data-baseweb="tab"] {
        font-family: 'Lato', sans-serif !important;
        font-weight: 700 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #4CAF50 !important;
        border-bottom-color: #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(__file__)

TEMPLATES = {
    "Design 1 — Classic": {
        "file": "template_v1.pptx",
        "preview": "preview_v1.jpg",
        "description": "Clean, minimal layout on a light background",
    },
    "Design 2 — Rose Gold": {
        "file": "template_v2.pptx",
        "preview": "preview_v2.jpg",
        "description": "Warm rose-gold accents with a modern feel",
    },
    "Design 3 — Bold": {
        "file": "template_v3.pptx",
        "preview": "preview_v3.jpg",
        "description": "High-contrast, bold typography for impact",
    },
}

# ─────────────────────────────────────────────
# Sidebar — live financial summary
# ─────────────────────────────────────────────
def sidebar_summary(data: dict) -> None:
    purchase = float(data.get("purchase_price", 0) or 0)
    closing  = float(data.get("closing_costs",  0) or 0)
    fin_fees = float(data.get("financing_fees", 0) or 0)
    total_acq = purchase + closing + fin_fees

    rehab_keys = ["kitchen","appliances","bathrooms","flooring","windows",
                  "interior_paint","hvac","exterior_paint","landscape",
                  "contingency","permits"]
    total_rehab = sum(float(data.get(k, 0) or 0) for k in rehab_keys)

    holding_keys = ["taxes","insurance","utilities","maintenance","interest_carry"]
    total_holding = sum(float(data.get(k, 0) or 0) for k in holding_keys)

    total_cost   = total_acq + total_rehab + total_holding
    arv          = float(data.get("arv", 0) or 0)
    gross_profit = arv - total_cost
    inv_pct      = float(data.get("investor_split", 50) or 50) / 100
    op_pct       = float(data.get("operator_split",  50) or 50) / 100

    def fmt(n): return f"${n:,.0f}"
    def pct(n): return f"{n*100:.1f}%"

    st.sidebar.markdown("""
<div style="font-family:'Montserrat',sans-serif;font-weight:800;font-size:1rem;color:#4CAF50;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:4px;">Funded By Others</div>
""", unsafe_allow_html=True)
    st.sidebar.markdown("## 📊 Deal Summary")
    st.sidebar.markdown(f"**Acquisition:** {fmt(total_acq)}")
    st.sidebar.markdown(f"**Renovation:** {fmt(total_rehab)}")
    st.sidebar.markdown(f"**Holding:** {fmt(total_holding)}")
    st.sidebar.divider()
    st.sidebar.markdown(f"**Total Cost:** {fmt(total_cost)}")
    st.sidebar.markdown(f"**ARV:** {fmt(arv)}")
    color = "green" if gross_profit >= 0 else "red"
    st.sidebar.markdown(
        f"**Gross Profit:** :{color}[{fmt(gross_profit)}]"
        f" ({pct(gross_profit / arv) if arv else 'N/A'})"
    )
    st.sidebar.divider()
    st.sidebar.markdown(f"**Investor Profit ({int(inv_pct*100)}%):** {fmt(gross_profit * inv_pct)}")
    st.sidebar.markdown(f"**Operator Profit ({int(op_pct*100)}%):** {fmt(gross_profit * op_pct)}")


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="vgs-header">
    <div>
        <div class="vgs-header-brand">Funded By Others</div>
        <div class="vgs-header-tagline">FBO Pitch Deck Generator — Funded By Others</div>
    </div>
</div>
<hr class="vgs-divider"/>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Design selector
# ─────────────────────────────────────────────
st.subheader("Step 1 — Choose Your Design")

design_names = list(TEMPLATES.keys())
preview_cols = st.columns(3)
for col, name in zip(preview_cols, design_names):
    tmpl = TEMPLATES[name]
    preview_path = os.path.join(BASE_DIR, tmpl["preview"])
    with col:
        if os.path.exists(preview_path):
            st.image(preview_path, use_container_width=True)
        st.markdown(f"**{name}**")
        st.caption(tmpl["description"])

selected_design = st.radio(
    "Select design:",
    design_names,
    horizontal=True,
    label_visibility="collapsed",
)
TEMPLATE_PATH = os.path.join(BASE_DIR, TEMPLATES[selected_design]["file"])

st.divider()
st.subheader("Step 2 — Fill In Your Deal Details")

# We collect all form values into this dict
data: dict = {}

# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📍 Property",
    "🎯 Overview",
    "👤 About You",
    "📈 Track Record",
    "💵 Purchase Costs",
    "🔨 Renovation",
    "🏦 Holding Costs",
    "🏷️ ARV & Comps",
    "📌 Justification",
    "🤝 Investor",
    "📅 Timeline",
    "📞 Contact",
])

# ── Tab 1: Property ────────────────────────────────────────────────────────
with tabs[0]:
    st.subheader("Cover Slide — Property Details")
    c1, c2 = st.columns(2)
    with c1:
        street = st.text_input("Street Address", "247 Maple Ridge Drive")
        city   = st.text_input("City", "Columbus")
        state  = st.text_input("State", "Ohio")
        zipcode = st.text_input("Zip Code", "43215")
    with c2:
        prop_type = st.text_input("Property Type", "Single-Family Residential (3BR / 2BA)")
        exit_strat = st.selectbox("Exit Strategy", ["Flip", "Refinance"])

    data["full_address"]       = f"{street}, {city}, {state} {zipcode}"
    data["street_address_short"] = street
    data["property_type"]      = prop_type
    data["exit_strategy"]      = exit_strat

# ── Tab 2: Project Overview ────────────────────────────────────────────────
with tabs[1]:
    st.subheader("Project Overview — 3 Selling Points")
    st.caption("These appear on Slide 3 of the deck.")
    data["selling_point_1"] = st.text_area(
        "Selling Point 1",
        "Strong ARV-to-cost ratio with 18%+ projected gross profit margin",
        height=80,
    )
    data["selling_point_2"] = st.text_area(
        "Selling Point 2",
        "Located in high-demand zip code — comps selling in under 18 days on market",
        height=80,
    )
    data["selling_point_3"] = st.text_area(
        "Selling Point 3",
        "Contractor bids secured and permits pre-approved — ready to break ground immediately",
        height=80,
    )

# ── Tab 3: About You ───────────────────────────────────────────────────────
with tabs[2]:
    st.subheader("About You — Slide 4")
    c1, c2 = st.columns(2)
    with c1:
        data["your_name"] = st.text_input("Full Name", "James R. Mitchell")
        data["your_role"] = st.text_input("Title / Role", "Managing Partner")
    with c2:
        st.caption("These four statements appear in the credential boxes.")
    data["cred_1"] = st.text_area(
        "Credential Box 1",
        "Over $3.2M in residential transactions closed in the past 4 years across Central Ohio",
        height=80,
    )
    data["cred_2"] = st.text_area(
        "Credential Box 2",
        "12 fix-and-flip projects exited with an average 23% gross profit and zero investor capital losses",
        height=80,
    )
    data["cred_3"] = st.text_area(
        "Credential Box 3",
        "Deep relationships with licensed contractors, title companies, and private lenders for faster closings",
        height=80,
    )
    data["cred_4"] = st.text_area(
        "Credential Box 4",
        "Licensed Ohio Real Estate Agent | Certified Residential Specialist (CRS)",
        height=80,
    )

# ── Tab 4: Track Record ────────────────────────────────────────────────────
with tabs[3]:
    st.subheader("Track Record — Up to 5 Past Deals (Slide 5)")
    st.caption("Fill in as many deals as you have. Leave rows blank to keep the template examples.")

    deals = []
    for i in range(5):
        with st.expander(f"Deal {i+1}", expanded=(i == 0)):
            c1, c2, c3 = st.columns(3)
            with c1:
                street_d = st.text_input("Street Address", key=f"d{i}_street",
                                         placeholder="412 Elmwood Ave")
                city_state = st.text_input("City, State", key=f"d{i}_city",
                                           placeholder="Columbus, OH 43219")
                year = st.text_input("Year of Sale", key=f"d{i}_year", placeholder="2024")
            with c2:
                hold_months = st.text_input("Hold Time (Months)", key=f"d{i}_hold", placeholder="7")
                purchase_p  = st.number_input("Purchase Price ($)", key=f"d{i}_purchase",
                                              min_value=0, value=0, step=1000)
                rehab_c     = st.number_input("Rehab, Carrying & Selling Costs ($)", key=f"d{i}_rehab",
                                              min_value=0, value=0, step=1000)
            with c3:
                sale_p = st.number_input("Sale Price ($)", key=f"d{i}_sale",
                                         min_value=0, value=0, step=1000)
                if purchase_p + rehab_c > 0:
                    total_inv = purchase_p + rehab_c
                    gp = ((sale_p - total_inv) / total_inv * 100) if total_inv else 0
                    st.metric("Gross Profit %", f"{gp:.1f}%")

            if street_d:  # only add if the user filled something in
                deals.append({
                    "street": street_d,
                    "city_state": city_state,
                    "year": year,
                    "hold_months": hold_months,
                    "purchase_price": purchase_p,
                    "rehab_costs": rehab_c,
                    "sale_price": sale_p,
                })

    data["deals"] = deals

# ── Tab 5: Purchase Costs ──────────────────────────────────────────────────
with tabs[4]:
    st.subheader("Purchase Costs — Slide 6")
    c1, c2 = st.columns(2)
    with c1:
        data["purchase_price"] = st.number_input("Purchase Price ($)", min_value=0, value=180000, step=1000)
        data["closing_costs"]  = st.number_input("Closing Costs ($)",  min_value=0, value=4500,  step=500)
        data["financing_fees"] = st.number_input("Financing Fees ($)", min_value=0, value=6300,  step=500)
    with c2:
        total_acq = (
            float(data["purchase_price"]) +
            float(data["closing_costs"]) +
            float(data["financing_fees"])
        )
        st.metric("Total Acquisition Cost", f"${total_acq:,.0f}")

# ── Tab 6: Renovation Budget ───────────────────────────────────────────────
with tabs[5]:
    st.subheader("Renovation Budget — Slide 8")
    c1, c2 = st.columns(2)
    with c1:
        data["kitchen"]       = st.number_input("Kitchen ($)",              min_value=0, value=18000, step=500)
        data["appliances"]    = st.number_input("Appliances ($)",           min_value=0, value=4500,  step=500)
        data["bathrooms"]     = st.number_input("Bathrooms ($)",            min_value=0, value=12000, step=500)
        data["flooring"]      = st.number_input("Flooring ($)",             min_value=0, value=8500,  step=500)
        data["windows"]       = st.number_input("Windows ($)",              min_value=0, value=5000,  step=500)
        data["interior_paint"]= st.number_input("Interior Paint & Trim ($)",min_value=0, value=4000,  step=500)
    with c2:
        data["hvac"]          = st.number_input("HVAC / Electrical / Plumbing ($)", min_value=0, value=9000,  step=500)
        data["exterior_paint"]= st.number_input("Exterior Paint ($)",       min_value=0, value=2500,  step=500)
        data["landscape"]     = st.number_input("Landscape ($)",            min_value=0, value=2000,  step=500)
        data["contingency"]   = st.number_input("Contingency ($)",          min_value=0, value=4500,  step=500)
        data["permits"]       = st.number_input("Permits ($)",              min_value=0, value=1200,  step=100)
        rehab_keys = ["kitchen","appliances","bathrooms","flooring","windows",
                      "interior_paint","hvac","exterior_paint","landscape",
                      "contingency","permits"]
        total_r = sum(float(data.get(k, 0) or 0) for k in rehab_keys)
        st.metric("Total Rehab Cost", f"${total_r:,.0f}")

# ── Tab 7: Holding Costs ───────────────────────────────────────────────────
with tabs[6]:
    st.subheader("Holding & Soft Costs — Slide 9")
    c1, c2 = st.columns(2)
    with c1:
        data["taxes"]         = st.number_input("Taxes ($)",          min_value=0, value=1800,  step=100)
        data["insurance"]     = st.number_input("Insurance ($)",      min_value=0, value=950,   step=100)
        data["utilities"]     = st.number_input("Utilities ($)",      min_value=0, value=1400,  step=100)
    with c2:
        data["maintenance"]   = st.number_input("Maintenance ($)",    min_value=0, value=600,   step=100)
        data["interest_carry"]= st.number_input("Interest Carry ($)", min_value=0, value=7560,  step=100)
        holding_keys = ["taxes","insurance","utilities","maintenance","interest_carry"]
        total_h = sum(float(data.get(k, 0) or 0) for k in holding_keys)
        st.metric("Total Holding Cost", f"${total_h:,.0f}")

# ── Tab 8: ARV & Comps ────────────────────────────────────────────────────
with tabs[7]:
    st.subheader("After Repair Value & Comparable Sales — Slides 11 & 13")
    data["arv"] = st.number_input(
        "Target Sale Price / ARV ($)", min_value=0, value=325000, step=1000,
        help="This appears on the ARV slide and drives all profit calculations."
    )

    st.markdown("#### Neighborhood Comps (up to 5)")
    st.caption("Fill in as many comps as you have. Leave rows blank to use the template examples.")

    comps = []
    for i in range(5):
        with st.expander(f"Comp {i+1}", expanded=(i == 0)):
            c1, c2, c3 = st.columns(3)
            with c1:
                addr    = st.text_input("Address",        key=f"comp{i}_addr",  placeholder="319 Maple Ridge Dr")
                cs      = st.text_input("City, State",    key=f"comp{i}_cs",    placeholder="Columbus, OH 43215")
                sold_dt = st.text_input("Sold Date",      key=f"comp{i}_date",  placeholder="01/15/2025")
            with c2:
                beds    = st.text_input("Bedrooms",       key=f"comp{i}_beds",  placeholder="3")
                baths   = st.text_input("Baths",          key=f"comp{i}_baths", placeholder="2")
                garage  = st.text_input("Garage Spaces",  key=f"comp{i}_gar",   placeholder="1")
            with c3:
                dom     = st.text_input("Days on Market", key=f"comp{i}_dom",   placeholder="12")
                sale_p  = st.number_input("Sale Price ($)", key=f"comp{i}_sale",
                                          min_value=0, value=0, step=1000)

            if addr:
                comps.append({
                    "address": addr, "city_state": cs, "sold_date": sold_dt,
                    "bedrooms": beds, "baths": baths, "garage": garage,
                    "dom": dom, "sale_price": sale_p,
                })

    data["comps"] = comps

# ── Tab 9: Justification ──────────────────────────────────────────────────
with tabs[8]:
    st.subheader("Property & Location Justification — Slide 12")
    st.markdown("**Why this property is a good investment:**")
    data["prop_reason_1"] = st.text_area("Reason 1",
        "Strong bones — roof replaced 2018, foundation inspection cleared, no structural concerns.",
        height=80)
    data["prop_reason_2"] = st.text_area("Reason 2",
        "3BR/2BA layout is the most in-demand configuration in this price range, maximizing buyer pool.",
        height=80)
    data["prop_reason_3"] = st.text_area("Reason 3",
        "Cosmetic-heavy rehab keeps costs predictable with minimal risk of hidden structural surprises.",
        height=80)

    st.markdown("**Why this location is a good investment:**")
    data["loc_reason_1"] = st.text_area("Location Reason 1",
        "Columbus metro area is among the top 5 fastest-growing markets in the Midwest with 3.2% YoY population growth.",
        height=80)
    data["loc_reason_2"] = st.text_area("Location Reason 2",
        "Top-rated school district with an 8/10 GreatSchools rating — a major driver for family buyers.",
        height=80)
    data["loc_reason_3"] = st.text_area("Location Reason 3",
        "Average days on market for comps in this zip code is under 18 days, reflecting strong buyer demand.",
        height=80)

# ── Tab 10: Investor Structure ─────────────────────────────────────────────
with tabs[9]:
    st.subheader("Investor Structure — Slide 15")
    c1, c2 = st.columns(2)
    with c1:
        data["capital_needed"] = st.number_input(
            "Capital Needed from Investor ($)", min_value=0, value=190800, step=1000
        )
        data["investor_split"] = st.slider("Investor Split (%)", 0, 100, 50, 5)
        data["operator_split"] = 100 - data["investor_split"]
        st.caption(f"Operator split: {data['operator_split']}%")
    with c2:
        arv_v       = float(data.get("arv", 0) or 0)
        total_cost_v = (
            float(data.get("purchase_price", 0) or 0) +
            float(data.get("closing_costs", 0) or 0) +
            float(data.get("financing_fees", 0) or 0) +
            sum(float(data.get(k, 0) or 0) for k in
                ["kitchen","appliances","bathrooms","flooring","windows",
                 "interior_paint","hvac","exterior_paint","landscape",
                 "contingency","permits",
                 "taxes","insurance","utilities","maintenance","interest_carry"])
        )
        gp = arv_v - total_cost_v
        st.metric("Projected Gross Profit", f"${gp:,.0f}")
        st.metric("Investor Profit", f"${gp * data['investor_split']/100:,.0f}")
        st.metric("Operator Profit", f"${gp * data['operator_split']/100:,.0f}")

# ── Tab 11: Timeline ──────────────────────────────────────────────────────
with tabs[10]:
    st.subheader("Exit Strategy & Timeline — Slide 16")
    c1, c2, c3 = st.columns(3)
    with c1:
        data["reno_months"] = st.number_input("Renovation Timeline (Months)", min_value=1, value=4)
    with c2:
        data["list_sell_months"] = st.number_input("List & Sell Timeframe (Months)", min_value=1, value=2)
    with c3:
        data["total_hold_months"] = int(data["reno_months"]) + int(data["list_sell_months"])
        st.metric("Total Estimated Hold", f"{data['total_hold_months']} months")

# ── Tab 12: Contact ────────────────────────────────────────────────────────
with tabs[11]:
    st.subheader("Contact Information — Slide 17")
    c1, c2 = st.columns(2)
    with c1:
        data["phone"]            = st.text_input("Phone Number", "(614) 555-0192")
        data["email"]            = st.text_input("Email", "james@mitchellreinvestments.com")
        data["website"]          = st.text_input("Website", "www.mitchellreinvestments.com")
    with c2:
        data["business_location"]  = st.text_input("Business Location", "1200 Dublin Rd, Suite 210, Columbus, OH 43215")
        data["office_hours_days"]  = st.text_input("Office Hours — Days", "Monday-Friday")
        data["office_hours_times"] = st.text_input("Office Hours — Times", "09.00-17.00")

# ─────────────────────────────────────────────
# Live sidebar summary
# ─────────────────────────────────────────────
sidebar_summary(data)

# ─────────────────────────────────────────────
# Generate button
# ─────────────────────────────────────────────
st.divider()
st.subheader("Generate Your Pitch Deck")

if not os.path.exists(TEMPLATE_PATH):
    st.error(f"⚠️ Template file not found: `{TEMPLATES[selected_design]['file']}`. Make sure all three template files are in the same folder as `app.py`.")
else:
    st.markdown(f"*Generating with: **{selected_design}***")
    if st.button("Generate Deck", type="primary", use_container_width=True):
        with st.spinner("Building your deck…"):
            pptx_bytes = generate_deck(TEMPLATE_PATH, data)

        address_slug = data.get("full_address", "pitch_deck").replace(", ", "_").replace(" ", "_")[:40]
        design_slug = selected_design.split("—")[0].strip().replace(" ", "_")
        filename = f"{address_slug}_{design_slug}_Pitch_Deck.pptx"

        st.success("✅ Your deck is ready!")
        st.download_button(
            label="⬇️ Download Pitch Deck",
            data=pptx_bytes,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
        )
        st.info(
            "💡 **Next steps:** Download the file, then upload it to Google Slides "
            "(File → Import slides) or open directly in PowerPoint."
        )

st.markdown("""
<br>
<div style="text-align:center; font-family:'Lato',sans-serif; font-size:0.8rem; color:#2C3E50; opacity:0.6; padding-top:20px;">
    Powered by <strong>Funded By Others</strong> · videogrowthsystems.com
</div>
""", unsafe_allow_html=True)
