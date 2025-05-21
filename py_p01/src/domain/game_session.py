import random
from time import gmtime, strftime
from .entities.player import Player
from .map_generation.map import Map

class GameSession:
    def __init__(self, levels=21):
        self.player = Player()
        self.levels = levels
        self.current_level = 1
        self.game_map = None
        self.exit_requested = False  # Флаг для выхода из игры
        # Список попыток (каждая попытка – словарь со статистикой прохождения)
        self.attempts = []

    def get_state(self):
        """Полный снимок незавершённой сессии для save_in_progress()."""
        return {
            "current_level": self.current_level,
            "rng_state":     random.getstate(),
            "player":        self.player.to_dict(),
            "map":           self.game_map.to_dict(),
        }

    def restore_from_state(self, st):
        """Восстановление из load_in_progress()."""
        self.current_level = st["current_level"]
        random.setstate(tuple(st["rng_state"]))
        self.player   = Player.from_dict(st["player"])
        self.game_map = Map.from_dict(st["map"])


    def init_saved_state(self, saved_state):
        self.player.current_health = saved_state["player"]["cur_hp"]
        self.player.treasure_value = saved_state["player"]["treasure"]
        self.player.max_health = saved_state["player"]["max_hp"]
        self.player.skill = saved_state["player"]["skill"]
        self.player.strength = saved_state["player"]["strength"]
        self.player.move_count = saved_state["player"].get("move_count", 0)
        self.player.enemies_killed = saved_state["player"].get("enemies_killed", 0)
        self.player.food_eaten = saved_state["player"].get("food_eaten", 0)
        self.player.potions_drunk = saved_state["player"].get("potions_drunk", 0)
        self.player.scrolls_read = saved_state["player"].get("scrolls_read", 0)
        self.player.hits_delivered = saved_state["player"].get("hits_delivered", 0)
        self.player.hits_received = saved_state["player"].get("hits_received", 0)
        self.player.position = tuple(saved_state["player"].get("pos", (0, 0)))
        self.current_level = saved_state.get("current_level", 1)

    def generate_level(self, max_y, max_x):
        self.game_map = Map(max_y, max_x)
        self.game_map.create_all_map(self.player)
        # Устанавливаем стартовую позицию в центре первой комнаты
        start_room = self.game_map.rooms[0]
        self.player.set_position(*start_room.center())

    
    def check_items_around(self):
        for item in self.game_map.items:
            if item[1][0] == self.player.get_position()[1] and item[1][1] == self.player.get_position()[0]:
                self.game_map.status_info.insert(0, f"You found {item[0].subtype}! {item[0].description}")
                loot = item[0]
                self.game_map.items.remove(item)
                if loot.item_type == 'treasure':
                    loot.apply_effect(self.player)
                elif loot.item_type == 'weapon':
                    self.player.equip_weapon(loot, self.game_map)
                    self.player.inventory.add_item(loot)
                elif loot.item_type == 'key':
                    self.player.inventory.add_item(loot)
                    # self.game_map.status_info.insert(0, f"You found a key {loot.color_id}")

                else:
                    self.player.inventory.add_item(loot)
    

    def init_level(self):
        self.game_map.current_level = self.current_level
        self.game_map.generate_enemies(self.player)
    
    def game_step(self, new_x, new_y):
        self.player.recount_buffs()
        self.player.move(new_x, new_y, self.game_map)
        self.check_items_around()            

    def record_attempt(self, success: bool):
        stats = {
            "success": success,
            "date": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "level": self.current_level,
            "treasure": self.player.treasure_value,
            "move_count": self.player.move_count,
            "enemies_killed": self.player.enemies_killed,
            "food_eaten": self.player.food_eaten,
            "potions_drunk": self.player.potions_drunk,
            "scrolls_read": self.player.scrolls_read,
            "hits_delivered": self.player.hits_delivered,
            "hits_received": self.player.hits_received,
        }
        self.attempts.append(stats)
