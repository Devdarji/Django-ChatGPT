from django.contrib import admin
from .models import QuizData


# Register your models here.
@admin.register(QuizData)
class QuizDataAdmin(admin.ModelAdmin):
    search_fields = ["question", "question_uuid", "quiz_uuid"]
    list_display = ["quiz_uuid", "question_uuid", "question", "answer", "is_active"]
