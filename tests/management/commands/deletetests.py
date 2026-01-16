from django.core.management.base import BaseCommand
from tests.models import Subject, Question, Answer
from django.db import transaction

class Command(BaseCommand):
    help = 'Belgilangan fan bo‘yicha barcha savol va javoblarni o‘chiradi'

    def add_arguments(self, parser):
        parser.add_argument('subject_name', type=str, help='Fan nomi')

    @transaction.atomic
    def handle(self, *args, **options):
        subject_name = options['subject_name'].capitalize()

        try:
            subject = Subject.objects.get(name=subject_name)
        except Subject.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Fan topilmadi: {subject_name}"))
            return

        questions = Question.objects.filter(subject=subject)
        question_count = questions.count()
        answer_count = Answer.objects.filter(question__in=questions).count()

        # Javoblarni o'chirish
        Answer.objects.filter(question__in=questions).delete()
        # Savollarni o'chirish
        questions.delete()

        self.stdout.write(self.style.SUCCESS(
            f"{subject_name}: {question_count} savol va {answer_count} javob o‘chirildi!"
        ))
