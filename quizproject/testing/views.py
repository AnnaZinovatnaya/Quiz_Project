from django.http import Http404, HttpResponseRedirect
from . import models
from django.shortcuts import render, redirect
from django.urls import reverse


def show_all_tests(request):
    tests = models.Test.objects.all()
    valid_tests = []
    for test in tests:
        if len(models.Question.objects.filter(test__pk=test.id)) > 0:
            valid_tests.append(test)
    return render(request, 'allTests.html', context={'tests_list': valid_tests})


def show_question(request, test_id, question_number):
    try:
        test = models.Test.objects.get(pk=test_id)

        # find all questions of a given test
        questions = models.Question.objects.filter(test__pk=test_id)

        # find needed question
        question = questions[int(question_number)-1]

        # find answers of the question
        answers = models.Answer.objects.filter(question__pk=question.id)
    except models.Test.DoesNotExist:
        raise Http404
    return render(request, 'question.html', {'test': test, 'question_number': question_number,
                                             'question_id': question.id, 'question': question, 'answers': answers})


def check_question(request, test_id, question_number):
    try:
        test = models.Test.objects.get(pk=test_id)

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

        k = 0
        for answer in answers:
            user_answer_to_save = models.UserAnswer()
            user_answer_to_save.user = request.user
            user_answer_to_save.answer = answer
            user_answer_to_save.is_correctly_answered = (answer.is_correct == user_answers[k])
            k = k + 1
            user_answer_to_save.save()

    except models.Test.DoesNotExist:
        raise Http404
    return render(request, 'question_result.html', {'test': test, 'question': question, 'answers': answers, 'user_answers': user_answers, 'next_question': str(next_question)})


def redirect_to_all_tests(request):
    return HttpResponseRedirect(reverse('all_tests'))
