import logging
from typing import Any, Dict, List


def format_message(author, content, search_results=None):
    message = f"**{author}:**\n{content}\n"

    if search_results:
        message += "\n**Resultados da pesquisa:**\n"
        for result in search_results:
            message += f"- {result['title']}: {result['link']}\n"

    return message


MAX_MESSAGES = 10
MAX_TEXT_LENGTH = 1000

def valid_messages(messages: List[Dict[str, Any]]) -> bool:
    if not isinstance(messages, list) or len(messages) > MAX_MESSAGES:
        return False
        
    for message in messages:
        if not isinstance(message, dict) or 'role' not in message or 'parts' not in message:
            return False
        if not isinstance(message['parts'], list) or not all(isinstance(part, dict) and 'text' in part for part in message['parts']):
            return False
        if any(len(part['text']) > MAX_TEXT_LENGTH for part in message['parts']):
            return False
    return True

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")  # Logger específico do Uvicorn