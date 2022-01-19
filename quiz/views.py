from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .models import Question, LandingQuiz, Quiz

from .dto import AnswersDTO, AnswerDTO, QuizDTO
from .services import get_question_by_id, get_quiz_dto, QuizResultService


def update_quiz_user_answers(request) -> AnswersDTO:
    """считать ответ из формы, добавить/заменить ответ в сессии"""
    question_uuid = request.POST.get('uuid')
    answer_choices = request.POST.getlist('answer')

    user = AnswersDTO(*request.session['quiz'])
    current_answer = AnswerDTO(question_uuid, answer_choices)

    for idx, user_answer in enumerate(user.answers):
        user_answer_dto = AnswerDTO(*user_answer)
        user.answers[idx] = user_answer_dto
        if user_answer_dto.question_uuid == current_answer.question_uuid:
            del user.answers[idx]

    if len(answer_choices) > 0:
        user.answers.append(current_answer)
    return user


class StartView(TemplateView):
    template_name = 'start.html'

    def get_context_data(self, **kwargs):
        quiz_obj: Quiz = LandingQuiz.objects.first().quiz
        try:
            question_obj: Question = quiz_obj.question_set.get(idx=1)
            start_uuid = question_obj.pk
        except Question.DoesNotExist:
            start_uuid = None

        kwargs['start_uuid'] = start_uuid
        kwargs['quiz'] = quiz_obj
        return super().get_context_data(**kwargs)


class ResultView(TemplateView):
    template_name = 'result.html'

    def get(self, request, *args, **kwargs):
        return redirect('start')

    def post(self, request, *args, **kwargs):
        if request.session.get('quiz') is None:
            return redirect('start')

        user: AnswersDTO = update_quiz_user_answers(request)
        quiz_dto: QuizDTO = get_quiz_dto()
        quiz_service = QuizResultService(quiz_dto=quiz_dto, answers_dto=user)

        del request.session['quiz']

        context = dict(
            score=quiz_service.get_result()
        )
        return render(request, self.template_name, context=context, *args, **kwargs)


class QuestionView(TemplateView):
    template_name = 'question.html'

    def get(self, request, *args, **kwargs):
        uuid_question: str = kwargs.get('uuid')

        question_obj: Question = get_question_by_id(question_id=int(uuid_question))
        quiz_obj: Quiz = question_obj.quiz

        if request.session.get('quiz') is None:
            request.session['quiz'] = AnswersDTO(quiz_uuid=quiz_obj.pk, answers=list())

        has_next: bool = question_obj.idx < quiz_obj.question_set.count()
        has_prev: bool = question_obj.idx > 1
        finish: bool = question_obj.idx == quiz_obj.question_set.count()
        multiselect: bool = question_obj.choice_set.filter(is_correct=True).count() > 1

        # находим ранее выбранные ответы на текущий question
        user = update_quiz_user_answers(request)
        user_prev_choices = list()
        for answer in user.answers:
            if answer.question_uuid == uuid_question:
                user_prev_choices = answer.choices
                break

        context = dict(
            question=question_obj,
            multiselect=multiselect,
            user_prev_choices=user_prev_choices,
            next=has_next,
            next_uuid=quiz_obj.question_set.get(idx=question_obj.idx + 1).pk if has_next else None,
            prev=has_prev,
            prev_uuid=quiz_obj.question_set.get(idx=question_obj.idx - 1).pk if has_prev else None,
            finish=finish
        )
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        # обновим ответы пользователя и сохраним в сессии
        request.session['quiz'] = update_quiz_user_answers(request)
        return self.get(request, *args, **kwargs)
