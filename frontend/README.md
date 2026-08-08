# FinPilot AI — Enterprise Financial Operations Assistant

This is an exact, high-fidelity implementation of the **FinPilot AI** operations platform built with pure HTML, CSS (Vanilla Design System), JavaScript, and Chart.js.

## 🚀 Features & Components Replicated

### 1. Operations Control Dashboard (`/`)
- **Top Metric Cards**: Pending Tokens (34), Completed Today (212), Human Approvals (9), Fraud Alerts (17), Avg AI Confidence (93.4%), Avg Resolution Time (3m 42s), Knowledge Documents (1,284), Audit Log Entries (48,902).
- **Interactive Charts**:
  - Daily Cases (Received vs Resolved bar chart)
  - Fraud Categories Share (Donut chart)
  - AI vs Human Decision Ownership (Stacked bar chart)
  - Refund Trends in ₹ Lakhs (Area chart)
- **Recent Activity Table**: Real-time table of recent dispute cases with quick report action buttons.

### 2. Incoming Investigation Queue (`/tokens`)
- Summary metric cards (In Queue: 8, SLA 30m; Critical: 3; Oldest Token: 18m; Mesh Capacity: 72%).
- 8 queued dispute tokens with Customer IDs, channels, dispute types, amounts, and live `[Activate]` triggers.

### 3. AI Investigation Workspace (`/investigation`)
- **Eight-Agent Investigation Mesh**:
  1. Intelligent Case Intake
  2. Enterprise Context Retrieval (Hybrid RAG)
  3. Decision Intelligence
  4. Zero Trust Decision Validation (Adversarial checks & REVISE revision loop)
  5. Pre-Flight Shadow Simulation
  6. Privacy Protection Engine (Zero-Knowledge PII Tokenization Vault)
  7. Policy Guardrail (§11.4 Ceiling Enforcement)
  8. Execution Orchestration
- Customer Profile Drawer, Payment Details, Risk Signals, Attachment Evidence Viewer, and RAG Knowledge Retrieval Panel.
- Interactive step-by-step agent execution simulation (`[Dispatch Agent Mesh]`).

### 4. Human Approval Queue (`/approvals`)
- Governance metrics (Awaiting Review: 6, Breaching SLA: 3, Approved Today: 41, Override Rate: 7.6%).
- Approval queue table with SLA status and interactive `[Review]` action modal.

### 5. Approval Review Modal (`/approvals/:id`)
- Detailed review for `CASE-77120` (Rhea Kapoor - ₹48,250).
- Manager authorization note input, Zero Trust verification log, Shadow simulation data, and `[Approve Reversal]` / `[Reject Claim]` actions.

### 6. Case History (`/cases`)
- Immutable record of completed investigations with filter tabs (All, Autonomous, Manager Approved, Rejected).

### 7. Investigation Reports (`/reports` & `/reports/:id`)
- Signed, exportable investigation records.
- PDF-style Signed Case Report modal with digital signatures, Zero-Knowledge tokenized PII table, and print handler.

### 8. Knowledge Base RAG (`/knowledge`)
- File ingestion zone, pgvector HNSW engine status, vector count (2,146,908), embedding model specs, and 5 uploaded policy documents.

### 9. Executive Analytics (`/analytics`)
- Board-level operational metrics, Confidence trends, Override rates, Policy citation frequencies, and Shadow Simulation outcome alignment.

### 10. Platform Settings (`/settings`)
- LLM model selectors, RAG parameters, 8 Agent Toggles (with mandatory locks for Zero Trust, Privacy Engine, and Policy Guardrail), and privacy mode settings.

---

## 🛠️ How to Run

Simply open [index.html](file:///c:/Users/Dell/OneDrive/Desktop/FinIQ/index.html) in any modern web browser or serve via any static web server:

```bash
# Using Python
python -m http.server 8000

# Or using npx
npx serve .
```
