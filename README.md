# ⚖️ LegalEase — AI-Powered Legal Information Assistant

LegalEase is a modern, modular AI assistant that translates complex legal terminology, doctrines, procedures, and concepts into clear, plain language. Built on a decoupled architecture with a **FastAPI** REST backend, **Google Gemini 2.5 Flash** for natural language understanding, and an intuitive **Streamlit** user interface.

> **Disclaimer**: LegalEase is designed strictly for informational and educational purposes. It does not provide formal legal advice, representation, or substitute for a licensed attorney.

---

## 🌟 Key Features

- **Plain-Language Explanations**: Deconstructs complicated statutes, contract terms, torts, and legal doctrines into accessible, structured breakdowns.
- **Strict Ethical Boundaries**: Configured with system instructions preventing legal hallucinations, false court citations, or offering unlawful assistance.
- **Context & Jurisdiction Awareness**: Allows users to provide jurisdiction-specific details to receive tailored educational context.
- **Decoupled Architecture**: Robust REST API powered by FastAPI with full Swagger (`/docs`) and ReDoc (`/redoc`) API documentation.
- **Secure Key Management**: Google Gemini API key is isolated strictly within the backend `.env` file and never exposed to the frontend or browser.
- **Resilient Error Handling**: Gracefully handles missing API keys, rate limits, network timeouts, invalid inputs, and connection drops.
- **Interactive Web Interface**: Streamlit UI with connection status testing, sample questions, and clean markdown presentation.

---

## 🛠️ Technologies Used

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core programming language |
| **Backend Framework** | FastAPI | High-performance asynchronous REST API |
| **ASGI Server** | Uvicorn | Production-ready ASGI web server |
| **AI / LLM** | Google Gemini API (`google-genai`) | State-of-the-art LLM for legal text analysis |
| **Validation** | Pydantic v2 | Strict request and response data schema validation |
| **Frontend UI** | Streamlit | Clean, reactive user interface |
| **HTTP Client** | Requests | Robust HTTP calls between frontend and backend |
| **Configuration** | python-dotenv | Secure environment variable handling |

---

## 📁 Project Structure

```text
LegalEase/
│
├── backend/
│   ├── __init__.py           # Backend package initialization
│   ├── main.py               # FastAPI application, routes, and CORS setup
│   ├── models.py             # Pydantic request and response schemas
│   └── gemini_service.py     # Google Gemini SDK integration and system prompts
│
├── frontend/
│   └── app.py                # Streamlit user interface and backend communication
│
├── .env                      # Local environment configuration (contains API key)
├── .env.example              # Template environment configuration
├── .gitignore                # Git ignore rules for venv, env files, and caches
├── requirements.txt          # Python dependencies
└── README.md                 # Complete project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher installed on your system
- An active Google Gemini API key ([Get one free from Google AI Studio](https://aistudio.google.com/app/apikey))

### 1. Clone or Open the Project
Ensure you are in the project root directory:
```bash
cd LegalEase
```

### 2. Create a Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

Open `.env` and insert your Gemini API key:
```ini
GEMINI_API_KEY=AIzaSy...your_actual_api_key_here
```

---

## 🖥️ Running the Application

LegalEase runs as two communicating services: the **FastAPI Backend** and the **Streamlit Frontend**.

### Step 1: Start the Backend Server

In your first terminal (with the virtual environment activated):
```bash
uvicorn backend.main:app --reload --port 8000
```
- **Backend API**: `http://127.0.0.1:8000`
- **Interactive API Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Alternative Docs (ReDoc)**: `http://127.0.0.1:8000/redoc`
- **Health Check**: `http://127.0.0.1:8000/health`

### Step 2: Start the Frontend Interface

In a second terminal (activate the virtual environment first):
```bash
# Windows
venv\Scripts\activate

# Start Streamlit
streamlit run frontend/app.py
```
Streamlit will automatically open `http://localhost:8501` in your browser.

---

## 📡 API Endpoints

### 1. Root Endpoint
- **URL**: `GET /`
- **Description**: Returns welcome message and endpoints guide.
- **Response**:
```json
{
  "message": "Welcome to the LegalEase API",
  "service": "LegalEase",
  "status": "active",
  "docs": "/docs",
  "health": "/health"
}
```

### 2. Health Check
- **URL**: `GET /health`
- **Description**: Verifies service status.
- **Response**:
```json
{
  "status": "healthy",
  "service": "LegalEase Backend",
  "version": "1.0.0"
}
```

### 3. Ask Legal Question
- **URL**: `POST /ask`
- **Request Body**:
```json
{
  "question": "What are the essential elements required to form a legally enforceable contract?",
  "context": "Jurisdiction: New York, USA"
}
```
- **Response**:
```json
{
  "answer": "### Essential Elements of a Contract\n\nUnder New York and general common law, an enforceable contract requires...",
  "disclaimer": "IMPORTANT DISCLAIMER: LegalEase provides general legal information for educational and informational purposes only. It is NOT legal advice..."
}
```

---

## 🧪 Testing & Verification

Run these verification steps to test the system:

1. **Verify Backend Root**:
   ```bash
   curl http://127.0.0.1:8000/
   ```
2. **Verify Health Check**:
   ```bash
   curl http://127.0.0.1:8000/health
   ```
3. **Verify Input Validation (Empty Question)**:
   ```bash
   curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"\"}"
   ```
   *Expected: HTTP 400 Bad Request*
4. **Verify Frontend**: Open `http://localhost:8501`, click "Test Connection" in the sidebar to verify FastAPI connectivity.

---

## ❓ Troubleshooting

| Issue | Likely Cause | Solution |
| :--- | :--- | :--- |
| `Cannot connect to LegalEase backend` | FastAPI server is not running | Start backend with `uvicorn backend.main:app --reload`. Ensure port 8000 is open. |
| `Gemini API key is not configured` | Empty or placeholder in `.env` | Add a valid Gemini API key to `.env` (`GEMINI_API_KEY=AIzaSy...`) and restart backend. |
| `Gemini AI Service Error (502)` | Invalid API key or quota issue | Verify API key in [Google AI Studio](https://aistudio.google.com/app/apikey). |
| `ModuleNotFoundError: No module named 'backend'` | Running uvicorn from inside `backend/` folder | Run uvicorn from the **project root**: `uvicorn backend.main:app --reload`. |
| Port 8000 already in use | Another application is bound to 8000 | Specify a different port: `uvicorn backend.main:app --reload --port 8080`, and update the backend URL in Streamlit sidebar. |

---

## ⚖️ Legal Disclaimer

LegalEase is an artificial intelligence-assisted educational tool. The information provided by LegalEase is for general informational and educational purposes only and does not constitute formal legal advice, representation, or an attorney-client relationship. You should not act or refrain from acting on the basis of any information provided without seeking competent, licensed legal counsel in your relevant jurisdiction.
