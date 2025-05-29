from domain.login.user_service import UserService

class AuthService(UserService):
    def __init__(self, repository):
        self.repository = repository

    def register(self, request): 
        return self.repository.add_user(request)

    def autorize(self, logdata):
        return self.repository.get_user(logdata)