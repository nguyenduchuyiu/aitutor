from rest_framework import serializers
from .models import Lesson, LessonSection, Example, Exercise, Tool

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ["explanation", "image"]

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["question", "answer"]

class LessonSectionSerializer(serializers.ModelSerializer):
    examples = ExampleSerializer(many=True, read_only=True)
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = LessonSection
        fields = ["title", "content", "examples", "exercises"]

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ["name", "description", "embed_url"]

class LessonSerializer(serializers.ModelSerializer):
    sections = LessonSectionSerializer(many=True, read_only=True)
    tools = ToolSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "progress", "sections", "tools"]
