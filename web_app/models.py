from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CodeQuestionAnswer(models.Model):
    user = models.ForeignKey(
        User, related_name="code_question_answer", on_delete=models.DO_NOTHING
    )
    question = models.TextField(max_length=5000)
    answer = models.TextField(max_length=5000)
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.question
