from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="quiz"),
    path("download-image/", views.download_image, name="download-image"),
    path("test-api/", views.test_api, name="test-api"),
    path("image-api/<uuid:question_uuid>/", views.image_api, name="image-api"),
    path("question-answers/", views.question_answers, name="question-answers"),
    path("new-api", views.new_text_api, name="new-test-api"),
]
