from django.urls import path
from .views import question_view, result_view

urlpatterns = [
    path('', question_view, name='quiz'),
    path('<int:q_num>/', question_view, name='question'),
    path('result/', result_view, name='result'),
]