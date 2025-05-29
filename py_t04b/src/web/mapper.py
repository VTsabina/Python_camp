# Mapper domain<->web
from .model import GameWeb
from domain.model import Game
from domain.login.model import SignUpRequest
from werkzeug.security import generate_password_hash
import base64


class MapperWeb:

    @classmethod
    def domain_to_web(cls, domain_model):
        return GameWeb(domain_model.id, domain_model.board.board, domain_model.current_player, domain_model.winner)
    
    @classmethod
    def web_to_domain(cls, web_model):
        return Game(web_model.id, web_model.board, web_model.current_player, web_model.winner)
    
    @classmethod
    def generate_request(cls, login, psw):
        psw_hash = generate_password_hash(psw)
        return SignUpRequest(login, psw_hash)
    
    @classmethod
    def to_base64(cls, login, psw):
        str = f'{login}:{psw}'
        bytes = str.encode('utf-8')
        coded = base64.b64encode(bytes)
        return coded.decode('utf-8')

    
    # @classmethod
    # def update_winner(cls, web_model):
    #     game = MapperWeb.web_to_domain(web_model)
    #     game.winner = web_model.winner
    
    # @classmethod
    # def web_presentation(cls, current_game):
    #     render_template('game.html', gameboard=current_game.board.board, current_player=current_game.current_player, id=current_game.id)