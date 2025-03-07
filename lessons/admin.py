from django.contrib import admin
from .models import Lesson, LessonSection, Example, Exercise, Tool

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "progress", "created_at")

@admin.register(LessonSection)
class LessonSectionAdmin(admin.ModelAdmin):
    list_display = ("lesson", "title", "order")

@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ("section", "explanation")

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("section", "question")

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("lesson", "name")
