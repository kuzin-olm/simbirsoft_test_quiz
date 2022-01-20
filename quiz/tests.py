from django.test import TestCase
from typing import List
from .services import QuizResultService
from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO


class BaseTestCase(TestCase):
    def setUp(self):
        choices1: List[ChoiceDTO] = [
            ChoiceDTO(
                "1-1-1",
                "An elephant",
                True
            ),
            ChoiceDTO(
                "1-1-2",
                "A mouse",
                False
            )
        ]

        choices2: List[ChoiceDTO] = [
            ChoiceDTO(
                "1-2-1",
                "A rainbow",
                True
            ),
            ChoiceDTO(
                "1-2-2",
                "A mouse",
                False
            ),
            ChoiceDTO(
                "1-2-3",
                "A pivozavr",
                True
            )
        ]

        questions: List[QuestionDTO] = [
            QuestionDTO(
                "1-1",
                "Who is bigger?",
                choices1
            ),

            QuestionDTO(
                "1-2",
                "Who is the fictional animal?",
                choices2
            )
        ]

        self.quiz_dto = QuizDTO(
            "1",
            "Animals",
            questions
        )

    def test_success_quiz_result(self):
        answers: List[AnswerDTO] = [
            AnswerDTO(
                "1-1",
                ["1-1-1"]
            ),
            AnswerDTO(
                "1-2",
                ["1-2-1", "1-2-3"]
            )
        ]

        answers_dto = AnswersDTO(
            "1",
            answers
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 1.00)

    def test_failure_quiz_result(self):
        answers: List[AnswerDTO] = [
            AnswerDTO(
                "1-1",
                ["1-1-2"]
            ),
            AnswerDTO(
                "1-2",
                ["1-2-1", "1-2-2", "1-2-3"]
            )
        ]

        answers_dto = AnswersDTO(
            "1",
            answers
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.00)

    def test_half_failure_quiz_result(self):
        answers: List[AnswerDTO] = [
            AnswerDTO(
                "1-1",
                ["1-1-1"]
            ),
            AnswerDTO(
                "1-2",
                ["1-2-2", "1-2-3"]
            )
        ]

        answers_dto = AnswersDTO(
            "1",
            answers
        )

        quiz_result_service = QuizResultService(
            self.quiz_dto,
            answers_dto
        )

        self.assertEqual(quiz_result_service.get_result(), 0.50)
