from django.db import models

class Question(models.Model):
    text = models.TextField()

    def str(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def str(self):
        return self.text