# Models of current game and gameboard for datasource

class GameDatasource:
    def __init__(self, game_dict):
        self.data = game_dict

class User:
    def __init__(self, id, login, psw):
        self.id = id
        self.login = login
        self.psw = psw