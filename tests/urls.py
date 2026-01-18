from django.contrib import admin
from django.urls import path
from tests.views import subject_list, test_list, quiz, submit_answer, result

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', subject_list, name='subject_list'),
    path('subject/<int:subject_id>/', test_list, name='test_list'),
    path('subject/<int:subject_id>/test/<int:test_no>/', quiz, name='quiz'),
    path('subject/<int:subject_id>/submit/<int:test_no>/', submit_answer, name='submit'),
    path('subject/<int:subject_id>/result/<int:test_no>/', result, name='result'),
]