# Mapper domain<->datasource
import base64
from uuid import uuid4
from domain.model import Game
from .model import GameDatasource, User

class MapperDatasource:

    @classmethod
    def domain_to_datasource(cls, domain_model):
        game_dict = {
            'id': domain_model.id,
            'board': domain_model.board.board,
            'current_player': domain_model.current_player,
        }
        return GameDatasource(game_dict)

    @classmethod
    def datasource_to_domain(cls, datasource_model):
        data = datasource_model
        return Game(id=data.id, board=data.board, player=data.current_player)
    
    @classmethod
    def request_to_user(cls, request):
        id = uuid4()
        login = request.login
        psw = request.psw
        return User(id, login, psw)
    
    @classmethod
    def decode_base64(cls, logdata):
        bytes = base64.b64decode(logdata)
        return bytes.decode('utf-8')