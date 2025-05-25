# Mapper domain<->datasource
from domain.model import Game
from .model import GameDatasource

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