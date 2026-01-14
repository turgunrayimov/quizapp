from django.core.management.base import BaseCommand
from docx import Document
from tests.models import Question, Answer

class Command(BaseCommand):
    help = "Load tests from Word file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        doc = Document(file_path)

        Question.objects.all().delete()

        current = None
        tests = []

        for para in doc.paragraphs:
            text = para.text.strip()
            if text.startswith("*"):
                if current:
                    tests.append(current)
                current = {"question": text[1:].strip(), "answers": []}
            elif text.startswith("+"):
                current["answers"].append((text[1:].strip(), True))
            elif text.startswith("="):
                current["answers"].append((text[1:].strip(), False))

        if current:
            tests.append(current)

        for test in tests:
            q = Question.objects.create(text=test["question"])
            for a_text, is_correct in test["answers"]:
                Answer.objects.create(question=q, text=a_text, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS(f"{len(tests)} tests loaded!"))