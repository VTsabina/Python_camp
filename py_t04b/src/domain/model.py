# Models of current game and gameboard for domain

import uuid

# Модель игрового поля
class GameBoard:
    def __init__(self, board=None):
        if board == None:
            self.board = [[' ' for _ in range(3)] for _ in range(3)]
        else:
            self.board = board

    def __repr__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])

# Модель текущей игры
class Game:
    def __init__(self, id=str(uuid.uuid4()), board=None, player='X', winner=None):
        self.id = id
        self.board = GameBoard(board)
        self.current_player = player  # Начинает игрок (крестик)
        self.winner = winner

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'