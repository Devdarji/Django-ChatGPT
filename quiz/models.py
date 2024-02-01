from django.db import models
from uuid import uuid4


# Create your models here.
class QuizData(models.Model):
    quiz_uuid = models.UUIDField()
    question_uuid = models.UUIDField(default=uuid4)
    question = models.CharField(max_length=1000)
    option_a = models.CharField(max_length=1000)
    option_b = models.CharField(max_length=1000)
    option_c = models.CharField(max_length=1000)
    option_d = models.CharField(max_length=1000)
    code = models.CharField(max_length=2000, null=True, blank=True)
    answer = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)

    def get_details(self):
        return {
            "quiz_uuid": self.quiz_uuid,
            "question_uuid": self.question_uuid,
            "question": self.question,
            "option_a": self.option_a,
            "option_b": self.option_b,
            "option_c": self.option_c,
            "option_d": self.option_d,
            "code": self.code,
            "answer": self.answer,
            "is_active": self.is_active,
        }
