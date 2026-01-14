from django.shortcuts import render, redirect
from .models import Question, Answer
import math

PAGE_SIZE = 30  # Bir testdagi savollar soni

def test_list(request):
    total_questions = Question.objects.count()
    test_count = math.ceil(total_questions / PAGE_SIZE)
    tests = range(1, test_count + 1)

    # har ehtimolga qarshi
    request.session['q_index'] = 0
    request.session['score'] = 0

    return render(request, 'tests/test_list.html', {
        'tests': tests,
        'total': total_questions
    })


def quiz(request, test_no):
    q_index = request.session.get('q_index', 0)
    questions = Question.objects.all()

    start = (test_no - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    group = questions[start:end]

    # agar test savollari tugasa
    if q_index >= len(group):
        return redirect('result', test_no=test_no)

    question = group[q_index]
    answers = Answer.objects.filter(question=question)

    return render(request, 'tests/question.html', {
        'question': question,
        'answers': answers,
        'index': q_index + 1,
        'total': len(group),
        'test_no': test_no
    })


def submit_answer(request, test_no):
    if request.method == 'POST':
        answer_id = request.POST.get('answer')
        q_index = request.session.get('q_index', 0)

        questions = Question.objects.all()
        start = (test_no - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        group = questions[start:end]

        # ball hisob
        if answer_id:
            ans = Answer.objects.get(id=answer_id)
            if ans.is_correct:
                request.session['score'] = request.session.get('score', 0) + 1

        request.session['q_index'] = q_index + 1

    return redirect('quiz', test_no=test_no)


def result(request, test_no):
    questions = Question.objects.all()
    start = (test_no - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    group = questions[start:end]

    score = request.session.get('score', 0)
    total = len(group)

    # Reset
    request.session['q_index'] = 0
    request.session['score'] = 0

    return render(request, 'tests/result.html', {
        'score': score,
        'total': total,
        'test_no': test_no
    })