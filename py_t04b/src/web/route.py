# All the routes for web-interface

from uuid import uuid4
from flask import Flask, request, redirect, url_for, render_template
from di.container import container
from .mapper import MapperWeb
from .model import menu
# from .model import app
# from flask import Flask, render_template

app = Flask(__name__)


#TODO: add ai and pvp games, add states (FSM?), sign info (?)

@app.route('/', methods=['GET'])
def main_paige():
    return render_template('index.html', mainmenu=menu)

@app.route('/register', methods=['GET', 'POST'])
def registration():
    pass

@app.route('/login', methods=['GET', 'POST'])
def autorization():
    pass

@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def show_profile(user_id):
    pass

@app.route('/create_game', methods=['GET', 'POST'])
def choose_mode():
    pass

@app.route('/join', methods=['GET', 'POST'])
def join_game():
    pass

@app.route('/game')
def get_uuid():
    id = uuid4()
    return redirect(url_for('play_game_computer', game_id=id))

@app.route('/game/<game_id>', methods=['POST'])
def play_game_player(game_id):
    if game_id not in container.repository.get_keys():
        container.service.create_game(game_id)

    current_game = MapperWeb.domain_to_web(container.repository.get(game_id))

    if request.method == 'POST' and not container.service.check_game_over(MapperWeb.web_to_domain(current_game)):
        data = request.json
        move_x, move_y = data['move']

        if current_game.board[move_x][move_y] != ' ':
            return {'error': 'Cell already taken'}, 400
        else:
            current_game.board[move_x][move_y] = current_game.current_player

        winner = container.service.check_game_over(MapperWeb.web_to_domain(current_game))
        if winner == 'X':
            current_game.winner = 'You'
        elif winner == 'draw':
            current_game.winner = 'Draw'
        
        current_game.switch_player()

        container.repository.save(MapperWeb.web_to_domain(current_game))

        return current_game.update_game(), 200
        
    return current_game.web_presentation()

@app.route('/game/<game_id>', methods=['GET'])
def play_game_computer(game_id):

    if game_id not in container.repository.get_keys():
        container.service.create_game(game_id)

    current_game = MapperWeb.domain_to_web(container.repository.get(game_id))

    if request.method == 'GET':
       if current_game.current_player == 'O':            

            next_move_x, next_move_y = container.service.get_best_move(MapperWeb.web_to_domain(current_game))
            current_game.board[next_move_x][next_move_y] = current_game.current_player

            winner = container.service.check_game_over(MapperWeb.web_to_domain(current_game))
            if winner == 'O':
                current_game.winner = 'Computer'
            elif winner == 'draw':
                current_game.winner = 'Draw'

            if not winner and not container.service.validate_board(MapperWeb.web_to_domain(current_game)):
                return render_template('500.html', mainmenu=menu, error='Sorry, looks like computer can not play right now!') 
            
            current_game.switch_player()

            container.repository.save(MapperWeb.web_to_domain(current_game))


    return current_game.web_presentation(), 200

@app.route('/history', methods=['GET'])
def show_history():
    return render_template('history.html', mainmenu=menu)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', mainmenu=menu), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', mainmenu=menu), 500