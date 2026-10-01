"""
app.py - Streamlit Frontend for LegalEase
AI-Powered Legal Document Generator with FastAPI Backend Integration.
Supports English & Tamil legal drafting with instant PDF and DOCX export.
"""

import os
import io
import requests
import streamlit as st
from datetime import datetime, date
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# Import local fallback exporters & templates for standalone resilience
from document_templates import DOCUMENT_TYPES, build_legal_document
from pdf_exporter import create_pdf_from_text
from docx_exporter import create_docx_from_text

# Backend URL configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

# Page Configuration
st.set_page_config(
    page_title="LegalEase - AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for a Professional Legal-Tech Aesthetic
st.markdown("""
<style>
    /* Global Base */
    .main {
        background-color: #f8fafc;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #1e3a8a 100%);
        color: white;
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-tag {
        display: inline-block;
        background: rgba(59, 130, 246, 0.2);
        color: #93c5fd;
        border: 1px solid rgba(147, 197, 253, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0 0 10px 0;
        color: #ffffff;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        max-width: 780px;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Feature Cards */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.4rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }
    
    .feature-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.4rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #64748b;
        line-height: 1.5;
    }

    /* Paper Document Preview */
    .legal-document-paper {
        background-color: #ffffff;
        color: #1e293b;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        padding: 2.5rem;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.07);
        font-family: 'Courier New', Courier, monospace;
        white-space: pre-wrap;
        line-height: 1.65;
        font-size: 0.95rem;
        max-height: 650px;
        overflow-y: auto;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 12px;
    }
    
    .badge-primary {
        background: #e0f2fe;
        color: #0369a1;
        border: 1px solid #bae6fd;
    }
    
    .badge-success {
        background: #dcfce7;
        color: #15803d;
        border: 1px solid #bbf7d0;
    }
    
    .badge-ai {
        background: #ede9fe;
        color: #6d28d9;
        border: 1px solid #ddd6fe;
    }

    .legal-footer {
        text-align: center;
        padding: 2rem 0;
        color: #94a3b8;
        font-size: 0.85rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)


# Helper function to check Backend Status
def check_backend_status():
    try:
        res = requests.get(f"{BACKEND_URL}/api/health", timeout=1.5)
        if res.status_code == 200:
            return True, res.json().get("gemini_configured", False)
    except Exception:
        pass
    return False, False


# Initialize Session States
if "generated_doc" not in st.session_state:
    st.session_state.generated_doc = None
if "doc_title" not in st.session_state:
    st.session_state.doc_title = ""
if "doc_lang" not in st.session_state:
    st.session_state.doc_lang = "en"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "source_type" not in st.session_state:
    st.session_state.source_type = "template"


# Check backend availability
backend_online, gemini_active = check_backend_status()


# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/scales.png", width=60)
    st.title("LegalEase")
    st.caption("AI-Powered Legal Document Generator")
    st.markdown("---")

    nav_selection = st.radio(
        "Navigation",
        options=["🏠 Home", "⚖️ Document Generator", "ℹ️ About & Help"],
        index=0 if st.session_state.current_page == "Home" else 1 if st.session_state.current_page == "Generator" else 2
    )

    if nav_selection == "🏠 Home":
        st.session_state.current_page = "Home"
    elif nav_selection == "⚖️ Document Generator":
        st.session_state.current_page = "Generator"
    else:
        st.session_state.current_page = "About"

    st.markdown("---")
    
    # Backend & AI Status Indicator
    st.markdown("### 🔌 System Status")
    if backend_online:
        if gemini_active:
            st.success("🟢 **FastAPI:** Online\n\n✨ **Gemini AI:** Active")
        else:
            st.info("🟢 **FastAPI:** Online\n\n📝 **Engine:** Template Mode\n*(Add `GEMINI_API_KEY` in `.env` for AI)*")
    else:
        st.warning("⚪ **FastAPI:** Offline\n\n⚡ **Fallback:** Built-in Engine Active\n*(Run `uvicorn backend:app`)*")

    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.markdown(
        "- **Dual Language:** Generate in English or தமிழ்.\n"
        "- **Signatures:** Ensure party names match government IDs.\n"
        "- **Stamp Duty:** Print on appropriate Non-Judicial stamp paper."
    )
    
    st.markdown("---")
    st.markdown(
        "<div style='font-size: 0.75rem; color: #94a3b8;'>LegalEase v1.0 • Streamlit + FastAPI</div>",
        unsafe_allow_html=True
    )


# ==============================================================================
# PAGE 1: HOME PAGE
# ==============================================================================
if st.session_state.current_page == "Home":
    st.markdown("""
    <div class="hero-banner">
        <span class="hero-tag">AI-Powered Legal Tech • FastAPI & Streamlit</span>
        <h1 class="hero-title">LegalEase</h1>
        <p class="hero-subtitle">
            Draft legally structured agreements, contracts, and sworn affidavits in seconds.
            Powered by Google Gemini AI with complete bilingual support in 
            <strong>English</strong> and <strong>தமிழ் (Tamil)</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Call to action
    col_cta1, col_cta2 = st.columns([1, 4])
    with col_cta1:
        if st.button("🚀 Start Drafting Now", type="primary", use_container_width=True):
            st.session_state.current_page = "Generator"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Key Features
    st.subheader("Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✨</div>
            <div class="feature-title">Gemini AI Powered</div>
            <div class="feature-desc">
                Intelligently incorporates your specific financial terms, custom clauses, and jurisdiction into a formal legal document.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <div class="feature-title">English & தமிழ் Support</div>
            <div class="feature-desc">
                Generate authentic bilingual legal drafting in either English or formal court Tamil (வாடகை ஒப்பந்தம், ரகசிய காப்பு ஒப்பந்தம்).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📑</div>
            <div class="feature-title">PDF & DOCX Export</div>
            <div class="feature-desc">
                Download court-ready printable PDFs or fully editable Microsoft Word (.docx) files ready for signing and stamp paper.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Supported Documents Showcase
    st.subheader("Supported Legal Document Types")
    doc_cols = st.columns(3)
    
    docs_info = [
        ("🏠 Rental Agreement", "Residential lease with deposit, monthly rent, utilities, and termination notice.", "வாடகை ஒப்பந்தம்"),
        ("🔒 Non-Disclosure Agreement", "Mutual or unilateral confidentiality clauses safeguarding proprietary info.", "ரகசிய காப்பு ஒப்பந்தம்"),
        ("📜 General Affidavit", "Sworn legal declaration suitable for notary attestation and government filings.", "பொது உறுதிமொழி"),
        ("💻 Freelance Service Contract", "Scope of work, milestone payments, delivery timeline, and IP assignment.", "சேவை ஒப்பந்தம்"),
        ("💼 Employment Offer Letter", "Designation, annual CTC, probation period, and standard corporate terms.", "பணி நியமனக் கடிதம்"),
        ("💵 Promissory Note", "Legally binding debt acknowledgment with principal, interest, and demand terms.", "கடன் உறுதிப்பத்திரம்"),
    ]

    for idx, (title, desc, ta_title) in enumerate(docs_info):
        col_target = doc_cols[idx % 3]
        with col_target:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.2rem; margin-bottom: 1.2rem;">
                <h4 style="margin: 0 0 6px 0; color: #1e293b; font-size: 1.05rem;">{title}</h4>
                <div style="font-size: 0.8rem; color: #2563eb; font-weight: 600; margin-bottom: 8px;">{ta_title}</div>
                <p style="font-size: 0.85rem; color: #64748b; margin: 0; line-height: 1.4;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Architecture Overview
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("How It Works: Streamlit + FastAPI Architecture")
    arc1, arc2, arc3 = st.columns(3)
    with arc1:
        st.markdown("### 1. Interactive Frontend\nEnter details in the Streamlit UI with live bilingual switching.")
    with arc2:
        st.markdown("### 2. FastAPI + Gemini\nBackend receives parameters and drafts the document via Gemini AI.")
    with arc3:
        st.markdown("### 3. Instant Document Export\nPreview the document live and export to court-formatted PDF or Word DOCX.")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.caption(
        "⚠️ **Legal Notice**: LegalEase provides automated legal drafting assistance. "
        "It does not substitute formal legal advice. Please review finalized documents "
        "with an advocate before notarization or registration."
    )


# ==============================================================================
# PAGE 2: LEGAL DOCUMENT GENERATOR
# ==============================================================================
elif st.session_state.current_page == "Generator":
    st.markdown("## ⚖️ Legal Document Generator")
    st.write("Complete the details below to generate your customized legal document.")

    # 1. Language & Document Type Selection
    st.markdown("#### 1. Language & Document Type")
    col_lang, col_type = st.columns([1, 2])

    with col_lang:
        language_option = st.radio(
            "Select Language / மொழியைத் தேர்ந்தெடுக்கவும்:",
            options=["English", "தமிழ் (Tamil)"],
            horizontal=True,
            index=0 if st.session_state.doc_lang == "en" else 1
        )
        current_lang = "ta" if "Tamil" in language_option else "en"
        st.session_state.doc_lang = current_lang

    with col_type:
        doc_type_keys = list(DOCUMENT_TYPES.keys())
        doc_type_labels = [
            f"{k} ({DOCUMENT_TYPES[k]['ta']})" if current_lang == "ta" else k
            for k in doc_type_keys
        ]
        selected_index = st.selectbox(
            "Select Document Type / ஆவண வகையைத் தேர்ந்தெடுக்கவும்:",
            options=range(len(doc_type_keys)),
            format_func=lambda i: doc_type_labels[i]
        )
        selected_doc_type = doc_type_keys[selected_index]

    is_ta = (current_lang == "ta")
    st.markdown("---")

    # 2. Name & Address Inputs
    st.markdown("#### 2. Parties Information")
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown(f"**{'முதல் தரப்பினர் விவரம்' if is_ta else 'First Party Details'}**")
        party1_label = "முதல் தரப்பினர் பெயர் (உரிமையாளர் / முதலாளி / கடன் கொடுத்தவர்):" if is_ta else "Full Name (e.g. Landlord / Employer / Discloser / Lender):"
        party1_name = st.text_input(
            party1_label,
            placeholder="e.g. R. Sundaram",
            key="p1_name"
        )
        party1_addr_label = "முதல் தரப்பினர் முகவரி:" if is_ta else "Full Address:"
        party1_address = st.text_area(
            party1_addr_label,
            placeholder="e.g. No. 12, Anna Salai, T. Nagar, Chennai - 600017",
            height=85,
            key="p1_addr"
        )

    with col_p2:
        st.markdown(f"**{'இரண்டாம் தரப்பினர் விவரம்' if is_ta else 'Second Party Details'}**")
        party2_label = "இரண்டாம் தரப்பினர் பெயர் (வாடகைதாரர் / பணியாளர் / கடன் பெற்றவர்):" if is_ta else "Full Name (e.g. Tenant / Employee / Recipient / Borrower):"
        party2_name = st.text_input(
            party2_label,
            placeholder="e.g. K. Vignesh",
            key="p2_name"
        )
        party2_addr_label = "இரண்டாம் தரப்பினர் முகவரி:" if is_ta else "Full Address:"
        party2_address = st.text_area(
            party2_addr_label,
            placeholder="e.g. Flat 3B, Sunshine Apartments, Velachery, Chennai - 600042",
            height=85,
            key="p2_addr"
        )

    st.markdown("---")
    st.markdown("#### 3. Legal Requirements & Specific Terms")

    # Dictionary for API request payload
    req_payload = {
        "doc_type": selected_doc_type,
        "language": current_lang,
        "party1_name": party1_name.strip() or ("முதல் தரப்பினர்" if is_ta else "First Party Name"),
        "party1_address": party1_address.strip() or ("முகவரி" if is_ta else "First Party Address"),
        "party2_name": party2_name.strip() or ("இரண்டாம் தரப்பினர்" if is_ta else "Second Party Name"),
        "party2_address": party2_address.strip() or ("முகவரி" if is_ta else "Second Party Address"),
    }

    col_date, col_jurisdiction = st.columns(2)
    with col_date:
        exec_date = st.date_input("Date of Execution / ஒப்பந்தத் தேதி:", value=date.today())
        req_payload["date"] = exec_date.strftime("%d %B, %Y")

    with col_jurisdiction:
        jurisdiction_val = st.text_input(
            "Jurisdiction / Court City / சட்ட எல்லை:",
            value="Chennai, Tamil Nadu" if is_ta else "Chennai, India"
        )
        req_payload["jurisdiction"] = jurisdiction_val

    # Dynamic document specific fields
    requirements_summary = []

    if selected_doc_type == "Rental Agreement":
        st.markdown("##### 🏠 Rental Agreement Details")
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            rent = st.text_input("Monthly Rent (₹) / மாதாந்திர வாடகை:", value="15,000")
            req_payload["rent_amount"] = rent
            requirements_summary.append(f"Monthly Rent: ₹{rent}")
        with rc2:
            deposit = st.text_input("Security Deposit (₹) / முன்வைப்புத் தொகை:", value="50,000")
            req_payload["deposit_amount"] = deposit
            requirements_summary.append(f"Security Deposit: ₹{deposit}")
        with rc3:
            duration = st.selectbox("Duration (Months) / கால அளவு:", ["11", "24", "36", "6"], index=0)
            req_payload["duration_months"] = duration
            requirements_summary.append(f"Tenancy Duration: {duration} months")
        
        rc4, rc5 = st.columns([1, 2])
        with rc4:
            notice = st.selectbox("Notice Period (Months) / முன்னறிவிப்பு:", ["1", "2", "3"], index=0)
            req_payload["notice_period_months"] = notice
        with rc5:
            p_addr = st.text_input("Rented Property Address / வாடகை வீடு முகவரி:", value=party1_address or "Same as Landlord Address")
            req_payload["property_address"] = p_addr
            requirements_summary.append(f"Property Address: {p_addr}")

    elif selected_doc_type == "Non-Disclosure Agreement (NDA)":
        st.markdown("##### 🔒 Non-Disclosure Terms")
        nc1, nc2 = st.columns([2, 1])
        with nc1:
            purpose = st.text_area(
                "Purpose of Disclosure / ரகசியத் தகவல் பகிர்வின் நோக்கம்:",
                value="Evaluation of business partnership, product integration, and software development collaboration."
            )
            req_payload["nda_purpose"] = purpose
            requirements_summary.append(f"Purpose: {purpose}")
        with nc2:
            period = st.selectbox("Confidentiality Term / காப்பு கால அளவு:", ["2", "3", "5", "Indefinite"], index=0)
            req_payload["nda_period"] = period
            requirements_summary.append(f"Confidentiality Duration: {period} years")

    elif selected_doc_type == "General Affidavit":
        st.markdown("##### 📜 Affidavit Details")
        ac1, ac2 = st.columns(2)
        with ac1:
            ps = st.text_input("Father / Mother / Spouse Name / தந்தை அல்லது கணவர் பெயர்:", value="S. Ramasamy")
            req_payload["deponent_parent_spouse"] = ps
            age = st.text_input("Deponent Age / வயது:", value="32")
            req_payload["deponent_age"] = age
            requirements_summary.append(f"Deponent Father/Spouse: {ps}, Age: {age}")
        with ac2:
            aff_purpose = st.text_input("Official Purpose / சமர்ப்பிக்கும் நோக்கம்:", value="Name variation clarification for passport & official records")
            req_payload["affidavit_purpose"] = aff_purpose
            requirements_summary.append(f"Purpose: {aff_purpose}")
        
        aff_stmt = st.text_area(
            "Sworn Statement of Facts / உறுதிமொழி அறிக்கை விவரம்:",
            value="I solemnly affirm that all personal information and credentials provided are true and accurate to the best of my knowledge.",
            height=100
        )
        req_payload["affidavit_statement"] = aff_stmt
        requirements_summary.append(f"Sworn Statement: {aff_stmt}")

    elif selected_doc_type == "Freelance Service Agreement":
        st.markdown("##### 💻 Freelance Service Terms")
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            fee = st.text_input("Total Project Fee (₹) / மொத்த கட்டணம்:", value="45,000")
            req_payload["service_fee"] = fee
            requirements_summary.append(f"Fee: ₹{fee}")
        with fc2:
            deadline = st.text_input("Delivery Deadline / நிறைவு நாள்:", value="30 Days from signing")
            req_payload["service_deadline"] = deadline
            requirements_summary.append(f"Deadline: {deadline}")
        with fc3:
            scope = st.text_input("Scope of Work / பணியின் சுருக்கம்:", value="Full-stack web application development & deployment")
            req_payload["service_scope"] = scope
            requirements_summary.append(f"Scope: {scope}")

    elif selected_doc_type == "Employment Offer Letter":
        st.markdown("##### 💼 Employment Terms")
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            job = st.text_input("Job Designation / பதவி:", value="Software Engineer")
            req_payload["job_title"] = job
            requirements_summary.append(f"Designation: {job}")
        with ec2:
            ctc = st.text_input("Annual CTC (₹) / ஆண்டு ஊதியம்:", value="6,50,000")
            req_payload["annual_ctc"] = ctc
            requirements_summary.append(f"Annual CTC: ₹{ctc}")
        with ec3:
            prob = st.selectbox("Probation Period (Months) / தகுதிகாண் காலம்:", ["3", "6", "1"], index=0)
            req_payload["probation_months"] = prob
            requirements_summary.append(f"Probation: {prob} months")
        jdate = st.text_input("Date of Joining / பணியில் இணையும் தேதி:", value="1st of next month")
        req_payload["joining_date"] = jdate

    elif selected_doc_type == "Promissory Note":
        st.markdown("##### 💵 Promissory Note Terms")
        pc1, pc2 = st.columns(2)
        with pc1:
            lamt = st.text_input("Principal Loan Amount (₹) / கடன் தொகை:", value="1,00,000")
            req_payload["loan_amount"] = lamt
            requirements_summary.append(f"Loan Amount: ₹{lamt}")
        with pc2:
            irate = st.text_input("Annual Interest Rate (%) / ஆண்டு வட்டி விகிதம்:", value="12")
            req_payload["interest_rate"] = irate
            requirements_summary.append(f"Interest Rate: {irate}% per annum")

    # Extra custom clauses
    st.markdown(f"**{'கூடுதல் நிபந்தனைகள் / சிறப்பு ஷரத்துக்கள்' if is_ta else 'Additional Terms / Custom Legal Requirements'}**")
    extra_terms_val = st.text_area(
        "Enter any extra conditions or specific instructions (Optional):",
        placeholder="e.g. Painting charges of ₹5,000 shall be deducted upon vacating / Non-compete clause applies for 6 months.",
        height=75
    )
    req_payload["extra_terms"] = extra_terms_val
    req_payload["requirements"] = "\n".join(requirements_summary)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Generate Document Button
    btn_col1, btn_col2 = st.columns([1, 3])
    with btn_col1:
        generate_clicked = st.button("✨ Generate Document", type="primary", use_container_width=True)

    if generate_clicked:
        with st.spinner("Drafting legal document via LegalEase Engine..."):
            doc_generated = False
            
            # Step A: Try calling FastAPI backend
            if backend_online:
                try:
                    res = requests.post(f"{BACKEND_URL}/api/generate", json=req_payload, timeout=25)
                    if res.status_code == 200:
                        data_res = res.json()
                        st.session_state.generated_doc = data_res.get("document", "")
                        st.session_state.doc_title = data_res.get("title", selected_doc_type)
                        st.session_state.source_type = data_res.get("source", "gemini_ai")
                        doc_generated = True
                except Exception as ex:
                    st.warning(f"Backend call encountered: {ex}. Switching to standalone engine.")

            # Step B: Fallback to local template generator
            if not doc_generated:
                local_text = build_legal_document(
                    doc_type=selected_doc_type,
                    data=req_payload,
                    lang=current_lang
                )
                st.session_state.generated_doc = local_text
                title_dict = DOCUMENT_TYPES.get(selected_doc_type, {"en": selected_doc_type, "ta": selected_doc_type})
                st.session_state.doc_title = title_dict["ta"] if is_ta else title_dict["en"]
                st.session_state.source_type = "local_template"

            st.success("🎉 Document generated successfully! Review and download below.")

    # ==============================================================================
    # 5. DISPLAY GENERATED DOCUMENT & DOWNLOAD BUTTONS
    # ==============================================================================
    if st.session_state.generated_doc:
        st.markdown("---")
        st.markdown("### 4. Generated Legal Document Preview")

        # Badges Summary
        word_count = len(st.session_state.generated_doc.split())
        lang_badge_text = "Language: தமிழ் (Tamil)" if st.session_state.doc_lang == "ta" else "Language: English"
        source_label = "✨ Generated via Gemini AI" if "gemini" in st.session_state.source_type else "📄 Legal Conveyancing Engine"

        st.markdown(f"""
        <div>
            <span class="status-badge badge-primary">📄 {st.session_state.doc_title}</span>
            <span class="status-badge badge-success">🌐 {lang_badge_text}</span>
            <span class="status-badge badge-ai">{source_label}</span>
            <span class="status-badge badge-primary">✍️ {word_count} Words</span>
        </div>
        """, unsafe_allow_html=True)

        # Download Buttons Row
        col_pdf, col_docx, col_space = st.columns([1, 1, 2])

        # PDF Buffer Generation
        pdf_bytes = None
        # Try backend PDF endpoint first if online
        if backend_online:
            try:
                res_pdf = requests.post(
                    f"{BACKEND_URL}/api/export/pdf",
                    json={
                        "title": st.session_state.doc_title,
                        "content": st.session_state.generated_doc,
                        "language": st.session_state.doc_lang
                    },
                    timeout=10
                )
                if res_pdf.status_code == 200:
                    pdf_bytes = res_pdf.content
            except Exception:
                pass

        # Standalone PDF fallback
        if not pdf_bytes:
            pdf_buf = create_pdf_from_text(
                title=st.session_state.doc_title,
                text_content=st.session_state.generated_doc,
                language=st.session_state.doc_lang
            )
            pdf_bytes = pdf_buf.getvalue()

        with col_pdf:
            st.download_button(
                label="📥 Download as PDF",
                data=pdf_bytes,
                file_name=f"LegalEase_{selected_doc_type.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # DOCX Buffer Generation
        docx_bytes = None
        # Try backend DOCX endpoint first if online
        if backend_online:
            try:
                res_docx = requests.post(
                    f"{BACKEND_URL}/api/export/docx",
                    json={
                        "title": st.session_state.doc_title,
                        "content": st.session_state.generated_doc,
                        "language": st.session_state.doc_lang
                    },
                    timeout=10
                )
                if res_docx.status_code == 200:
                    docx_bytes = res_docx.content
            except Exception:
                pass

        # Standalone DOCX fallback
        if not docx_bytes:
            docx_buf = create_docx_from_text(
                title=st.session_state.doc_title,
                text_content=st.session_state.generated_doc,
                language=st.session_state.doc_lang
            )
            docx_bytes = docx_buf.getvalue()

        with col_docx:
            st.download_button(
                label="📥 Download as DOCX",
                data=docx_bytes,
                file_name=f"LegalEase_{selected_doc_type.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        # Tabs for Paper Preview and Direct Editing
        st.markdown("<br>", unsafe_allow_html=True)
        tab_view, tab_edit = st.tabs(["📄 Paper Preview", "✏️ Quick Edit Clauses"])

        with tab_view:
            st.markdown(
                f'<div class="legal-document-paper">{st.session_state.generated_doc}</div>',
                unsafe_allow_html=True
            )

        with tab_edit:
            st.info("You can customize any clause or add custom witness details directly before downloading!")
            edited_text = st.text_area(
                "Edit Document Text:",
                value=st.session_state.generated_doc,
                height=450
            )
            if edited_text != st.session_state.generated_doc:
                st.session_state.generated_doc = edited_text
                st.rerun()


# ==============================================================================
# PAGE 3: ABOUT & HELP
# ==============================================================================
else:
    st.markdown("## ℹ️ About LegalEase & Indian Legal Guide")
    st.write("Essential tips and statutory guidelines for formalizing your generated documents.")

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        st.markdown("### 📌 Execution Guidelines")
        st.markdown("""
        1. **Print on Stamp Paper**:
           - **Rental Agreements**: In Tamil Nadu and most states, residential leases are usually executed on ₹20, ₹50, or ₹100 Non-Judicial Stamp Paper, or e-Stamped.
           - **Affidavits**: Typically printed on ₹20 / ₹50 Non-Judicial Stamp paper and sworn before an Advocate / Notary Public.
           - **Promissory Notes**: Executed on plain paper with a **Revenue Stamp** (₹1) affixed, signed across by the borrower.
        
        2. **Signatures & Inking**:
           - All parties must sign at the bottom of **each page**, with full signatures on the execution page.
           - Blue ink is widely preferred for original signatures to distinguish from photocopies.
        
        3. **Witnesses**:
           - Two adult witnesses should sign with their full legal name, father's/spouse's name, and contact address.
        """)

    with col_a2:
        st.markdown("### 🇮🇳 Registration vs Notarization")
        st.markdown("""
        | Document Type | Notarization Required? | Registration Required? |
        | :--- | :--- | :--- |
        | **Rental Agreement (<11 mos)** | Recommended | Optional (Mandatory if >11 months) |
        | **NDA** | Optional | Not Required |
        | **General Affidavit** | **Mandatory (Notary/Oath)** | Not Required |
        | **Employment Letter** | Not Required | Not Required |
        | **Freelance Agreement** | Optional | Not Required |
        | **Promissory Note** | Optional | Not Required (Revenue stamp needed) |
        """)

    st.markdown("---")
    st.markdown("### 🛠️ Developer & Technology Stack")
    st.markdown("""
    - **Frontend**: Streamlit
    - **Backend**: FastAPI + Uvicorn
    - **AI Model**: Google Gemini AI (gemini-2.5-flash)
    - **Document Exporters**: ReportLab (PDF) & Python-docx (Word)
    - **Language Engine**: Full English & தமிழ் (Tamil) Legal Conveyancing
    """)

# Common Footer
st.markdown("""
<div class="legal-footer">
    LegalEase — AI-Powered Legal Document Generator • Built with Streamlit & FastAPI.<br>
    © 2026 LegalEase. All rights reserved.
</div>
""", unsafe_allow_html=True)
