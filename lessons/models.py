from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    progress = models.FloatField(default=0.0)  # % progress
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class LessonSection(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=255)
    content = models.TextField()  # Markdown or rich text
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"

class Example(models.Model):
    section = models.ForeignKey(LessonSection, on_delete=models.CASCADE, related_name="examples")
    explanation = models.TextField()
    image = models.ImageField(upload_to="lesson/examples/", blank=True, null=True)

    def __str__(self):
        return f"Example: {self.section.title}"

class Exercise(models.Model):
    section = models.ForeignKey(LessonSection, on_delete=models.CASCADE, related_name="exercises")
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"Exercise: {self.section.title}"

class Tool(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tools")
    name = models.CharField(max_length=255)
    description = models.TextField()
    embed_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
