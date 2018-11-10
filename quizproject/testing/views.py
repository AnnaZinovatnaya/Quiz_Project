from django.http import Http404, HttpResponseRedirect
from . import models
from django.shortcuts import render, redirect
from django.urls import reverse


def all_tests(request):
    return render(request, 'allTests.html', context={'tests_list': models.Test.objects.all()})


def test(request, test_id):
    try:
        t = models.Test.objects.get(pk=test_id)
        questions = models.Question.objects.filter(test__pk=test_id)
        answers = []
        for q in questions:
            q_answers = models.Answer.objects.filter(question__pk=q.id)
            for a in q_answers:
                answers.append(a)
    except models.Test.DoesNotExist:
        raise Http404
    return render(request, 'test.html', {'test': t, 'questions_list': questions, 'answers_list': answers})


def check(request, test_id):
    try:
        t = models.Test.objects.get(pk=test_id)
        questions = models.Question.objects.filter(test__pk=test_id)
        answers = []
        for q in questions:
            q_answers = models.Answer.objects.filter(question__pk=q.id)
            for a in q_answers:
                answers.append(a)
    except models.Test.DoesNotExist:
        raise Http404
    return render(request, 'test_result.html', {'test': t, 'questions_list': questions, 'answers_list': answers})


def redirect_to_all_tests(request):
    return HttpResponseRedirect(reverse('all_tests'))
