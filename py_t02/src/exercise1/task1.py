from entities import ExamManager
import multiprocessing as mp
from prettytable import PrettyTable
import os
import time


def print_students(app, states, table_st):
    for student in app.results:
        states[student.name] = student.status
    for name in states.keys():
        if states[name] == "Очередь":
            table_st.add_row([name, states[name]])
    for name in states.keys():
        if states[name] == "Сдал":
            table_st.add_row([name, states[name]])
    for name in states.keys():
        if states[name] == "Провалил":
            table_st.add_row([name, states[name]])


def print_examiners(app, table_ex):
    for examiner in app.examiners.values():
        if examiner.finished > 0:
            table_ex.add_row([examiner.name, examiner.current, examiner.count,
                             examiner.failed, format(examiner.finished, '.3f')])
        elif examiner.is_on_break == False:
            table_ex.add_row([examiner.name, examiner.current,
                              examiner.count, examiner.failed, format(app.worktime["time"] - examiner.coffeebreak, '.3f')])
        else:
            table_ex.add_row([examiner.name, examiner.current,
                              examiner.count, examiner.failed, format(examiner.breaktime, '.3f')])


def print_examiners_res(app, table_ex_res):
    for examiner in app.examiners.values():
        table_ex_res.add_row([examiner.name, examiner.count,
                              examiner.failed, format(examiner.finished, '.3f')])


def print_exam(app, states, table_st, table_ex):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_students(app, states, table_st)
    print_examiners(app, table_ex)
    print(table_st)
    print(table_ex)
    table_st.clear_rows()
    table_ex.clear_rows()


def print_results(app, states, table_st):
    table_ex_res = PrettyTable()
    table_ex_res.field_names = ["Экзаменатор",
                                "Всего студентов", "Завалил", "Время работы"]
    os.system('cls' if os.name == 'nt' else 'clear')
    print_students(app, states, table_st)
    print_examiners_res(app, table_ex_res)
    print(table_st)
    print(table_ex_res)
    print('Экзамен длился: ' + format(app.worktime["time"], '.3f'))
    print('Лучшие студенты: ' + ", ".join(app.find_best_students()))
    print('Лучшие экзаменаторы: ' + ", ".join(app.find_best_examiners()))
    print('Лучшие вопросы: ' + ", ".join(app.find_best_questions()))
    print('Список на отчисление: ' + ", ".join(app.find_expelled()))
    app.summurize_exam()


def main():
    app = ExamManager()
    queue = mp.Queue()
    states = {}
    for student in app.get_students():
        queue.put(student)
        states[student.name] = student.status
    processes = []
    app.worktime = mp.Manager().dict({"time": 0.0})
    app.results = mp.Manager().list()
    app.examiners = mp.Manager().dict()
    app.question_stats = mp.Manager().dict()
    for task in app.questions:
        app.question_stats[task.data] = task.answered

    for examiner in app.get_examiners():
        app.examiners[examiner.name] = examiner
        exam = mp.Process(target=app.work,
                          args=(examiner, queue))
        processes.append(exam)

    start_time = time.time()
    time_process = mp.Process(target=app.timer)
    processes.append(time_process)

    table_st = PrettyTable()
    table_st.field_names = ["Студент", "Статус"]
    table_ex = PrettyTable()
    table_ex.field_names = ["Экзаменатор", "Текущий студент",
                            "Всего студентов", "Завалил", "Время работы"]

    for pr in processes:
        pr.start()

    print_exam(app, states, table_st, table_ex)

    while "Очередь" in states.values():
        print_exam(app, states, table_st, table_ex)
        print(f'Студентов в очереди: {queue.qsize()}')
        print('Время с начала экзамена: ' +
              format(app.worktime["time"], '.3f'))
        time.sleep(1)

    for pr in processes:
        pr.terminate()
        while pr.is_alive():
            pass
        pr.close()

    print_results(app, states, table_st)


if __name__ == "__main__":
    main()
# end main
