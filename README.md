# FinPilot AI

> **Enterprise AI-Powered Financial Operations Assistant**

FinPilot AI is an enterprise-grade AI assistant that helps financial institutions automate customer case investigations using multiple AI agents.

Instead of relying on a single AI model, FinPilot AI uses a **multi-agent architecture** where each AI agent has a dedicated responsibility. Every important decision is verified before execution, making the system more secure, transparent, and compliant.

The project is designed as a hackathon MVP using **FastAPI**, **MySQL**, **Groq LLM**, **RAG**, and a modern enterprise web interface.

---

# Problem Statement

Financial institutions receive thousands of customer requests every day such as:

- Refund Requests
- Failed Transactions
- Chargebacks
- Payment Disputes
- Fraud Complaints

Most existing AI assistants make a decision using a single AI model.

If that AI makes a mistake or is manipulated through prompt injection, the wrong decision may be approved.

FinPilot AI solves this problem by introducing multiple specialized AI agents that validate each other before making a final decision.

---

# Our Solution

FinPilot AI follows an enterprise workflow where every customer investigation passes through multiple AI agents.

Each agent performs one dedicated task.

Instead of trusting one AI, every important decision is verified using a **Zero Trust AI Validation Agent** before moving forward.

This creates a secure, explainable and enterprise-ready AI system.

---

# AI Agent Architecture




<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/ba0dc1e3-614c-4874-b887-bdc284a3a213" />


---

# AI Agents

## Agent 1 – Intelligent Case Intake

Responsible for understanding the customer request.

**Tasks**

- Intent Detection
- Classification
- Priority Detection
- Sentiment Analysis

---

## Agent 2 – Enterprise Context Retrieval

Collects all enterprise information.

Retrieves

- Customer Profile
- Transactions
- CRM History
- Fraud History
- Previous Tickets
- RAG Documents

---

## Agent 3 – Decision Intelligence

Uses the LLM to generate

- Recommendation
- Reasoning
- Confidence Score
- Explanation

---

## Agent 4 – Zero Trust Decision Validation

This is our primary innovation.

Instead of trusting the Decision Agent, another AI validates it.

Checks

- Prompt Injection
- Contradictions
- Missing Evidence
- Duplicate Refund
- Confidence Validation
- Alternative Hypothesis

If validation fails,

the Decision Agent receives structured feedback exactly **one time**.

---

## Agent 5 – Pre-Flight Shadow Simulation

Predicts business impact before execution.

Example

- Fraud Risk
- Financial Impact
- Customer Retention
- Operational Cost
- Net Recommendation

---

## Agent 6 – Zero Knowledge Privacy Engine

Protects customer information before AI reasoning.

Converts sensitive information into secure tokens.

Example

```
John Smith

↓

USER_ALPHA

Account Number

↓

ACC_TOKEN_91

PAN

↓

PAN_HASH_72
```

No AI model sees original customer information.

---

## Agent 7 – Policy Guardrail & Risk Assessment

Verifies

- RBI Guidelines
- Company Policies
- Compliance Rules
- Risk Threshold

Returns

- Auto Execute
- Human Approval
- Block

---

## Agent 8 – Audit & Compliance

Stores

- AI Decisions
- Human Decisions
- Agent Logs
- Compliance Records
- Audit Trail

---

# Key Innovations

## Innovation 1

### Zero Trust AI Decision Validation

Every AI decision is verified by another AI before execution.

No AI is trusted without validation.

---

## Innovation 2

### Pre-Flight Shadow Simulation

Predicts downstream impact before approving financial operations.

Shows

- Fraud Risk
- Financial Impact
- Business Impact
- Customer Retention

---

## Innovation 3

### Zero Knowledge Privacy Engine

Customer sensitive information is tokenized before reaching AI.

Provides

- Privacy
- Security
- Compliance
- Explainability

---

# Retrieval Augmented Generation (RAG)

FinPilot AI supports enterprise document reasoning.

Employees can upload

- Refund Policy
- RBI Guidelines
- Fraud SOP
- Internal Operations Manual
- Compliance Policy

Workflow

```
PDF Upload

↓

Document Parsing

↓

Chunking

↓

Embeddings

↓

Vector Database

↓

Similarity Search

↓

Relevant Context

↓

AI Agents
```

---

# Technology Stack

## Frontend

- HTML
- CSS
- JavaScript

---

## Backend

- FastAPI
- Python

---

## Database

- MySQL

---

## AI

- Groq LLM
- Multiple AI Agents

---

## RAG

- ChromaDB
- Sentence Transformers

---

## Authentication

- JWT Authentication

---

## Charts

- Chart.js

---

#  Features

# Enterprise Application

FinPilot AI provides an employee-oriented enterprise interface.

## Dashboard

Provides visibility into:

- Pending Investigations
- Completed Investigations
- Human Approvals
- Fraud Alerts
- AI Confidence
- Resolution Time
- Agent Performance
- Recent Activity

---

## Incoming Tokens

Employees can view incoming investigation tokens.

