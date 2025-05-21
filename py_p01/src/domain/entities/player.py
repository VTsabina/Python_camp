import random
from .inventory import Inventory
from domain.map_generation.map import Map
from config.constants import (FLOOR_SYMBOL, CORRIDOR_SYMBOL, PLAYER, EXITO, ITEMS, DOOR_CLOSED, DOOR_OPEN)

class Player:
    face = PLAYER

    def __init__(self, max_health=100, skill=100, strength=50):
        self.max_health = max_health
        self.current_health = max_health
        self.skill = skill
        self.strength = strength
        self.inventory = Inventory()
        self.position = (0, 0)
        self.treasure_value = 0
        self.equipped_weapon = None
        self.is_alive = True
        self.damage = self.strength 
        self.current_bufs = [] # list of lists [[max_health_buff = 0, skill_buff = 0, strength_buff = 0,, moves_left]...]
        self.skip_next_turn = False

          # Статистика прохождения:
        self.move_count = 0            # пройденных клеток
        self.enemies_killed = 0        # убитых врагов
        self.food_eaten = 0            # съедено единиц еды
        self.potions_drunk = 0         # выпито эликсиров
        self.scrolls_read = 0          # прочитано свитков
        self.hits_delivered = 0        # нанесено ударов
        self.hits_received = 0         # пропущено ударов

    def get_position(self):
        return self.position

    def set_position(self, x, y):
        if (x, y) != self.position:
            self.move_count += 1
        self.position = (x, y)

    def set_skip_next_turn(self, value):
        self.skip_next_turn = value

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.current_health = 0
            self.die()

    def die(self):
        self.is_alive = False

    # def has_key(self, color_id):
    #     return any(isinstance(it, Key) and it.color_id==color_id
    #             for it in self.inventory.items['key'])

    def has_key(self, color_id: int):
        return any(getattr(it, "color_id", -1) == color_id
                for it in self.inventory.items["key"])




    def move(self, new_x, new_y, game_map):
        if not (0 <= new_x < game_map.max_x and 0 <= new_y < game_map.max_y):
            return
        cell = game_map.game_map[new_y][new_x]

        # закрытая дверь?
        if cell in DOOR_CLOSED.values():
            cid = [c for c,sym in DOOR_CLOSED.items() if sym==cell][0]
            if self.has_key(cid):                         # ключ есть
                game_map.game_map[new_y][new_x] = DOOR_OPEN[cid]
                game_map.status_info.insert(0, f"Door {cid} opened!")
                for it in list(self.inventory.items["key"]):
                    if it.color_id == cid:
                        self.inventory.remove_item(it)
                        break
            else:                                         # нет ключа – стоп
                game_map.status_info.insert(0, "Need a key!")
                return

        if cell in (FLOOR_SYMBOL, CORRIDOR_SYMBOL, EXITO, *DOOR_OPEN.values()):
            self.set_position(new_x, new_y)





    def heal(self, amount):
        self.current_health = min(self.current_health + amount, self.max_health)

    def add_treasure(self, value):
        self.treasure_value += value
        self.inventory.items['treasure'] += 1

    def equip_weapon(self, weapon, map):
        if self.equipped_weapon:
            self.drop_weapon(map)
        self.equipped_weapon = weapon
        self.damage = self.strength + self.equipped_weapon.strength_boost

    def check_cells(self, cells, map):
        drop_coor = (0, 0)
        for cell in cells:
            if cell[0] < map.max_y and cell[1] < map.max_x:
                is_taken = False
                if map.game_map[cell[0]][cell[1]] == FLOOR_SYMBOL:
                    for item in map.items:
                        if cell == item[1]:
                            is_taken = True
                else:
                    is_taken = True
                if not is_taken:
                    place_found = True
                    drop_coor = cell
                    break

        return place_found, drop_coor

    def drop_weapon(self, map):
        if self.equipped_weapon:
            weapon = self.equipped_weapon
            pos_y = self.position[1]
            pos_x = self.position[0]
            drop_coor = (0, 0)
            place_found = False
            prior_cells = ((pos_y - 1, pos_x - 1), (pos_y - 1, pos_x + 1), (pos_y + 1, pos_x - 1), (pos_y + 1, pos_x + 1))
            spare_cells = ((pos_y, pos_x - 1), (pos_y, pos_x + 1), (pos_y + 1, pos_x), (pos_y - 1, pos_x))

            place_found, drop_coor = self.check_cells(prior_cells, map)
            if not place_found:
                place_found, drop_coor = self.check_cells(spare_cells, map)
            self.inventory.remove_item(weapon)               
            map.items.append((weapon, drop_coor))
            self.equipped_weapon = None

    def attack(self, enemy, game_map):
        hit_chance = (self.skill / (self.skill + enemy.skill)) * 100
        if random.randint(1, 100) <= hit_chance:
            damage = self.strength
            if self.equipped_weapon:
                damage += self.equipped_weapon.strength_boost
            enemy.take_damage(damage)
            game_map.status_info.insert(0, f"Yay, you attacked {enemy.enemy_type} for {damage} XP!")
            self.hits_delivered += 1
        else:
            game_map.status_info.insert(0, f"Oh no, your attack fails!")
    
    def recount_buffs(self):
        for item in self.current_bufs: 
            if item[3] <= 0:
                self.strength -= item[2]
                self.skill -= item[1]
                self.max_health -= item[0]
                self.current_health -= item[0]
                self.current_bufs.remove(item)
                if self.current_health <= 0:
                    self.current_health = 5
            item[3] -= 1
                
    def to_dict(self) -> dict:
        inv_dict = {}
        for t, cat in self.inventory.items.items():
            if t == "treasure":                 # это счётчик, а не список
                inv_dict[t] = cat               # просто число
            else:
                inv_dict[t] = [it.subtype for it in cat]    # берём всё, что нужно
                                
        return {
            "pos":       list(self.position),
            "max_hp":    self.max_health,
            "cur_hp":    self.current_health,
            "skill":     self.skill,
            "strength":  self.strength,
            "treasure":  self.treasure_value,
            "inventory": inv_dict,
            "current_buffs": self.current_bufs
        }


    @classmethod
    def from_dict(cls, data: dict):
        p = cls(max_health=data["max_hp"],
                skill=data["skill"],
                strength=data["strength"])
        p.set_position(*data["pos"])
        p.current_health = data["cur_hp"]
        p.treasure_value = data["treasure"]
        p.current_bufs = data["current_buffs"]
        p.inventory = Inventory()

        for type in data["inventory"].keys():
            if type != "treasure":
                for subtype in data["inventory"][type]:
                    for item in ITEMS[type.lower()+'s']:
                        if item['name'] == subtype:
                            factory = Map.convert_item(type, item)
                            p.inventory.items[type].append(factory)

        # # перевооружаемся, если в руках было оружие
        if p.inventory.items["weapon"]:
            p.equipped_weapon = p.inventory.items["weapon"][0]
            p.damage = p.strength + p.equipped_weapon.strength_boost
        return p
