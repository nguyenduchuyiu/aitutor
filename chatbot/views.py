# chatbot.views.py
import json
from django.shortcuts import render
from django.http import JsonResponse
from .services import get_llm_response
from django.contrib.auth.decorators import login_required

@login_required
def chatbot_response(request):
    message = request.POST.get('message')
    lesson_id = request.POST.get('lesson_id')
    
    if not message:
        return JsonResponse({'response': 'No input provided'}, status=400)
    
    try:
        result = get_llm_response(message, request, lesson_id)
        
        # Return the response with action flags
        return JsonResponse({
            'response': result['response'], 
            'update_lesson': result['stage_change'],
            'new_stage': result['new_stage'],
            'update_tab': result['tab_change'],
            'new_tab': result['new_tab'],
            'update_progress': result['progress_update'],
            'progress': result['progress']
        })
    except Exception as e:
        return JsonResponse({
            'response': 'Sorry, I cannot process your message at this time.',
            'error': str(e)
        }, status=500)

def update_tab_context(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lesson_id = data.get('lesson_id')
        tab_id = data.get('tab')

        # Update the session with the new tab context
        request.session['current_lesson'] = lesson_id
        request.session['current_tab'] = tab_id

        # Optionally, you can generate a response from the chatbot here
        # For example, you might want to ask if the user needs help with the new tab
        response_message = f"You have switched to the {tab_id} tab. How can I assist you?"
        
        return JsonResponse({'status': 'success', 'message': response_message, 'lesson_id': lesson_id, 'tab': tab_id})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)