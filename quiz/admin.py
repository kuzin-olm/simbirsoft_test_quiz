from django.contrib import admin
from django import forms

from .models import Question, Choice, Quiz, LandingQuiz


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['text']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('text', 'get_title_quiz')


class QuestInline(admin.TabularInline):
    model = Question
    extra = 0
    show_change_link = True


class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Основные поля', {'fields': ['title', 'text', 'btn_text']}),
    ]
    inlines = [QuestInline]
    list_display = ('name', )


class LandingQuizForm(forms.ModelForm):
    name = forms.CharField(label='Название')
    quiz = forms.ModelChoiceField(
        label='Опрос',
        queryset=Quiz.objects.all(),
    )

    class Meta:
        model = LandingQuiz
        fields = ['name', 'quiz']


class LandingQuizAdmin(admin.ModelAdmin):
    fields = ('name', 'quiz')
    list_display = ('name',)
    form = LandingQuizForm


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(LandingQuiz, LandingQuizAdmin)
