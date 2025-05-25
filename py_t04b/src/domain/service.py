from abc import ABC, abstractmethod

class IService(ABC):

    @abstractmethod
    def minimax():
        'метод получения следующего хода текущей игры алгоритмом Минимакс'

    @abstractmethod
    def validate_board():
        'метод валидации игрового поля текущей игры'

    @abstractmethod
    def check_game_over():
        'метод проверки окончания игры'