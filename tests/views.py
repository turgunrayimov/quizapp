from django.shortcuts import render, redirect
from tests.models import Question, Answer
import random

def home(request):
    """Bosh sahifa — tugmalar tanlash"""
    return render(request, 'tests/home.html')


def start_quiz(request, mode):
    """
    mode: 'all' yoki '30'
    Sessiyaga savollar ro'yxatini saqlaymiz
    """
    all_questions = list(Question.objects.all())

    if mode == 'all':
        questions = all_questions
    elif mode == '30':
        questions = random.sample(all_questions, min(30, len(all_questions)))
    else:
        return redirect('home')

    # Sessiyada saqlaymiz
    request.session['questions'] = [q.id for q in questions]
    request.session['score'] = 0
    request.session['current'] = 0  # hozirgi savol index

    return redirect('question')


def question_view(request):
    """1 test = 1 sahifa"""
    questions_ids = request.session.get('questions', [])
    current_index = request.session.get('current', 0)

    if current_index >= len(questions_ids):
        return redirect('result')

    question = Question.objects.get(id=questions_ids[current_index])

    if request.method == "POST":
        selected = request.POST.get('answer')
        if selected and Answer.objects.filter(id=selected, is_correct=True).exists():
            request.session['score'] += 1

        # Keyingi savol
        request.session['current'] = current_index + 1
        return redirect('question')

    return render(request, 'tests/question.html', {
        'question': question,
        'q_num': current_index + 1,
        'total': len(questions_ids)
    })


def result_view(request):
    score = request.session.get('score', 0)
    total = len(request.session.get('questions', []))

    # Bahoni hisoblash
    percentage = (score / total) * 100 if total > 0 else 0
    if percentage >= 90:
        grade = 5
    elif percentage >= 75:
        grade = 4
    elif percentage >= 50:
        grade = 3
    else:
        grade = 2

    # Sessiyani tozalash
    request.session['questions'] = []
    request.session['score'] = 0
    request.session['current'] = 0

    return render(request, 'tests/result.html', {
        'score': score,
        'total': total,
        'grade': grade
    })