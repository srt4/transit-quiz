from operator import attrgetter
from random import shuffle
import uuid
from dict_utils import LRUCache

__author__ = 'Spencer Thomas'


class DifficultyLevel():
    EASY = .25  # 75th %ile of routes by frequency
    MEDIUM = .5  # 50th %ile of routes by frequency
    DIFFICULT = .75  # 25th %ile of routes by frequency


class Question():

    def __init__(self, answer_route, all_routes):
        """

        :param answer_route: Route
        :param all_routes: list of Route
        """
        self.__answer_route = answer_route
        self.__all_routes = all_routes
        self.__question_id = uuid.uuid4()

    def is_correct(self, route_id):
        return route_id == self.__answer_route.route_id

    def get_routes(self):
        return self.__all_routes

    def get_question_id(self):
        return self.__question_id

    def __str__(self):
        return "answerroute=" + str(self.__answer_route) + ", allroutes=" + str([str(route) for route in self.__all_routes])


class QuizManager():

    ROUTES_PER_QUESTION = 5

    def __init__(self, transit_agency, difficulty, number_questions):
        """

        :type transit_agency: TransitAgency
        """
        self.__transit_agency = transit_agency
        self.__routes_used_as_answers = []
        self.__questions = []
        self.__instance_guid = uuid.uuid4()
        self.__difficulty = difficulty
        self.__number_questions = number_questions
        self.__answers = {}

    def get_next_question(self):
        """

        :rtype : Question
        """
        routes = self.__get_random_routes(self.ROUTES_PER_QUESTION, self.__difficulty,
                                          tuple(self.__routes_used_as_answers))
        answer = routes[0]
        shuffle(routes)
        self.__routes_used_as_answers.append(answer)
        question = Question(answer, routes)
        self.__questions.append(question)
        return question

    def has_next_question(self):
        return len(self.__questions) < self.__number_questions

    def get_instance_id(self):
        return str(self.__instance_guid)

    def submit_answer(self, question_id, answer_id):
        self.__answers[question_id] = answer_id

    def get_results(self):
        if self.has_next_question():
            raise Exception("Quiz not completed")
        correct = 0
        for question_id, answer_id in self.__answers.iteritems():
            if self.__questions[question_id].is_correct(answer_id):
                correct += 1
        return correct / len(self.__answers)

    def __get_random_routes(self, count, difficulty_level, excluded_routes=()):
        # remove any excluded routes
        route_candidates = [route for route in self.__transit_agency.get_routes() if route not in excluded_routes]

        route_candidates = sorted(route_candidates, key=attrgetter("number_trips"), reverse=True)
        number_to_show = difficulty_level * len(route_candidates)
        route_candidates = route_candidates[:int(number_to_show)]
        shuffle(route_candidates)
        return route_candidates[:count]

    def __str__(self):
        return "QuizManager<" + str(self.__instance_guid) + ">"


class QuizManagerRepository():

    __quiz_managers = LRUCache(1024)

    def __init__(self, agency):
        self.__agency = agency

    def get_quiz_manager(self, quiz_manager_id):
        # Here we can choose to quietly handle exceptions, or
        # let the user know that their session expired or the
        # service was restarted. Currently opting for the former.
        if not self.__quiz_managers.contains_key(quiz_manager_id):
            self.__quiz_managers.set(quiz_manager_id, QuizManager(self.__agency))

        return self.__quiz_managers.get(quiz_manager_id)

    def initialize_quiz_manager(self, difficulty, number_questions):
        quiz_manager = QuizManager(self.__agency, difficulty, number_questions)
        return quiz_manager.get_instance_id()