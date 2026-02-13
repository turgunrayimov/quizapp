from django.shortcuts import render, redirect
from .models import Subject, Question, Answer
import math
import random

PAGE_SIZE = 30

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'tests/subject_list.html', {
        'subjects': subjects
    })

def test_list(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    questions = Question.objects.filter(subject=subject)
    test_count = math.ceil(questions.count() / PAGE_SIZE)
    tests = range(1, test_count + 1)

    return render(request, 'tests/test_list.html', {
        'subject': subject,
        'tests': tests,
        'total': questions.count()
    })

def quiz(request, subject_id, test_no):
    # session kalitlari test_no bo'yicha
    q_index_key = f'q_index_{subject_id}_{test_no}'
    score_key = f'score_{subject_id}_{test_no}'

    q_index = request.session.get(q_index_key, 0)

    subject = Subject.objects.get(id=subject_id)
    questions = Question.objects.filter(subject=subject).order_by('id')
    start = (test_no - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    group = list(questions[start:end])

    if q_index >= len(group):
        return redirect('result', subject_id=subject.id, test_no=test_no)

    question = group[q_index]
    answers = list(Answer.objects.filter(question=question))
    random.shuffle(answers)

    return render(request, 'tests/question.html', {
        'question': question,
        'answers': answers,
        'index': q_index + 1,
        'total': len(group),
        'test_no': test_no,
        'subject': subject
    })

def submit_answer(request, subject_id, test_no):
    if request.method == 'POST':
        q_index_key = f'q_index_{subject_id}_{test_no}'
        score_key = f'score_{subject_id}_{test_no}'

        q_index = request.session.get(q_index_key, 0)
        answer_id = request.POST.get('answer_id')  # JS orqali yuboriladi

        subject = Subject.objects.get(id=subject_id)
        questions = Question.objects.filter(subject=subject)
        start = (test_no - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        group = list(questions[start:end])

        if answer_id:
            ans = Answer.objects.get(id=answer_id)
            if ans.is_correct:
                request.session[score_key] = request.session.get(score_key, 0) + 1

        request.session[q_index_key] = q_index + 1

    return redirect('quiz', subject_id=subject_id, test_no=test_no)

def result(request, subject_id, test_no):
    score_key = f'score_{subject_id}_{test_no}'

    subject = Subject.objects.get(id=subject_id)
    questions = Question.objects.filter(subject=subject)
    start = (test_no - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    group = list(questions[start:end])

    score = request.session.get(score_key, 0)
    total = len(group)

    # reset faqat test tugaganda
    request.session[f'q_index_{subject_id}_{test_no}'] = 0
    request.session[score_key] = 0

    return render(request, 'tests/result.html', {
        'score': score,
        'total': total,
        'test_no': test_no,
        'subject': subject
    })