from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import CodeQuestionAnswer
from .forms import SignUpForm

import openai


def home(request):
    lang_list = [
        "bash",
        "basic",
        "c",
        "clike",
        "cobol",
        "cpp",
        "csharp",
        "css",
        "csv",
        "dart",
        "django",
        "dns-zone-file",
        "docker",
        "git",
        "go",
        "go-module",
        "graphql",
        "hpkp",
        "hsts",
        "icon",
        "ignore",
        "java",
        "javadoclike",
        "javascript",
        "js-extras",
        "js-templates",
        "jsdoc",
        "json",
        "json5",
        "jsstacktrace",
        "jsx",
        "julia",
        "kotlin",
        "markdown",
        "markup",
        "markup-templating",
        "matlab",
        "mongodb",
        "monkey",
        "nginx",
        "pascal",
        "perl",
        "php",
        "plsql",
        "python",
        "r",
        "regex",
        "ruby",
        "rust",
        "sas",
        "sass",
        "scala",
        "scss",
        "solidity",
        "sql",
        "squirrel",
        "swift",
        "tsx",
        "typescript",
        "uri",
        "vbnet",
        "visual-basic",
    ]

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
            openai.api_key = "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"

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
                CodeQuestionAnswer.objects.create(
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
    lang_list = [
        "bash",
        "basic",
        "c",
        "clike",
        "cobol",
        "cpp",
        "csharp",
        "css",
        "csv",
        "dart",
        "django",
        "dns-zone-file",
        "docker",
        "git",
        "go",
        "go-module",
        "graphql",
        "hpkp",
        "hsts",
        "icon",
        "ignore",
        "java",
        "javadoclike",
        "javascript",
        "js-extras",
        "js-templates",
        "jsdoc",
        "json",
        "json5",
        "jsstacktrace",
        "jsx",
        "julia",
        "kotlin",
        "markdown",
        "markup",
        "markup-templating",
        "matlab",
        "mongodb",
        "monkey",
        "nginx",
        "pascal",
        "perl",
        "php",
        "plsql",
        "python",
        "r",
        "regex",
        "ruby",
        "rust",
        "sas",
        "sass",
        "scala",
        "scss",
        "solidity",
        "sql",
        "squirrel",
        "swift",
        "tsx",
        "typescript",
        "uri",
        "vbnet",
        "visual-basic",
    ]

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
            openai.api_key = "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"

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
                response = response["choices"][0]["text"]

                # Save the Instance in Database
                CodeQuestionAnswer.objects.create(
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
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

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
    logout(request)
    messages.success(request, "You Have been Logged Out...")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have been Registered... Congatulation...")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form})


def user_data(request):
    if request.user.is_authenticated:
        code_question_answer_instances = CodeQuestionAnswer.objects.filter(
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
    CodeQuestionAnswer.objects.filter(id=instance_id).delete()
    # code_question_answer_instances = CodeQuestionAnswer.objects.filter(user_id=request.user.id)
    messages.success(request, "Code Question Answer Instance Deleted Successfully")
    return redirect("user-data")
    # render(request, 'user_data.html',{'code_question_answer_instances': code_question_answer_instances})
