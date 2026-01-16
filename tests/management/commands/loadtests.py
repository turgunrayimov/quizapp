from django.core.management.base import BaseCommand
from tests.models import Subject, Question, Answer
from docx import Document
import os

class Command(BaseCommand):
    help = 'Word fayllardan fanlar va testlarni yuklash'

    def add_arguments(self, parser):
        parser.add_argument('filepaths', nargs='+', type=str, help='Word fayllar manzili')

    def handle(self, *args, **options):
        filepaths = options['filepaths']

        for filepath in filepaths:
            if not os.path.exists(filepath):
                self.stdout.write(self.style.ERROR(f"{filepath} mavjud emas"))
                continue

            # Fayl nomidan fan nomi
            filename = os.path.basename(filepath)
            subject_name = os.path.splitext(filename)[0].capitalize()

            # Fan mavjud bo'lmasa yaratamiz
            subject, created = Subject.objects.get_or_create(name=subject_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Fan yaratildi: {subject_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Fan mavjud: {subject_name}"))

            questions = Question.objects.filter(subject=subject)
            Answer.objects.filter(question__in=questions).delete()
            questions.delete()

            # Word faylni ochamiz
            doc = Document(filepath)
            current_question = None
            tests_count = 0

            for p in doc.paragraphs:
                text = p.text.strip()
                if not text:
                    continue

                # Savol aniqlash:
                # Belgilar: Q:, 1., ? yoki *
                first_char = text[0]
                if first_char in ["?", "*"] or (first_char.isdigit() and len(text) > 1 and text[1] == "."):
                    # Savol yaratish
                    current_question = Question.objects.create(
                        subject=subject,
                        text=text.lstrip("Q:?*1234567890.").strip()
                    )
                    tests_count += 1
                    continue

                # Javoblar
                if current_question is not None:
                    if text.startswith("+"):
                        # To'g'ri javob
                        Answer.objects.create(
                            question=current_question,
                            text=text[1:].strip(),
                            is_correct=True
                        )
                    else:
                        # Noto'g'ri javob
                        cleaned_text = text.lstrip("=-").strip()
                        Answer.objects.create(
                            question=current_question,
                            text=cleaned_text,
                            is_correct=False
                        )
                else:
                    # Javob topildi, lekin savol mavjud emas
                    self.stdout.write(self.style.WARNING(f"Javob topildi, lekin savol yo‘q: {text}"))

            self.stdout.write(self.style.SUCCESS(f"{subject_name}: {tests_count} savol yuklandi!"))
