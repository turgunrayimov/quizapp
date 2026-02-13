from django.core.management.base import BaseCommand
from tests.models import Subject, Question, Answer
from docx import Document
from django.db import transaction
import os


class Command(BaseCommand):
    help = "Word fayldan testlarni yuklash (? savol, + to‘g‘ri, = noto‘g‘ri)"

    def add_arguments(self, parser):
        parser.add_argument(
            "filepaths",
            nargs="+",
            type=str,
            help="Word (.docx) fayl manzillari"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        filepaths = options["filepaths"]

        for filepath in filepaths:
            if not os.path.exists(filepath):
                self.stdout.write(self.style.ERROR(f"{filepath} topilmadi ❌"))
                continue

            # Fayl nomidan fan nomi olinadi
            filename = os.path.basename(filepath)
            subject_name = os.path.splitext(filename)[0].capitalize()

            subject, created = Subject.objects.get_or_create(name=subject_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Fan yaratildi: {subject_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Fan mavjud: {subject_name}"))

            # Eski savollarni tozalash
            old_questions = Question.objects.filter(subject=subject)
            Answer.objects.filter(question__in=old_questions).delete()
            old_questions.delete()

            doc = Document(filepath)

            current_question = None
            question_count = 0

            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()

                if not text:
                    continue

                # ----------------------
                # SAVOL
                # ----------------------
                if text.startswith("?"):
                    question_text = text[1:].strip()

                    if not question_text:
                        continue

                    current_question = Question.objects.create(
                        subject=subject,
                        text=question_text
                    )
                    question_count += 1
                    continue

                # Agar savol hali yaratilmagan bo‘lsa
                if current_question is None:
                    self.stdout.write(
                        self.style.WARNING(f"Savolsiz javob topildi: {text}")
                    )
                    continue

                # ----------------------
                # TO‘G‘RI JAVOB
                # ----------------------
                if text.startswith("+"):
                    Answer.objects.create(
                        question=current_question,
                        text=text[1:].strip(),
                        is_correct=True
                    )

                # ----------------------
                # NOTO‘G‘RI JAVOB
                # ----------------------
                elif text.startswith("="):
                    Answer.objects.create(
                        question=current_question,
                        text=text[1:].strip(),
                        is_correct=False
                    )

                else:
                    self.stdout.write(
                        self.style.WARNING(f"Noma’lum format: {text}")
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"{subject_name}: {question_count} ta savol yuklandi ✅"
                )
            )
