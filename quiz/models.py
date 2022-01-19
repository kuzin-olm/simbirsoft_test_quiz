from django.contrib import admin
from django.db import models
from django.core.validators import MinValueValidator


class Quiz(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название опроса', default='name')
    title = models.CharField(max_length=200, verbose_name='Основной заголовок на лэндинге', default='title')
    text = models.CharField(max_length=200, verbose_name='Поясняющий текст', default='text')
    btn_text = models.CharField(max_length=200, verbose_name='Текст на кнопке', default='btn_text')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Все опросы'


class LandingQuiz(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', default='name')
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'id={self.pk} "{self.name}"'

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Распределение опросов'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name='Текст вопроса')
    idx = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Порядковый номер вопроса')

    @admin.display(description='опрос')
    def get_title_quiz(self):
        return f'{self.quiz.name}'

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['idx']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ(ы)')
    idx = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Порядковый номер ответа')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'
        ordering = ['idx']
