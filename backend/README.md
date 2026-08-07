# FinPilot AI - Enterprise Financial Operations Assistant

FinPilot AI is a production-grade, enterprise-ready multi-agent backend built for automated financial complaint intake, autonomous multi-agent risk & compliance investigation, pre-flight shadow simulation, policy guardrail enforcement, human-in-the-loop sign-off, and immutable audit telemetry.

---

## Technical Stack

- **Framework**: FastAPI (Python 3.12, Async)
- **Database & ORM**: SQLAlchemy 2.0 (MySQL / SQLite), PyMySQL, aiomysql
- **Data Validation**: Pydantic v2 & Pydantic-Settings
- **Authentication**: JWT (JSON Web Tokens) with Employee Role RBAC
- **AI Engine**: Groq LLM API (`llama-3.3-70b-versatile`)
- **RAG Architecture**: ChromaDB Vector Store, SentenceTransformers (`all-MiniLM-L6-v2`), LangChain
- **Document Parsing**: `pypdf`, `python-docx`, plain text loaders

---

## 9 Autonomous AI Agents Architecture

1. **Intelligent Case Intake Agent**: Parses raw complaint text, extracts entities (amounts, currencies, transaction IDs), and classifies severity.
2. **Zero Knowledge Privacy Engine**: Redacts sensitive PII (PAN, SSN, CVV, Card Numbers, emails, phone numbers) before downstream processing.
3. **Enterprise Context Retrieval Agent**: Fetches historical ledger transactions and queries ChromaDB for relevant SOPs/policies.
4. **Decision Intelligence Agent**: Evaluates intake, RAG context, and transaction history using Groq LLM to formulate decision recommendations.
5. **Zero Trust Decision Validation Agent**: Independently verifies dispute claims against database transactions without assuming trust.
6. **Pre-Flight Shadow Simulation Agent**: Simulates financial ledger impact, reserve balance changes, and ledger integrity before execution.
7. **Policy Guardrail Agent**: Enforces hard compliance limits (e.g. claims > ₹25,000 INR mandate Human Officer approval).
8. **Execution Agent**: Commits financial disbursement or holds the token in the queue for human approval.
9. **Audit Agent**: Synthesizes a cryptographic SHA-256 master hash audit report detailing the 9-agent workflow trajectory.

---

## Project Structure

```
backend/
├── app.py                      # Main FastAPI initialization & router setup
├── config.py                   # Environment settings & configuration
├── database.py                 # SQLAlchemy base, engine & session management
├── logging.py                  # Enterprise structured logger setup
├── requirements.txt            # Python production dependencies
├── .env.example                # Sample environment variables
├── README.md                   # Technical documentation
├── models/                     # SQLAlchemy ORM Models
│   ├── __init__.py
│   ├── user.py                 # Employee user account model
│   ├── investigation.py        # Investigation token case model
│   ├── transaction.py         # Financial transaction ledger model
│   ├── audit.py               # Immutable audit log model
│   └── policy.py              # Compliance rule model
├── schemas/                    # Pydantic Schemas
│   ├── __init__.py
│   ├── auth.py
│   ├── investigation.py
│   ├── agent.py
│   ├── rag.py
│   └── policy.py
├── agents/                     # 9 Independent AI Agent implementations
│   ├── __init__.py
│   ├── base.py                 # Abstract BaseAgent & Groq interaction layer
│   ├── intake_agent.py
│   ├── context_retrieval_agent.py
│   ├── decision_intelligence_agent.py
│   ├── zero_trust_validation_agent.py
│   ├── shadow_simulation_agent.py
│   ├── privacy_engine_agent.py
│   ├── policy_guardrail_agent.py
│   ├── execution_agent.py
│   └── audit_agent.py
├── orchestrator/               # Pipeline Orchestration
│   ├── __init__.py
│   └── workflow_orchestrator.py
├── routers/                    # FastAPI API Endpoints
│   ├── __init__.py
│   ├── auth.py                 # POST /auth/login, GET /auth/me
│   ├── investigations.py       # Investigation queue & activation endpoints
│   ├── rag.py                  # POST /rag/upload, POST /rag/search
│   ├── audit.py                # GET /audit/logs, GET /audit/investigation/{token_id}
│   ├── analytics.py            # GET /analytics/dashboard
│   └── policy.py               # GET/POST /policies
├── services/                   # Business logic services
│   ├── __init__.py
│   ├── auth_service.py
│   ├── investigation_service.py
│   ├── rag_service.py
│   └── policy_service.py
├── utils/                      # Authentication & helper utilities
│   ├── __init__.py
│   ├── jwt.py
│   └── deps.py
├── rag/                        # Vector Store & Embedding services
│   ├── __init__.py
│   ├── vector_store.py
│   ├── embeddings.py
│   ├── document_loader.py
│   └── retriever.py
├── prompts/                    # System Prompts for AI Agents
│   ├── __init__.py
│   └── agent_prompts.py
├── demo_data/                  # Seed data & sample documents
│   ├── __init__.py
│   ├── seed_data.py
│   └── sample_policy.txt
└── logs/                       # Application logs directory
    └── .gitkeep
```

---

## Quickstart & Installation

### 1. Requirements & Virtual Environment Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and set your Groq API Key:
```env
GROQ_API_KEY="gsk_your_groq_api_key"
```

### 3. Run the Backend Server
```bash
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```
Upon startup, `app.py` automatically initializes the database tables and populates seed data!

Open browser docs at: **http://localhost:8000/docs**

---

## Default Employee Credentials

| Parameter | Value |
|---|---|
| **Employee ID** | `EMP-1001` |
| **Email** | `employee@finpilot.ai` |
| **Password** | `Password123!` |
| **Role** | `OPERATIONS_EXEC` |

---

## Core API Endpoints

- **`POST /api/v1/auth/login`**: Employee Login -> Returns JWT Token.
- **`GET /api/v1/investigations/queue`**: View incoming complaints queue.
- **`POST /api/v1/investigations/`**: Submit a new complaint token.
- **`POST /api/v1/investigations/{token_id}/activate`**: Triggers full 9-agent investigation pipeline.
- **`POST /api/v1/investigations/{token_id}/approval`**: Human Operations Executive APPROVE/REJECT action.
- **`GET /api/v1/audit/investigation/{token_id}`**: Retrieve cryptographic multi-agent audit trail.
- **`GET /api/v1/analytics/dashboard`**: Operations summary statistics.
