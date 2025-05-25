# Mapper domain<->web
from .model import GameWeb
from domain.model import Game
from flask import render_template

class MapperWeb:

    @classmethod
    def domain_to_web(cls, domain_model):
        return GameWeb(domain_model.id, domain_model.board.board, domain_model.current_player, domain_model.winner)
    
    @classmethod
    def web_to_domain(cls, web_model):
        return Game(web_model.id, web_model.board, web_model.current_player, web_model.winner)
    
    # @classmethod
    # def update_winner(cls, web_model):
    #     game = MapperWeb.web_to_domain(web_model)
    #     game.winner = web_model.winner
    
    # @classmethod
    # def web_presentation(cls, current_game):
    #     render_template('game.html', gameboard=current_game.board.board, current_player=current_game.current_player, id=current_game.id)