# Опиши интерфейс сервиса, у которого есть следующие методы:
    # метод получения следующего хода текущей игры алгоритмом Минимакс;
    # метод валидации игрового поля текущей игры (проверь, что не изменены предыдущие ходы);
    # метод проверки окончания игры.
# Модели, интерфейсы, реализации должны находиться в разных файлах.

# domain/game_service.py
import uuid
import time
from domain.model import Game
from domain.service import IService

class GameService(IService):
    def __init__(self, repository):
        self.repository = repository

    def create_game(self, game_id=str(uuid.uuid4())):
        game = Game(id=game_id)
        self.repository.save(game)
        return game
    
    def get_gameboard(self, game_id):
        game = self.repository.get(game_id)
        return game.board.board
        
    # Алгоритм Минимакс
    def minimax(self, board, depth, is_maximizing):
        scores = {'X': -1, 'O': 1, 'draw': 0}
        winner = self.check_winner(board)

        if winner in scores:
            return scores[winner]

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def get_best_move(self, game):
        best_score = float('-inf')
        move = (-1, -1)
        
        for i in range(3):
            for j in range(3):
                if game.board.board[i][j] == ' ':
                    game.board.board[i][j] = 'O'
                    score = self.minimax(game.board.board, 0, False)
                    game.board.board[i][j] = ' '
                    
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        time.sleep(1)
        
        return move

    def check_winner(self, board):
        # Проверка строк и столбцов
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != ' ':
                return board[0][i]
        
        # Проверка диагоналей
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]

        # Проверка на ничью
        if all(cell != ' ' for row in board for cell in row):
            return 'draw'

        return None

    def validate_board(self, current_game: Game):
        current_count_x = sum(cell == 'X' for row in current_game.board.board for cell in row)
        current_count_o = sum(cell == 'O' for row in current_game.board.board for cell in row)

        return current_count_x >= current_count_o and current_count_x <= current_count_o + 1

    def check_game_over(self, current_game: Game):
        winner = self.check_winner(current_game.board.board)
        current_game.winner = winner
        return winner
