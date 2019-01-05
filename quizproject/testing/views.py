from django.http import Http404, HttpResponseRedirect
from . import models
from django.shortcuts import render
from django.urls import reverse
import uuid
import logging


logger = logging.getLogger('django')

current_user_test_uuid = "00000000000000000000000000000000"


def is_taken_by_current_user(test, user):
    user_answers = models.UserAnswer.objects.filter(user=user)
    for user_answer in user_answers:
        if user_answer.answer.question.test == test:
            return True
    return False


def show_all_tests(request):
    # dictionary {test.id : is_taken}
    tests = {}
    # tests that have at least one question
    valid_tests = []
    for test in models.Test.objects.all():
        if len(models.Question.objects.filter(test__pk=test.id)) > 0:
            valid_tests.append(test)
            tests.update({test.id: is_taken_by_current_user(test, request.user)})
    logger.info('valid_tests: ' + str(valid_tests))
    logger.info('user_tests: ' + str(tests))
    return render(request, 'allTests.html', context={'valid_tests': valid_tests, 'user_tests': tests})


def show_question(request, test_id, question_number):
    if str(question_number) == '1':
        global current_user_test_uuid
        current_user_test_uuid = str(uuid.uuid4())
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
            user_answer = request.POST.get('answer' + str(i))

            if user_answer is None:
                user_answers.append(False)
            else:
                user_answers.append(True)
            i = i + 1
        next_question = int(question_number)+1
        if next_question == (len(questions) + 1):
            next_question = 0  # there are no more questions

        k = 0
        for answer in answers:
            user_answer_to_save = models.UserAnswer()
            user_answer_to_save.user_test_uuid = current_user_test_uuid
            user_answer_to_save.user = request.user
            user_answer_to_save.answer = answer
            user_answer_to_save.is_correctly_answered = (answer.is_correct == user_answers[k])
            k = k + 1
            # TODO save answers only is user has finished the test (transactions?)
            user_answer_to_save.save()

    except models.Test.DoesNotExist:
        raise Http404
    return render(request, 'question_result.html', {'test': test, 'question': question, 'answers': answers, 'user_answers': user_answers, 'next_question': str(next_question)})


def redirect_to_all_tests(request):
    return HttpResponseRedirect(reverse('all_tests'))


# function that counts test score of a given user
def count_test_result(test_id):
    number_of_correct_answers = 0
    total_number_of_answers = 0

    for q in models.Question.objects.filter(test__pk=test_id):
        total_number_of_answers = total_number_of_answers + len(models.Answer.objects.filter(question__pk=q.id))

        for answer in models.Answer.objects.filter(question__pk=q.id):
            if models.UserAnswer.objects.filter(answer=answer, user_test_uuid=current_user_test_uuid)[0].is_correctly_answered:
                number_of_correct_answers = number_of_correct_answers + 1

    test_result = round((number_of_correct_answers / total_number_of_answers) * 100)

    return test_result


def show_test_report(request, test_id):
    test_result = count_test_result(test_id)
    return render(request, 'test_result.html', {'test_result': test_result})



