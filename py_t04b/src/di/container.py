# Реализуй класс Container, в котором описывается граф зависимостей.
# Он должен содержать как минимум:
    # класс-хранилище в качестве singleton;
    # репозиторий для работы с классом-хранилищем;
    # сервис для работы с репозиторием.

# di/container.py

from datasource.repository import Repository
from datasource.service import GameService
from datasource.auth_service import AuthService

class Container:
    def __init__(self):
        self.repository = Repository()
        self.service = GameService(self.repository)
        self.auth = AuthService(self.repository)

container = Container() # module as singleton