from django.shortcuts import render, redirect
from .models import Subject, Question, Answer
import math

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

    # session reset
    request.session['q_index'] = 0
    request.session['score'] = 0

    return render(request, 'tests/test_list.html', {
        'subject': subject,
        'tests': tests,
        'total': questions.count()
    })

def quiz(request, subject_id, test_no):
    q_index = request.session.get('q_index', 0)
    subject = Subject.objects.get(id=subject_id)
    questions = Question.objects.filter(subject=subject)
    start = (test_no - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    group = questions[start:end]

    if q_index >= len(group):
        return redirect('result', subject_id=subject.id, test_no=test_no)

    question = group[q_index]
    answers = Answer.objects.filter(question=question)

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
        answer_id = request.POST.get('answer')
        q_index = request.session.get('q_index', 0)
        subject = Subject.objects.get(id=subject_id)
        questions = Question.objects.filter(subject=subject)
        start = (test_no - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        group = questions[start:end]

        if answer_id:
            ans = Answer.objects.get(id=answer_id)
            if ans.is_correct:
                request.session['score'] = request.session.get('score', 0) + 1

        request.session['q_index'] = q_index + 1

    return redirect('quiz', subject_id=subject_id, test_no=test_no)

def result(request, subject_id, test_no):
    subject = Subject.objects.get(id=subject_id)
    questions = Question.objects.filter(subject=subject)
    start = (test_no - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    group = questions[start:end]

    score = request.session.get('score', 0)
    total = len(group)

    # reset
    request.session['q_index'] = 0
    request.session['score'] = 0

    return render(request, 'tests/result.html', {
        'score': score,
        'total': total,
        'test_no': test_no,
        'subject': subject
    })