Each token contains:

- Token ID
- Customer
- Issue
- Priority
- Status
- Creation Time

Employees can activate individual investigations or activate the complete queue.

---

## AI Investigation

The investigation interface provides a complete view of the AI workflow.

### Displays

- Customer Summary
- Transaction History
- Enterprise Evidence
- Retrieved RAG Documents
- Agent Execution Timeline
- Zero Trust Validation
- Shadow Simulation
- Privacy Transformation
- Policy Guardrail
- Final Recommendation

The agent timeline provides visibility into the execution of each stage.

---

## Human Approval Queue

Cases requiring human intervention appear in the Human Approval Queue.

Employees can review:

- AI Recommendation
- Investigation Evidence
- RAG Sources
- Zero Trust Validation
- Shadow Simulation
- Risk Analysis

The employee can:

- Approve
- Reject

Human decisions are recorded in the audit trail.

---

## Case History

Displays previously completed investigations.

Cases can be opened to inspect:

- Investigation Timeline
- AI Decision
- Human Decision
- Evidence
- Agent Results
- Audit Information

---

## Investigation Reports

Provides consolidated investigation reports containing:

- Customer Information
- Investigation Timeline
- Agent Results
- Evidence
- RAG Sources
- Simulation Results
- Privacy References
- Policy Decision
- Execution Result
- Audit Information

---

## Knowledge Base

Employees can upload enterprise documents and monitor:

- Document Status
- Chunk Count
- Embedding Status
- Indexing Status
- Retrieval Information

---

## Analytics

Provides operational and AI analytics including:

- Investigation Volume
- AI vs Human Decisions
- AI Confidence
- Human Overrides
- Fraud Trends
- Agent Runtime
- Policy Usage
- Simulation Results
- Resolution Time

---

## Settings

Provides configurable system controls including:

- AI Model Configuration
- Model Selection
- Privacy Settings
- RAG Configuration
- Risk Thresholds
- Workflow Configuration

---

# Project Structure

```text
FinIQ/
│
├── backend/
│   │
│   ├── agents/
│   │   ├── agent_1_intake.py
│   │   ├── agent_2_context.py
│   │   ├── agent_3_decision.py
│   │   ├── agent_4_zero_trust.py
│   │   ├── agent_5_shadow.py
│   │   ├── agent_6_privacy.py
│   │   ├── agent_7_guardrail.py
│   │   ├── agent_8_execution.py
│   │   ├── agent_9_audit.py
│   │   ├── agent_context.py
│   │   └── base_agent.py
│   │
│   ├── middleware/
│   ├── orchestrator/
│   ├── rag/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── models/
│   ├── database/
│   ├── demo_data/
│   ├── tests/
│   │
│   ├── app.py
│   ├── config.py
│   └── database.py
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── charts.js
│   ├── styles.css
│   └── README.md
│
├── create_db.py
├── seed_demo.py
├── startup.py
├── health_check.py
├── run.py
├── requirements.txt
└── README.md
```

---

# Project Status

Current Progress

- Project Architecture Completed
- Enterprise UI Completed
- Backend Structure Completed
- Database Design Completed
- Agent Architecture Designed
- RAG Architecture Designed
- FastAPI Backend Development In Progress

---

# Future Enhancements

- Real Banking API Integration
- Email Notifications
- Multi-Tenant Architecture
- Kubernetes Deployment
- Real-Time Monitoring
- Agent Performance Analytics


# API Capabilities

## Authentication

```text
POST /api/auth/login
GET  /api/auth/me
```

## Investigations

```text
GET  /api/investigations
POST /api/investigations/start
GET  /api/investigations/{id}
GET  /api/investigations/{id}/timeline
```

## Dashboard

```text
GET /api/dashboard
```

## Approvals

```text
GET  /api/approvals
GET  /api/approvals/{id}
POST /api/approvals/{id}/approve
POST /api/approvals/{id}/reject
```

## Knowledge Base

```text
POST   /api/knowledge/upload
GET    /api/knowledge/documents
DELETE /api/knowledge/{id}
POST   /api/knowledge/reindex
GET    /api/knowledge/search
```

## Reports

```text
GET /api/reports
GET /api/reports/{id}
```

## Analytics

```text
GET /api/analytics
```

## Settings

```text
GET /api/settings
PUT /api/settings
```

---

# Running the Project

## 1. Clone the Repository

```bash
git clone https://github.com/123Lasya/FinIQ.git
cd FinIQ
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a local `.env` file using `.env.example` as the reference.

Configure:

```text
DATABASE_URL
GROQ_API_KEY
JWT_SECRET
CHROMA_PERSIST_DIRECTORY
CORS_ORIGINS
```

Never commit real credentials or API keys to GitHub.

## 5. Initialize Database

```bash
python create_db.py
```

## 6. Seed Demo Data

```bash
python seed_demo.py
```

## 7. Start the Backend

```bash
uvicorn backend.app:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger API Documentation:

```text
http://localhost:8000/docs
```

---


