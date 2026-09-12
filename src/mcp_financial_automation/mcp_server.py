from fastmcp import FastMCP

from .database import init_db, is_message_processed, mark_message_processed

mcp = FastMCP("Financial Automation")


@mcp.tool
def check_message_status(message_id: str) -> bool:
    """Check whether a message has already been processed."""
    init_db()
    return is_message_processed(message_id)


@mcp.tool
def mark_message_as_processed(message_id: str) -> str:
    """Mark a message as processed to prevent duplicate processing."""
    init_db()
    mark_message_processed(message_id)
    return f"Message {message_id} marked as processed."


if __name__ == "__main__":
    mcp.run()