import random
from lessons.models import Lesson, LessonSection, Example, Exercise, Tool

# Sample data
LESSON_TITLES = ["Introduction to AI", "Machine Learning Basics", "Deep Learning Fundamentals", "NLP Essentials", "Computer Vision"]
SECTION_TITLES = ["Overview", "Key Concepts", "Advanced Topics", "Hands-on Example", "Summary"]
EXAMPLE_EXPLANATIONS = ["Example of implementation", "Case study of real-world usage", "Sample code snippet"]
EXERCISE_QUESTIONS = ["What is the main topic of this section?", "Explain the key concept in simple terms.", "How does this apply to real-world scenarios?"]
EXERCISE_ANSWERS = ["Basic principles", "Advanced topics", "Practical applications"]
TOOL_NAMES = ["TensorFlow Playground", "Google Colab", "Jupyter Notebook", "PyTorch Framework", "OpenCV Library"]

def create_random_lessons(N=5):
    """Generate N random lessons with sections, examples, exercises, and tools."""
    for _ in range(N):
        lesson = Lesson.objects.create(
            title=random.choice(LESSON_TITLES),
            description="This is an auto-generated lesson.",
            progress=round(random.uniform(0, 100), 2)  # Ensure readable float
        )

        # Create sections with unique titles
        selected_sections = random.sample(SECTION_TITLES, random.randint(2, 4))
        for sec_order, sec_title in enumerate(selected_sections, start=1):
            section = LessonSection.objects.create(
                lesson=lesson,
                title=sec_title,
                content="This is auto-generated content for this section.",
                order=sec_order
            )

            # Add examples
            for _ in range(random.randint(1, 3)):
                Example.objects.create(
                    section=section,
                    explanation=random.choice(EXAMPLE_EXPLANATIONS),
                    image=None,
                )

            # Add exercises randomly (50% chance)
            if random.random() < 0.5:
                Exercise.objects.create(
                    section=section,
                    question=random.choice(EXERCISE_QUESTIONS),
                    answer=random.choice(EXERCISE_ANSWERS)
                )

        # Add a tool to the lesson
        Tool.objects.create(
            lesson=lesson,
            name=random.choice(TOOL_NAMES),
            description="This tool is useful for the lesson.",
            embed_url=""
        )

    print(f"✅ Successfully created {N} random lessons with sections, examples, exercises, and tools.")

# Run the function
create_random_lessons(10)  # Change 10 to any number you need
