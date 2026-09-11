import re


def clean_message(message: str) -> str:
    """Clean a WhatsApp message before further processing."""
    if not message:
        return ""

    message = message.strip()
    message = re.sub(r"\s+", " ", message)

    return message


def is_valid_message(message: str) -> bool:
    """Check whether a message contains useful text."""
    return bool(clean_message(message))