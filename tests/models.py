from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    text = models.TextField()

    def str(self):
        return self.text[:40]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def str(self):
        return self.text