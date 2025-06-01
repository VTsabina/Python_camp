# All the routes for web-interface

from uuid import uuid4
from flask import Flask, request, session, redirect, url_for, render_template, flash
from di.container import container
from .mapper import MapperWeb
from .model import menu

app = Flask(__name__)
app.config['SECRET_KEY'] = '11cd0882545fd8a7fb92f62c75684173c3c303b8'

#TODO: add ai and pvp games, add states (FSM?)

def UserAuthenticator(func):
    def wrapper(*args, **kwargs):
        if session.get('user_id') == None:
            result = render_template('401.html', mainmenu=menu), 401
        else:
            result = func(*args, **kwargs)
        return result
    wrapper.__name__ = func.__name__
    return wrapper

# Main page
@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html', mainmenu=menu)

# Authorization controller
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            res = container.auth.register(MapperWeb.generate_request(request.form['name'], request.form['psw']))
            if res:
                return redirect(url_for('login'))
        except:
            flash("This username is already taken")
    return render_template('register.html', mainmenu=menu)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id') != None:
        return redirect(url_for('show_profile', user_id=session['user_id']))
    if request.method == 'POST':
        res = container.auth.autorize(MapperWeb.to_base64(request.form['name'], request.form['psw']))
        if res:
            session['user_id'] = res
            return redirect(url_for('show_profile', user_id=res))
        else:
            flash("Incorrect login or password")
    return render_template('login.html', mainmenu=menu)

@app.route('/logout', methods=['GET', 'POST'])
@UserAuthenticator
def logout():
    session['user_id'] = None
    return redirect(url_for('main_page'))

# Main-UI controller
@app.route('/profile/<user_id>', methods=['GET', 'POST'])
@UserAuthenticator
def show_profile(user_id):
    u = container.repository.get_user_info(user_id)
    return render_template('profile.html', mainmenu=menu, user=u)

@app.route('/play', methods=['GET', 'POST'])
@UserAuthenticator
def play_game():
    return render_template('play.html', mainmenu=menu)

@app.route('/join', methods=['GET', 'POST'])
@UserAuthenticator
def join_game():
    return render_template('available_games.html', mainmenu=menu)

@app.route('/create_game', methods=['GET', 'POST'])
@UserAuthenticator
def choose_mode():
    return render_template('create_game.html', mainmenu=menu)

@app.route('/create_pvp', methods=['GET', 'POST'])
@UserAuthenticator
def create_pvp():
    return render_template('create_pvp.html', mainmenu=menu)

@app.route('/play_x', methods=['GET', 'POST'])
@UserAuthenticator
def play_X():
    id = uuid4()
    return redirect(url_for('play_pvp', game_id=id))

@app.route('/play_o', methods=['GET', 'POST'])
@UserAuthenticator
def play_O():
    id = uuid4()
    return redirect(url_for('play_pvp', game_id=id))

@app.route('/pvp/<game_id>', methods=['GET', 'POST'])
@UserAuthenticator
def play_pvp(game_id):
    if game_id not in container.repository.get_keys():
        container.service.create_game(game_id)

    current_game = MapperWeb.domain_to_web(container.repository.get(game_id))

    return render_template('pvp_game.html', mainmenu=menu)


@app.route('/game')
@UserAuthenticator
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
        if data != None:
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
@UserAuthenticator
def show_history():
    return render_template('history.html', mainmenu=menu)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', mainmenu=menu), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', mainmenu=menu), 500