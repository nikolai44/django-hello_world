from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Tag, Answer, User
from .forms import *

from django.http import HttpResponse, HttpResponseServerError, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login

# Create your views here.


def sidebar():
    tag_list = Tag.objects.hottest()[:10]
    user_list = User.objects.by_rating()[:10]
    return {'tag_list': tag_list,
            'user_list': user_list}


def home(request):
    question_list = Question.objects.get_new()[:20]
    extra_context = sidebar()
    if question_list is None or extra_context['user_list'] is None or extra_context['tag_list'] is None:
        raise HttpResponseServerError
    context = {'question_list': question_list, }
    context.update(extra_context)           # eq add
    return render(request, 'home.html', context)


def hot(request):
    question_list = Question.objects.get_hot()[:20]
    extra_context = sidebar()
    if question_list is None or extra_context['user_list'] is None or extra_context['tag_list'] is None:
        raise HttpResponseServerError
    context = {'question_list': question_list, }
    context.update(extra_context)           # eq add
    return render(request, 'home.html', context)


def new(request):
    return redirect(request, '')


def settings(request, user_id):
    user = User.objects.by_username(user_id)
    if user is None:
        raise Http404
    context = {'profile': user}
    extra_context = sidebar()
    context.update(extra_context)
    return render(request, "settings.html", context)


def new_question(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddQuestionForm(request.POST)
            if form.is_valid():
                q = Question.objects.create(author=request.user,
                                            title=form.cleaned_data.get("title"),
                                            text=form.cleaned_data.get("text"))
                tags = form.cleaned_data.get("tags").replace(' ', '').split(",")[:3]
                for tag in tags:
                    t = Tag.objects.get_or_create(name=tag)[0]
                    q.tags.add(t)
                q.save()
                return redirect(f"/question/{q.id}")
            else:
                context = {"form": form}
                extra_context = sidebar()
                context.update(extra_context)
                return render(request, "add_question.html", context)
        else:
            form = AddQuestionForm
            context = {"form": form}
            extra_context = sidebar()
            context.update(extra_context)
            return render(request, "add_question.html", context)
    else:
        return redirect("/accounts/login")


def question(request, question_id):
    if request.user.is_authenticated:
        q = get_object_or_404(Question, pk=question_id)
        if request.method == "POST":
            form = AddAnswerForm(request.POST)
            if form.is_valid():
                a = Answer.objects.create(
                    author=User.objects.by_username(request.user),
                    question=q,
                    text=form.cleaned_data.get('text')
                )
                a.save()
                return redirect(f'/question/{question_id}')
            else:
                context = {"form": form}
                extra_context = sidebar()
                context.update(extra_context)
                return render(request, "question.html", context)
        else:
            answers = Answer.objects.get_for_answer(question_id)
            form = AddAnswerForm()
            context = {"question": q,
                       "answers": answers,
                       "form": form,
                       }
            extra_context = sidebar()
            context.update(extra_context)
            return render(request, "question.html", context)
    else:
        return redirect("/accounts/login")


def question_by_tag(request, tag):
    return render(request, "settings.html")


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            if form.cleaned_data.get('avatar') is not None:
                user.avatar = form.cleaned_data.get('avatar')
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("")
        else:
            context = {'form': form, }
            extra_context = sidebar()
            context.update(extra_context)           # eq add
            return render(request, template_name="registration/registration_form.html", context=context)

    else:
        form = UserRegistrationForm
        context = {'form': form, }
        extra_context = sidebar()
        context.update(extra_context)           # eq add
        return render(request, template_name="registration/registration_form.html", context=context)

