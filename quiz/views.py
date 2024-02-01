import requests
import openai
import uuid
import ast

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings as dj_settings

from quiz import constants as quiz_constants
from quiz import models as quiz_models
from quiz import utils as quiz_utils

from weasyprint import HTML
from pathlib import Path


# Create your views here.
def home(request):
    lang_list = quiz_constants.LANGUAGE_LIST
    difficulty_list = quiz_constants.DIFFICULTY_LIST
    quiz_uuid = str(uuid.uuid4())

    if request.method == "POST":
        lang = request.POST["lang"]
        level = request.POST["level"]
        topic = request.POST["topic"] if request.POST["topic"] else ""

        if lang == "Select Programming Language":
            messages.success(
                request, "Hey, You Forgot to Select a Programming Language...."
            )
            return render(
                request,
                "quiz.html",
                {"lang_list": lang_list, "difficulty_list": difficulty_list},
            )
        elif level == "Select level of difficulty":
            messages.success(
                request, "Hey, You Forgot to Select level of difficulty...."
            )
            return render(
                request,
                "quiz.html",
                {"lang_list": lang_list, "difficulty_list": difficulty_list},
            )
        else:
            # Open AI Token
            openai.api_key = dj_settings.OPENAI_TOKEN

            # Create Open AI Instance
            openai.Model.list()

            # Make an Open AI Request
            # try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=quiz_constants.PROMPT.format(
                    lang=lang, level=level, topic=topic
                ),
                temperature=0,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )

            # Parse the Response
            response = response["choices"][0]["text"]

            start_index = response.index("[")
            end_index = response.rindex("]")

            response = ast.literal_eval(response[start_index : end_index + 1])

            quiz_instances = []

            # Save the Instance in Database
            for r in response:
                quiz_instances.append(
                    quiz_models.QuizData(
                        quiz_uuid=quiz_uuid,
                        question=r.get("question"),
                        option_a=r.get("option_a"),
                        option_b=r.get("option_b"),
                        option_c=r.get("option_c"),
                        option_d=r.get("option_d"),
                        code=r.get("code", ""),
                        answer=r.get("correct_answer", r.get("answer", "")),
                    )
                )

            quiz_models.QuizData.objects.bulk_create(quiz_instances)

            quiz_utils.capture_screenshot(quiz_uuid)

            return render(
                request,
                "quiz.html",
                {
                    "lang_list": lang_list,
                    "difficulty_list": difficulty_list,
                    "quiz_list": [],
                    "lang": lang,
                },
            )

            # except Exception as e:
            #     print("====",e)
            #     return render(
            #         request,
            #         "quiz.html",
            #         {"lang_list": lang_list, "difficulty_list": difficulty_list},
            # )

    return render(
        request,
        "quiz.html",
        {"lang_list": lang_list, "difficulty_list": difficulty_list},
    )


def download_image(request):

    template_path = Path(
        "/home/devdarji/workplace/Practice/ChatGpt/codeweb/quiz/templates/test.html"
    )  # Replace with the absolute path to your template
    image_path = "out.png"
    if template_path.exists():
        html = HTML(str(template_path))
        html.write_png(image_path)
        with open(image_path, "rb") as image_file:
            response = HttpResponse(image_file.read(), content_type="image/png")
            response["Content-Disposition"] = 'attachment; filename="output.png"'
            return response
    else:
        return HttpResponse("Template file not found.")


# Test API for download Image
def test_api(request):
    url = (
        "http://127.0.0.1:8000/media/question_62e6f777-4328-4feb-988f-6de3cb474356.png"
    )
    filename = "question_62e6f777-4328-4feb-988f-6de3cb474356.png"
    response = requests.get(url)

    print("status code", response.status_code)
    with open(filename, "rb") as f:
        response = HttpResponse(f.read(), content_type="image/png")
        response[
            "Content-Disposition"
        ] = "inline; filename=question_62e6f777-4328-4feb-988f-6de3cb474356.png"
        return response

    return HttpResponse("Download image successfully.")


def image_api(request, question_uuid):
    question_instance = quiz_models.QuizData.objects.filter(
        question_uuid=question_uuid, is_active=True
    ).last()

    return render(request, "image.html", question_instance.get_details())


def question_answers(request):
    quiz_instances = [
        instance.get_details() for instance in quiz_models.QuizData.objects.all()
    ]

    return render(request, "question_answers.html", {"quiz_instances": quiz_instances})


def new_text_api(request):
    if request.method == "POST":
        openai.api_key = dj_settings.OPENAI_TOKEN

        # Create Open AI Instance
        openai.Model.list()

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=quiz_constants.NEW_PROMPT,
            temperature=0,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        # Parse the Response
        response = response["choices"][0]["text"]

        print(response)

        return render(request, "test.html", {"response": response})
