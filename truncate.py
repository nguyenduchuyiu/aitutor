import django
import os

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aitutor.settings")  # Replace with your project name
django.setup()

from lessons.models import Lesson, LessonSection, Example, Exercise, Tool

def truncate_tables():
    """Deletes all data from the tables in the 'lessons' app."""
    models = [Example, Exercise, LessonSection, Tool, Lesson]
    
    for model in models:
        model.objects.all().delete()  # Deletes all records in each table
        print(f"✅ Emptied table: {model.__name__}")

if __name__ == "__main__":
    truncate_tables()
    print("✅ All tables in 'lessons' app are now empty.")
