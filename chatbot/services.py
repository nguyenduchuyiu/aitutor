from google import genai
import os
from .models import ChatMessage, Conversation
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

MAX_NUMBER_OF_LATEST_CONVERSATION = 10

PROMPT_TEMPLATE = '''Đóng vai là giảng viên dạy toán trung học phổ thông Việt Nam, kiên nhẫn.  
                    Hãy trả lời câu hỏi của học sinh.
                    **TÓM TẮT TRƯỚC ĐÓ**: {summary}.
                    Lịch sử trò chuyện gần nhất: {conversation_history}.
                    Lưu ý : 
                    1. Trả lời ngắn gọn, đủ ý. 
                    2. Bạn đang trong cuộc trò chuyện liên tục với học sinh.
                    3. Hãy tóm những thông tin quan trọng trong cả cuộc trò chuyện từ trước đến nay, có thể stack vào nhau tránh làm mất thông tin.
                    Vui lòng trả lời dưới dạng JSON, ví dụ:
                    {{
                        "bot_response": "Hàm số là ...",
                        "summary": "Tóm tắt"
                    }}
                '''

def get_llm_response(user_input, request, lession_id=None):
    # Retrieve or create the conversation context from the session
    if 'conversation' not in request.session:
        request.session['conversation'] = {
            'history': [],
            'summary': ''
        }
    
    conversation = request.session['conversation']
    previous_summary = conversation.get('summary', '')
    
    # Update conversation history
    conversation['history'].append({"user": user_input})  # Store user message
    
    # Prepare the conversation history for the prompt
    conversation_history = ""
    for message in conversation['history'][-MAX_NUMBER_OF_LATEST_CONVERSATION:]:
        if 'user' in message:
            conversation_history += f"Học sinh: {message['user']}\n"
        elif 'bot' in message:
            conversation_history += f"Giảng viên: {message['bot']}\n"
    
    # Modify the prompt to request JSON output
    prompt = PROMPT_TEMPLATE.format(conversation_history=conversation_history, 
                                    user_input=user_input, 
                                    summary=previous_summary)
    
    # Generate response and summary in one request
    response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
    full_response = response.text.replace('```json', '').replace('```', '')

    try:
        # Parse the JSON response
        response_data = json.loads(full_response)
        print("previous summary: ", previous_summary)
        print("summay: ", response_data["summary"])
        print("current his: ", conversation_history)
        bot_response = response_data.get("bot_response", "Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu của bạn.")
        summary = response_data.get("summary", previous_summary)
    except json.JSONDecodeError:
        # Handle JSON parsing error
        bot_response = "Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu của bạn."
        summary = previous_summary  # Use previous summary if available
        
    # Update conversation history 
    conversation['history'].append({"bot": bot_response}) 

    # Update the session with the new summary
    conversation['summary'] = summary
    
    request.session.modified = True 

    # Store the chat message and response in the database
    ChatMessage.objects.create(
        user_message=user_input,
        bot_response=bot_response,
        conversation=None  # No need to store the conversation object in the database
    )

    return bot_response  # Return only the LLM response