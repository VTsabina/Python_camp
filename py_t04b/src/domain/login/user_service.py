from abc import ABC, abstractmethod

class UserService(ABC):
    
    @abstractmethod
    def register(): 
        'метод регистрации, который принимает SignUpRequest и возвращает факт успешной регистрации'

    @abstractmethod
    def autorize(): 
        'метод авторизации, который принимает в заголовке логин и пароль и возвращает UUID пользователя'
        'logdata - логин и пароль в виде base64(login:password)'