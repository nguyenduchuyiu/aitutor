from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Lesson
from .serializers import LessonSerializer

def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, "lessons/lesson_list.html", {"lessons": lessons})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, "lesson_detail.html")

# API View for chatbot integration
def api_lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    serializer = LessonSerializer(lesson)
    return JsonResponse(serializer.data, safe=False)
