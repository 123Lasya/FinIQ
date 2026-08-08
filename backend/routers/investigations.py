import json
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.repositories.investigation_repository import InvestigationRepository
from backend.repositories.customer_repository import CustomerRepository
from backend.repositories.transaction_repository import TransactionRepository
from backend.orchestrator.orchestrator_service import orchestrator_service
from backend.utils.response import api_response
from backend.utils.exceptions import ResourceNotFoundException

router = APIRouter(prefix="/investigations", tags=["AI Investigation Tokens & Workflows"])
inv_repo = InvestigationRepository()
cust_repo = CustomerRepository()
txn_repo = TransactionRepository()


@router.get("")
@router.get("/")
def get_incoming_queue(
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves incoming investigation tokens queue."""
    invs = inv_repo.get_queue(db, status=status_filter)
    result = []
    for inv in invs:
        result.append({
            "investigation_id": inv.investigation_id,
            "token_id": inv.token_id,
            "customer_id": inv.customer_id,
            "title": inv.title,
            "description": inv.description,
            "issue_type": inv.issue_type.value if hasattr(inv.issue_type, "value") else str(inv.issue_type),
            "priority": inv.priority.value if hasattr(inv.priority, "value") else str(inv.priority),
            "status": inv.status.value if hasattr(inv.status, "value") else str(inv.status),
            "current_agent": inv.current_agent or "PENDING",
            "final_decision": inv.final_decision,
            "created_at": inv.created_at.isoformat() + "Z" if inv.created_at else None
        })

    return api_response(
        data=result,
        message=f"Retrieved {len(result)} investigation tokens.",
        status_code=status.HTTP_200_OK
    )


@router.post("/start")
def start_investigation(
    payload: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Starts AI Orchestrator multi-agent workflow for an investigation."""
    investigation_id_or_token = payload.get("investigation_id") or payload.get("token_id")
    if not investigation_id_or_token:
        raise HTTPException(status_code=400, detail="Missing investigation_id or token_id in request body.")

    inv = inv_repo.find_by_id_or_token(db, investigation_id_or_token)
    if not inv:
        raise ResourceNotFoundException("Investigation Token", investigation_id_or_token)

    # Launch AI orchestrator in background so frontend polling immediately tracks progress
    res = orchestrator_service.start_investigation(inv.investigation_id, db, run_in_background=True)

    return api_response(
        data=res,
        message="AI Orchestrator workflow triggered successfully.",
        status_code=status.HTTP_200_OK
    )


@router.get("/{id}")
def get_investigation_detail(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves full aggregated investigation details (continuously updated for 1s polling)."""
    inv = inv_repo.find_by_id_or_token(db, id)
    if not inv:
        raise ResourceNotFoundException("Investigation Token", id)

    # 1. Retrieve customer details
    cust = cust_repo.get_by_customer_id(db, inv.customer_id)
    cust_data = {
        "customer_id": cust.customer_id,
        "name": cust.name,
        "email": cust.email,
        "phone": cust.phone,
        "account_number": cust.account_number,
        "risk_level": cust.risk_level.value if hasattr(cust.risk_level, "value") else str(cust.risk_level)
    } if cust else {}

    # 2. Retrieve transactions
    txns = txn_repo.get_by_customer_id(db, inv.customer_id, limit=5)
    txn_data = [
        {
            "transaction_id": t.transaction_id,
            "amount": t.amount,
            "merchant": t.merchant,
            "status": t.status.value if hasattr(t.status, "value") else str(t.status),
            "timestamp": t.timestamp.isoformat() + "Z"
        } for t in txns
    ]

    # 3. Retrieve agent step logs
    logs = inv_repo.get_execution_logs(db, inv.investigation_id)
    timeline = [
        {
            "agent_name": l.agent_name,
            "status": l.status.value if hasattr(l.status, "value") else str(l.status),
            "execution_time": l.execution_time,
            "confidence": l.confidence,
            "started_at": l.started_at.isoformat() + "Z" if l.started_at else None,
            "completed_at": l.completed_at.isoformat() + "Z" if l.completed_at else None
        } for l in logs
    ]

    # 4. Map agent artifacts
    artifacts = inv_repo.get_artifacts(db, inv.investigation_id)
    art_map = {}
    for a in artifacts:
        try:
            art_map[a.agent_name] = json.loads(a.artifact_json)
        except Exception:
            art_map[a.agent_name] = a.artifact_json

    # 5. Extract structured components
    evidence = art_map.get("EnterpriseContextRetrievalAgent", {})
    decision = art_map.get("DecisionIntelligenceAgent", {})
    zero_trust = art_map.get("ZeroTrustDecisionValidationAgent", {})
    simulation = art_map.get("PreFlightShadowSimulationAgent", {})
    privacy = art_map.get("ZeroKnowledgePrivacyEngine", {})
    policy = art_map.get("PolicyGuardrailAgent", {})
    execution = art_map.get("ExecutionAgent", {})
    audit = art_map.get("AuditAgent", {})

    agent_status_map = {
        "IntelligentCaseIntakeAgent": "COMPLETED" if "IntelligentCaseIntakeAgent" in art_map else ("RUNNING" if inv.current_agent == "IntelligentCaseIntakeAgent" else "WAITING"),
        "EnterpriseContextRetrievalAgent": "COMPLETED" if "EnterpriseContextRetrievalAgent" in art_map else ("RUNNING" if inv.current_agent == "EnterpriseContextRetrievalAgent" else "WAITING"),
        "DecisionIntelligenceAgent": "COMPLETED" if "DecisionIntelligenceAgent" in art_map else ("RUNNING" if inv.current_agent == "DecisionIntelligenceAgent" else "WAITING"),
        "ZeroTrustDecisionValidationAgent": "COMPLETED" if "ZeroTrustDecisionValidationAgent" in art_map else ("RUNNING" if inv.current_agent == "ZeroTrustDecisionValidationAgent" else "WAITING"),
        "PreFlightShadowSimulationAgent": "COMPLETED" if "PreFlightShadowSimulationAgent" in art_map else ("RUNNING" if inv.current_agent == "PreFlightShadowSimulationAgent" else "WAITING"),
        "ZeroKnowledgePrivacyEngine": "COMPLETED" if "ZeroKnowledgePrivacyEngine" in art_map else ("RUNNING" if inv.current_agent == "ZeroKnowledgePrivacyEngine" else "WAITING"),
        "PolicyGuardrailAgent": "COMPLETED" if "PolicyGuardrailAgent" in art_map else ("RUNNING" if inv.current_agent == "PolicyGuardrailAgent" else "WAITING"),
        "ExecutionAgent": "COMPLETED" if "ExecutionAgent" in art_map else ("RUNNING" if inv.current_agent == "ExecutionAgent" else "WAITING"),
        "AuditAgent": "COMPLETED" if "AuditAgent" in art_map else ("RUNNING" if inv.current_agent == "AuditAgent" else "WAITING")
    }

    response_payload = {
        "investigation_id": inv.investigation_id,
        "token_id": inv.token_id,
        "title": inv.title,
        "description": inv.description,
        "issue_type": inv.issue_type.value if hasattr(inv.issue_type, "value") else str(inv.issue_type),
        "priority": inv.priority.value if hasattr(inv.priority, "value") else str(inv.priority),
        "status": inv.status.value if hasattr(inv.status, "value") else str(inv.status),
        "current_agent": inv.current_agent or "PENDING",
        "final_decision": inv.final_decision,
        "created_at": inv.created_at.isoformat() + "Z" if inv.created_at else None,
        "completed_at": inv.completed_at.isoformat() + "Z" if inv.completed_at else None,
        "customer": cust_data,
        "transactions": txn_data,
        "timeline": timeline,
        "agent_status": agent_status_map,
        "evidence": evidence,
        "rag": evidence.get("rag_chunks", []),
        "simulation": simulation,
        "policy": policy,
        "decision": decision,
        "zero_trust": zero_trust,
        "privacy": privacy,
        "execution": execution,
        "audit": audit
    }

    return api_response(
        data=response_payload,
        message="Investigation details retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.get("/{id}/timeline")
def get_investigation_timeline(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves live execution timeline logs for polling."""
    inv = inv_repo.find_by_id_or_token(db, id)
    if not inv:
        raise ResourceNotFoundException("Investigation Token", id)

    logs = inv_repo.get_execution_logs(db, inv.investigation_id)
    timeline_data = [
        {
            "agent_name": l.agent_name,
            "status": l.status.value if hasattr(l.status, "value") else str(l.status),
            "execution_time_ms": round(l.execution_time * 1000, 2),
            "confidence": l.confidence,
            "model_used": l.model_used,
            "completed_at": l.completed_at.isoformat() + "Z" if l.completed_at else None
        } for l in logs
    ]

    return api_response(
        data={
            "investigation_id": inv.investigation_id,
            "token_id": inv.token_id,
            "current_agent": inv.current_agent,
            "status": inv.status.value if hasattr(inv.status, "value") else str(inv.status),
            "timeline": timeline_data
        },
        message="Execution timeline retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.post("/{id}/retry")
def retry_investigation(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Restarts multi-agent AI investigation pipeline for a given token."""
    inv = inv_repo.find_by_id_or_token(db, id)
    if not inv:
        raise ResourceNotFoundException("Investigation Token", id)

    res = orchestrator_service.start_investigation(inv.investigation_id, db, run_in_background=True)

    return api_response(
        data=res,
        message=f"Investigation {inv.token_id} workflow restarted successfully.",
        status_code=status.HTTP_200_OK
    )
