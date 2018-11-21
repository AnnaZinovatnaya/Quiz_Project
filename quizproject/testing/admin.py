from django.contrib import admin
from .models import Test, Question, Answer
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(AnswerInlineFormSet, self).clean()
        total_checked = 0

        for form in self.forms:
            if not form.is_valid():
                return
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                if form.cleaned_data['is_correct']:
                    total_checked += 1

        if total_checked < 1:
            raise ValidationError("You must have at least one correct answer")

class AnswerInline(admin.TabularInline):
    formset = AnswerInlineFormSet
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

class TestAdmin(admin.ModelAdmin):
    list_display = ["name", "is_valid"]

    def is_valid(self, obj):
        return len(Question.objects.filter(test__pk=obj.id)) != 0

    is_valid.boolean = True

admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
