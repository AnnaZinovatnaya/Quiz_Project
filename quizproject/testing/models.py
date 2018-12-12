from django.db import models
from django.contrib import auth


class Test(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=150)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Answer(models.Model):
    text = models.CharField(max_length=60)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    User = auth.settings.AUTH_USER_MODEL
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    is_correctly_answered = models.BooleanField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
