from django.http import Http404, HttpResponseRedirect
from . import models
from django.shortcuts import render, redirect
from django.urls import reverse


def all_tests(request):
    return render(request, 'allTests.html', context={'tests_list': models.Test.objects.all()})

def question(request, test_id, question_number):
    try:
        t = models.Test.objects.get(pk=test_id)

        # find all questions of a given test
        questions = models.Question.objects.filter(test__pk=test_id)

        # find needed question
        question = questions[int(question_number)-1]

        # find answers of the question
        answers = models.Answer.objects.filter(question__pk=question.id)
    except models.Test.DoesNotExist:
        raise Http404
    return render(request, 'question.html', {'test': t, 'question_number': question_number, 'question': question, 'answers': answers})


def check(request, test_id, question_number):
    try:
        t = models.Test.objects.get(pk=test_id)

        # find all questions of a given test
        questions = models.Question.objects.filter(test__pk=test_id)

        # find needed question
        question = questions[int(question_number)-1]

        # find answers of the question
        answers = models.Answer.objects.filter(question__pk=question.id)
        number_of_answers = len(answers)

        # get user answers from form
        user_answers = []
        i = 1
        while i < (number_of_answers + 1):
            user_answer = request.POST.get('answer'+str(i))
            if user_answer == None:
                user_answers.append(False)
            else:
                user_answers.append(True)
            i = i + 1
        next_question = int(question_number)+1
        if next_question == (len(questions) + 1):
            next_question = 0
    except models.Test.DoesNotExist:
        raise Http404
    return render(request, 'question_result.html', {'test': t, 'question': question, 'answers': answers, 'user_answers': user_answers, 'next_question': str(next_question)})


def redirect_to_all_tests(request):
    return HttpResponseRedirect(reverse('all_tests'))
