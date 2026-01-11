from django.shortcuts import render, redirect
from tests.models import Question, Answer

def question_view(request, q_num=1):
    questions = list(Question.objects.all())
    total = len(questions)

    if q_num > total:
        return redirect('result')

    question = questions[q_num - 1]

    # Javob tekshirish
    if request.method == "POST":
        selected = request.POST.get('answer')
        correct = Answer.objects.filter(id=selected, is_correct=True).exists()

        # Sessiyada natija saqlaymiz
        score = request.session.get('score', 0)
        if correct:
            score += 1
        request.session['score'] = score

        # Keyingi savolga o'tish
        return redirect(f'/{q_num + 1}/')

    return render(request, 'tests/question.html', {
        'question': question,
        'q_num': q_num,
        'total': total
    })

def result_view(request):
    score = request.session.get('score', 0)
    total = Question.objects.count()
    request.session['score'] = 0  # qayta boshlaganda nol
    return render(request, 'tests/result.html', {'score': score, 'total': total})