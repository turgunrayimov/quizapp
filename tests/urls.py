from django.urls import path
from .views import home, start_quiz, question_view, result_view

urlpatterns = [
    path('', home, name='home'),
    path('start/<str:mode>/', start_quiz, name='start_quiz'),
    path('question/', question_view, name='question'),
    path('result/', result_view, name='result'),
]