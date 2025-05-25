# Repository for current games
from .mapper import MapperDatasource
from collections import defaultdict
from threading import Lock
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON

db = SQLAlchemy()

class GameModel(db.Model):
    __tablename__ = 'games'
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    board: Mapped[dict] = mapped_column(JSON)
    current_player: Mapped[str] = mapped_column(String)

class Users(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    psw: Mapped[str] = mapped_column(String)

class Repository:
    def __init__(self):
        self.lock = Lock()

    def save(self, domain_model):
        game = MapperDatasource.domain_to_datasource(domain_model)
        with self.lock:
            existing_game = GameModel.query.get(game.data['id'])
            if existing_game:
                existing_game.board = game.data['board']
                existing_game.current_player = game.data['current_player']
            else:
                new_game = GameModel(
                    id=game.data['id'],
                    board=game.data['board'],
                    current_player=game.data['current_player']
                )
                db.session.add(new_game)
            db.session.commit()

    def get(self, uuid):
        with self.lock:
            game_record = GameModel.query.get(uuid)
            if not game_record:
                return None
            return MapperDatasource.datasource_to_domain(game_record)

    def get_keys(self):
        with self.lock:
            return [game.id for game in GameModel.query.all()]
        