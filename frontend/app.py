"""Streamlit frontend for LegalEase - AI-powered legal information assistant."""

import os
import requests
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="LegalEase — AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for polished, modern look
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.1rem;
    }
    .main-subtitle {
        font-size: 1.15rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .disclaimer-card {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 1rem 1.25rem;
        border-radius: 6px;
        margin-top: 1.5rem;
        color: #92400E;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .response-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .sidebar-section {
        margin-bottom: 1.5rem;
    }
    .badge-status {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-online {
        background-color: #DCFCE7;
        color: #166534;
    }
    .badge-offline {
        background-color: #FEE2E2;
        color: #991B1B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("## ⚖️ About LegalEase")
    st.markdown(
        """
        **LegalEase** is an AI-powered legal information assistant designed to translate
        complex legal terminology, doctrines, and procedures into plain, understandable English.
        """
    )
    st.divider()

    st.markdown("### ⚙️ Backend Settings")
    backend_url = st.text_input(
        "FastAPI Backend URL",
        value=os.getenv("BACKEND_URL", "http://127.0.0.1:8000"),
        help="Specify the URL where the LegalEase FastAPI backend server is running.",
    ).rstrip("/")

    # Connection Status Check
    col1, col2 = st.columns([1, 1])
    with col1:
        check_conn = st.button("🔌 Test Connection", use_container_width=True)

    backend_healthy = False
    if check_conn:
        try:
            resp = requests.get(f"{backend_url}/health", timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                st.success(f"Connected: {data.get('service', 'Backend')} (v{data.get('version', '1.0')})")
                backend_healthy = True
            else:
                st.error(f"Backend responded with status code: {resp.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect: Backend is not reachable.")
        except requests.exceptions.Timeout:
            st.error("Connection timed out.")
        except Exception as e:
            st.error(f"Error checking connection: {str(e)}")

    st.divider()
    st.markdown("### ⚠️ Important Notice")
    st.info(
        "LegalEase provides general educational information only. It is **not** a law firm, "
        "does not provide formal legal advice, and does not create an attorney-client relationship. "
        "Always consult a licensed attorney in your jurisdiction for specific legal counsel."
    )

    st.divider()
    st.caption("LegalEase v1.0 • Built with FastAPI, Streamlit & Google Gemini")

# ----------------- MAIN CONTENT -----------------
st.markdown('<div class="main-header">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">AI-powered legal information assistant</div>', unsafe_allow_html=True)

# Sample questions for quick testing
with st.expander("💡 Click here for sample questions to try"):
    sample_cols = st.columns(3)
    sample_questions = [
        ("Contract Breach", "What are the primary elements needed to establish a breach of contract claim?"),
        ("Non-Disclosure Agreement", "What key clauses should typically be included in a standard Non-Disclosure Agreement (NDA)?"),
        ("Fair Use & Copyright", "How does the 'fair use' doctrine work in copyright law and what factors are evaluated?"),
    ]
    for i, (label, sample_q) in enumerate(sample_questions):
        if sample_cols[i].button(label, key=f"sample_{i}", use_container_width=True):
            st.session_state["query_input"] = sample_q

# Inputs
question_input = st.text_area(
    "Legal Question *",
    value=st.session_state.get("query_input", ""),
    height=120,
    placeholder="e.g., What is the difference between a misdemeanor and a felony? What steps should a tenant take if a landlord refuses essential repairs?",
    help="Type your legal question or topic you want explained.",
)

context_input = st.text_area(
    "Optional Additional Context",
    height=80,
    placeholder="e.g., Jurisdiction: State of California, United States. Commercial lease dispute.",
    help="Optional: Provide relevant jurisdiction, parties involved, or background facts to make the information more pertinent.",
)

submit_button = st.button("⚖️ Get Legal Information", type="primary", use_container_width=True)

# ----------------- ACTION & HANDLING -----------------
if submit_button:
    # 1. Validation for empty question
    if not question_input or not question_input.strip():
        st.warning("⚠️ Please enter a legal question before submitting.")
    else:
        # 2. Loading indicator
        with st.spinner("Analyzing your legal query with Gemini AI..."):
            payload = {
                "question": question_input.strip(),
                "context": context_input.strip() if context_input else None,
            }
            
            try:
                # Call FastAPI backend POST /ask
                response = requests.post(
                    f"{backend_url}/ask",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=45.0,
                )

                # Check HTTP response code
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received.")
                    disclaimer = data.get("disclaimer", "")

                    # 3. Response section
                    st.markdown("### 📋 Legal Information")
                    st.markdown(
                        f"""
                        <div class="response-card">
                            {answer}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # 4. Disclaimer section
                    if disclaimer:
                        st.markdown(
                            f"""
                            <div class="disclaimer-card">
                                <strong>Legal Notice:</strong><br>{disclaimer}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                elif response.status_code == 400:
                    error_detail = response.json().get("detail", "Bad Request")
                    st.error(f"⚠️ Validation Error (400): {error_detail}")

                elif response.status_code == 502:
                    error_detail = response.json().get("detail", "Gemini API Gateway error")
                    st.error(
                        f"🤖 Gemini AI Service Error (502):\n\n"
                        f"{error_detail}\n\n"
                        f"Please ensure a valid `GEMINI_API_KEY` is set in the backend `.env` file."
                    )

                elif response.status_code == 500:
                    error_detail = response.json().get("detail", "Internal server error")
                    st.error(
                        f"⚙️ Backend Server Error (500):\n\n"
                        f"{error_detail}\n\n"
                        f"Check the backend console logs or `.env` configuration."
                    )

                else:
                    st.error(f"❌ Server returned unexpected status code {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    f"🔌 **Connection Error**: Unable to reach the LegalEase backend at `{backend_url}`.\n\n"
                    f"Please ensure the FastAPI server is running. You can start it with:\n"
                    f"```bash\n"
                    f"uvicorn backend.main:app --reload\n"
                    f"```"
                )

            except requests.exceptions.Timeout:
                st.error(
                    "⏱️ **Request Timeout**: The request to the backend took too long to complete. "
                    "This may be due to network latency or AI service response delay. Please try again."
                )

            except requests.exceptions.RequestException as req_err:
                st.error(f"🌐 **HTTP Error**: {str(req_err)}")

            except Exception as e:
                st.error(f"💥 **Unexpected Error**: {str(e)}")
