import random
from lessons.models import Lesson, LessonSection, Example, Exercise

# Define sample data
LESSON_TITLES = ["Introduction to AI", "Machine Learning Basics", "Deep Learning Fundamentals", "NLP Essentials", "Computer Vision"]
SECTION_TITLES = ["Overview", "Key Concepts", "Advanced Topics", "Hands-on Example", "Summary"]
EXAMPLE_EXPLANATIONS = ["Example of implementation", "Case study of real-world usage", "Sample code snippet"]
EXERCISE_QUESTIONS = ["What is the main topic of this section?", "Explain the key concept in simple terms.", "How does this apply to real-world scenarios?"]
EXERCISE_ANSWERS = ["Basic principles", "Advanced topics", "Practical applications"]

def create_random_lessons(N=5):
    """Generate N random lessons with sections, examples, and exercises."""
    for _ in range(N):
        lesson = Lesson.objects.create(
            title=random.choice(LESSON_TITLES),
            description="Auto-generated lesson for testing.",
            progress=random.uniform(0, 100)
        )

        num_sections = random.randint(2, 4)
        for sec_order in range(1, num_sections + 1):
            section = LessonSection.objects.create(
                lesson=lesson,
                title=random.choice(SECTION_TITLES),
                content="Auto-generated content.",
                order=sec_order
            )

            # Add examples
            num_examples = random.randint(1, 3)
            for ex_order in range(1, num_examples + 1):
                Example.objects.create(
                    section=section,
                    explanation=random.choice(EXAMPLE_EXPLANATIONS),
                    image=None,
                )

            # Add exercises randomly
            if random.choice([True, False]):  # 50% chance of having an exercise
                Exercise.objects.create(
                    section=section,
                    question=random.choice(EXERCISE_QUESTIONS),
                    answer=random.choice(EXERCISE_ANSWERS)
                )

    print(f"✅ Successfully created {N} random lessons.")

# Run the function
create_random_lessons(10)  # Change 10 to any number you need

                                