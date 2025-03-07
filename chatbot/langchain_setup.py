from langchain.llama import LlamaIndex
from .models import ChatMessage

# Initialize LlamaIndex
llama_index = LlamaIndex()

# Index existing chat messages
def index_chat_messages():
    for message in ChatMessage.objects.all():
        llama_index.add_document({
            "user_message": message.user_message,
            "bot_response": message.bot_response,
            "timestamp": message.timestamp.isoformat()
        })

def query_chat_history(conversation_id):
    # Retrieve messages for a specific conversation
    messages = ChatMessage.objects.filter(conversation_id=conversation_id)
    results = []
    for message in messages:
        results.append({
            "user_message": message.user_message,
            "bot_response": message.bot_response,
            "timestamp": message.timestamp.isoformat()
        })
    return results