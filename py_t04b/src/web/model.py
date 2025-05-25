# Models of current game and gameboard for web
from flask import render_template

menu = [{'name': 'About', 'url': '/'},
        {'name': 'Play', 'url': '/game'},
        {'name': 'History', 'url': '/history'}]

class GameWeb:
    def __init__(self, id, board, player, winner):
        self.id = id
        self.board = board
        self.current_player = player
        self.winner = winner

    def web_presentation(self):
        return render_template('game.html', title='Game', mainmenu=menu, gameboard=self.board, current_player=self.current_player, id=self.id, winner=self.winner)

    def update_game(self):
        return {
            'id': self.id,
            'board': self.board,
            'current_player': self.current_player,
            'winner': self.winner,
        }
    
    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'


class UserAuthenticator:

    def validate():
        pass