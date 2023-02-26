from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings as dj_settings

from web_app import models as web_app_models
from web_app import forms as web_app_forms
from web_app import constants as web_app_constants

import openai


def home(request):

    """
        - Add Question openai return that Question Answer in Code.
    """

    # Language List
    lang_list = web_app_constants.LANGUAGE_LIST

    if request.method == "POST":
        code = request.POST["code"]
        lang = request.POST["lang"]

        if lang == "Select Programming Language":
            messages.success(
                request, "Hey, You Forgot to Select a Programming Language...."
            )
            return render(
                request,
                "home.html",
                {"lang_list": lang_list, "code": code, "response": code, "lang": lang},
            )
        else:

            # Open AI Token
            openai.api_key = dj_settings.OPENAI_TOKEN

            # Create Open AI Instance
            openai.Model.list()

            # Make an Open AI Request
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Responsd only with code. Fix this {lang} code: {code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )

                # Parse the Response
                response = response["choices"][0]["text"]

                # Save the Instance in Database
                web_app_models.CodeQuestionAnswer.objects.create(
                    user=request.user, question=code, answer=response, language=lang
                )

                return render(
                    request,
                    "home.html",
                    {"lang_list": lang_list, "response": response, "lang": lang},
                )

            except Exception as e:

                return render(
                    request,
                    "home.html",
                    {"lang_list": lang_list, "response": e, "lang": lang},
                )

    return render(request, "home.html", {"lang_list": lang_list})


def suggest(request):
    """
        - Suggest Code for Question
    """

    # Language List
    lang_list = web_app_constants.LANGUAGE_LIST

    if request.method == "POST":
        code = request.POST["code"]
        lang = request.POST["lang"]

        if lang == "Select Programming Language":
            messages.success(
                request, "Hey, You Forgot to Select a Programming Language...."
            )
            return render(
                request,
                "suggest.html",
                {"lang_list": lang_list, "code": code, "response": code, "lang": lang},
            )
        else:
            # Open AI Token
            openai.api_key = dj_settings.OPENAI_TOKEN

            # Create Open AI Instance
            openai.Model.list()

            # Make an Open AI Request
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Responsd only with code. {code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )

                # Parse the Response
                response = response["choices"][0]["text"]

                # Save the Instance in Database
                web_app_models.CodeQuestionAnswer.objects.create(
                    user=request.user, question=code, answer=response, language=lang
                )

                return render(
                    request,
                    "suggest.html",
                    {"lang_list": lang_list, "response": response, "lang": lang},
                )

            except Exception as e:

                return render(
                    request,
                    "suggest.html",
                    {"lang_list": lang_list, "response": e, "lang": lang},
                )

    return render(request, "suggest.html", {"lang_list": lang_list})


def login_user(request):
    """
        - Login User
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate User
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have been Logged in successfully...")
            return redirect("home")
        else:
            messages.success(request, "Something went wrong...Please Try again..")
            return redirect("login")
    else:
        return render(request, "home.html", {})


def logout_user(request):
    """
        - Logout User
    """
    logout(request)
    messages.success(request, "You Have been Logged Out...")
    return redirect("home")


def register_user(request):
    """
        - Register User
    """
    if request.method == "POST":
        form = web_app_forms.SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "You Have been Registered... Congratulation...")

            return redirect("home")
    else:
        form = web_app_forms.SignUpForm()

    return render(request, "register.html", {"form": form})


def user_data(request):
    """
        - Get Particular All Data
    """
    if request.user.is_authenticated:
        code_question_answer_instances = web_app_models.CodeQuestionAnswer.objects.filter(
            user_id=request.user.id
        )
        return render(
            request,
            "user_data.html",
            {"code_question_answer_instances": code_question_answer_instances},
        )
    else:
        messages.success(request, "You Have to Must LogIn to view this Page...")
        return render(request, "home.html", {})


def delete_data(request, instance_id):
    """
        - Delete User Data Instance
    """
    web_app_models.CodeQuestionAnswer.objects.filter(id=instance_id).delete()
    messages.success(request, "Code Question Answer Instance Deleted Successfully")
    return redirect("user-data")
