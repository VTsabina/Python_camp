class AuthService:
    def __init__(self):
        pass

    def register(self, request): # метод регистрации, который принимает SignUpRequest и возвращает факт успешной регистрации
        pass

    def autorize(self, logdata): # метод авторизации, который принимает в заголовке логин и пароль и возвращает UUID пользователя.
        # logdata - логин и пароль в виде base64(login:password)
        pass