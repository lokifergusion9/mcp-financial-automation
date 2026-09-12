from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from .extractor import extract_transaction
from .mcp_server import check_message_status, mark_message_as_processed
from .models import FinancialTransaction
from .preprocessing import clean_message


class WorkflowState(TypedDict):
    message_id: str
    message: str
    transaction: FinancialTransaction | None
    already_processed: bool


def check_duplicate(state: WorkflowState) -> WorkflowState:
    """Check whether the message was already processed."""
    return {
        **state,
        "already_processed": check_message_status(state["message_id"]),
    }


def route_message(state: WorkflowState) -> str:
    """Route new messages for processing."""
    if state["already_processed"]:
        return "end"
    return "process"


def process_message(state: WorkflowState) -> WorkflowState:
    """Clean and extract financial information from the message."""
    cleaned_message = clean_message(state["message"])
    transaction = extract_transaction(cleaned_message)

    return {
        **state,
        "message": cleaned_message,
        "transaction": transaction,
    }


def mark_processed(state: WorkflowState) -> WorkflowState:
    """Mark the message as processed."""
    mark_message_as_processed(state["message_id"])
    return state


builder = StateGraph(WorkflowState)

builder.add_node("check_duplicate", check_duplicate)
builder.add_node("process_message", process_message)
builder.add_node("mark_processed", mark_processed)

builder.add_edge(START, "check_duplicate")
builder.add_conditional_edges(
    "check_duplicate",
    route_message,
    {
        "process": "process_message",
        "end": END,
    },
)
builder.add_edge("process_message", "mark_processed")
builder.add_edge("mark_processed", END)

workflow = builder.compile()