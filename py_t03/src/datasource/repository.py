# Repository for current games
from .mapper import MapperDatasource
from collections import defaultdict
from threading import Lock

class Repository:
    def __init__(self):
        self.games = defaultdict()
        self.lock = Lock()

    def save(self, domain_model):
        game = MapperDatasource.domain_to_datasource(domain_model)
        with self.lock:
            self.games[game.data['id']] = game

    def get(self, uuid):
        with self.lock:
            game = self.games.get(uuid)
            return MapperDatasource.datasource_to_domain(game)
    
    def get_keys(self):
        return self.games.keys()