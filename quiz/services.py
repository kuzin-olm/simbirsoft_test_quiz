from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswersDTO
from typing import Union

from .models import Question, Quiz, LandingQuiz


def get_quiz_dto() -> QuizDTO:
    """получить dto действующего опроса"""
    quiz_obj: Quiz = LandingQuiz.objects.first().quiz

    quiz_dto = QuizDTO(uuid=str(quiz_obj.pk), title=quiz_obj.title, questions=[])

    for question in quiz_obj.question_set.all():
        question_dto = QuestionDTO(uuid=str(question.pk), text=question.text, choices=[])
        for choice in question.choice_set.all():
            choice_dto = ChoiceDTO(uuid=str(choice.pk), text=choice.text, is_correct=choice.is_correct)
            question_dto.choices.append(choice_dto)
        quiz_dto.questions.append(question_dto)

    return quiz_dto


def get_question_by_id(question_id) -> Union[Question, None]:
    """получить объект question из бд"""
    try:
        question_obj = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return None
    return question_obj


class QuizResultService:
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def _get_question_by_uuid(self, uuid: str) -> QuestionDTO:
        """получить question dto из переданного в конструктор класса quiz_dto"""
        questions = filter(lambda q: q.uuid == uuid, self.quiz_dto.questions)
        return list(questions)[0]

    @staticmethod
    def _get_choice_from_question_by_uuid(question: QuestionDTO, uuid: str) -> ChoiceDTO:
        """получить choice dto из переданного в функцию question dto"""
        choices = filter(lambda c: c.uuid == uuid, question.choices)
        return list(choices)[0]

    def get_result(self) -> float:
        """
        расчитывает результат прохождения теста

        return: от 0.00 до 1.00 включительно, где 0 - это 0% прохождения теста, а 1 - 100%.
        """
        total_score = 0.0

        for answer_dto in self.answers_dto.answers:
            score = 0.0
            quiz_question = self._get_question_by_uuid(uuid=answer_dto.question_uuid)

            for answer_choice_uuid in answer_dto.choices:
                choice = self._get_choice_from_question_by_uuid(quiz_question, answer_choice_uuid)
                if choice.is_correct:
                    score += 1

            # кол-во правильных ответов
            qty_true_choices = len(list(filter(lambda _choice: _choice.is_correct, quiz_question.choices)))
            # засчитать правильный ответ, если
            # кол-во ответов == кол-во правильных ответов
            # и кол-во засчитанных ответов == кол-во правильных ответов
            total_score += 1 if score == qty_true_choices == len(answer_dto.choices) else 0

        return round(total_score/len(self.quiz_dto.questions), 2)
