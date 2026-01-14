from django.contrib import admin
from django.urls import path
from tests.views import test_list, quiz, submit_answer, result

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', test_list, name='test_list'),
    path('test/<int:test_no>/', quiz, name='quiz'),
    path('submit/<int:test_no>/', submit_answer, name='submit'),
    path('result/<int:test_no>/', result, name='result'),
]