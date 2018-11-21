from django.contrib import admin
from .models import Test, Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fields = ['test', 'name']
    inlines = [AnswerInline]
    list_display = ('name', 'test')
    list_filter = ['test']

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
