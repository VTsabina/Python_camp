import random as rd
import time
import multiprocessing as mp


class Question:
    def __init__(self, q_str: str):
        self.data = q_str
        self.words = self.data.split()
        self.num_words = len(self.words)
        self.is_the_best = False
        self.golden_ratio = (1 + 5 ** 0.5) / 2
        self.answered = 0

    def answer(self, gender):
        probabilities = list()
        probabilities.append(1 / self.golden_ratio)
        a = 1 / self.golden_ratio  # 1st
        for i in range(1, self.num_words):
            probabilities.append(1 - sum(probabilities))

        if gender == 'Ж':
            probabilities.reverse()

        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        answer = rd.choices(self.words, weights=probabilities, k=1)[0]
        return answer


class Student:
    def __init__(self, s_name, s_gender):
        self.name = s_name
        self.gender = s_gender
        self.time = 0
        self.status = "Очередь"
        self.answer_time = 0

    def __str__(self):
        return f'{self.name} ({self.gender}), статус: {self.status}'

    def choose_questions(self, q_col):
        questions = rd.choices(q_col, k=3)
        return questions

    def give_answer(self, question: Question):
        return question.answer(self.gender)


class Examiner:
    def __init__(self, ex_name, ex_gender):
        self.name = ex_name
        self.gender = ex_gender
        self.mood = "Neutral"
        self.coffeebreak = 0
        self.failed = 0
        self.current = "-"
        self.count = 0
        self.breaktime = 0
        self.is_on_break = False
        self.finished = 0

    def pick_student(self, student_list):
        student = student_list.get()
        return student

    def check_answer(self, question: Question, students_answer: str):
        right_answers = []
        answer = question.answer(self.gender)
        right_answers.append(answer)
        while len(question.words) < len(right_answers):
            chance = rd.randint(5, 7)
            if chance == 7:
                while answer in right_answers:
                    answer = question.answer(self.gender),
                    right_answers.append(answer)

        if students_answer in right_answers:
            return 1
        else:
            return 0

    def get_mood(self):
        mood_idx = rd.randint(1, 8)
        if mood_idx == 1:
            self.mood = "Bad"
        elif mood_idx in (2, 3):
            self.mood = "Good"
        else:
            self.mood = "Neutral"


class ExamManager:
    def __init__(self):
        self.results = []
        self.examiners = []
        self.questions = self.get_questions()
        self.duration = 0.0
        self.best_students = []
        self.best_examiners = []
        self.best_questions = []
        self.expelled = []
        self.start_time = time.time()
        self.worktime = []
        self.question_stats = []

    def timer(self):
        while True:
            self.worktime["time"] = time.time() - self.start_time
            time.sleep(1)

    def get_students(self) -> list:
        students = []
        with open("students.txt", "r") as file:
            students_data = file.readlines()
        for item in students_data:
            item = item.split()
            students.append(Student(*item))
        return students

    def get_examiners(self) -> list:
        examiners = []
        with open("examiners.txt", "r") as file:
            examiners_data = file.readlines()
        for item in examiners_data:
            item = item.split()
            examiners.append(Examiner(*item))
        return examiners

    def get_questions(self) -> list:
        questions = []
        with open("questions.txt", "r") as file:
            questions_data = file.readlines()
        for item in questions_data:
            item = item.split('\n')
            questions.append(Question(item[0]))
        return questions

    def work(self, examiner: Examiner, student_list):
        while not student_list.empty():

            if examiner.is_on_break == True:
                time.sleep(examiner.coffeebreak)
                examiner.is_on_break = False

            examiner.get_mood()
            res = 0

            student: Student = examiner.pick_student(student_list)
            examiner.current = student.name
            self.update_examiners_info(examiner)

            student.answer_time = rd.randint(
                len(examiner.name) - 1, len(examiner.name) + 1)

            time.sleep(student.answer_time)
            exam_paper = student.choose_questions(self.questions)

            for question in exam_paper:
                answer = student.give_answer(question)
                res += examiner.check_answer(question, answer)
                self.question_stats[question.data] += res
            if examiner.mood == "Neutral":
                pass
            elif examiner.mood == "Good":
                res = 3
            if res > 1:
                student.status = "Сдал"
            else:
                student.status = "Провалил"
                examiner.failed += 1
            examiner.count += 1

            if self.worktime["time"] > 30 and examiner.coffeebreak == 0:
                examiner.breaktime = self.worktime["time"]
                examiner.finished = self.worktime["time"]
                examiner.coffeebreak = rd.randint(12, 18)
                examiner.current = "-"
                examiner.is_on_break = True
                self.update_examiners_info(examiner)

            # self.update_examiners_info(examiner)
            self.results.append(student)

        examiner.current = "-"
        examiner.finished = self.worktime["time"] - examiner.coffeebreak
        self.update_examiners_info(examiner)

    def update_examiners_info(self, examiner):
        self.examiners[examiner.name] = examiner

    def find_best_students(self):
        passed_students = [
            student for student in self.results if student.status == 'Сдал']
        answer_times = [student.answer_time for student in passed_students]
        for student in passed_students:
            if student.answer_time == min(answer_times):
                self.best_students.append(student.name)
        return self.best_students

    def find_best_examiners(self):
        fail_percentage = [examiner.failed /
                           examiner.count for examiner in self.examiners.values()]
        for examiner in self.examiners.values():
            if examiner.failed / examiner.count == min(fail_percentage):
                self.best_examiners.append(examiner.name)
        return self.best_examiners

    def find_best_questions(self):
        max_answers = max(self.question_stats.values())
        for question in self.question_stats.keys():
            if self.question_stats[question] == max_answers:
                self.best_questions.append(question)
        return self.best_questions

    def find_expelled(self):
        failed_students = [
            student for student in self.results if student.status == 'Провалил']
        answer_times = [student.answer_time for student in failed_students]
        for student in failed_students:
            if student.answer_time == min(answer_times):
                self.expelled.append(student.name)
        return self.expelled

    def summurize_exam(self):
        passed_students = [
            student for student in self.results if student.status == 'Сдал']
        if len(passed_students) / len(self.results) >= 85:
            print("Экзамен удался")
        else:
            print("Экзамен не удался")
