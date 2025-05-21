import random
from collections import deque
from domain.entities.items import Food, Potion, Scroll, Weapon, Treasure
from domain.entities.enemies import Ghost, Zombie, Vampire, Snake_mage, Mimic, Ogre
from .room import Room
from .key import Key

from config.constants import (
    WALL_SYMBOL, FLOOR_SYMBOL, CORRIDOR_SYMBOL, EXITO, ITEMS, DOOR_CLOSED, DOOR_OPEN, VERTICAL_WALL, HORIZONTAL_WALL,
                            TOP_LEFT_CORNER, TOP_RIGHT_CORNER,
                            LOW_LEFT_CORNER, LOW_RIGHT_CORNER, DOOR_KEY_COLORS
)

# DOOR_KEY_COLORS = ["red", "blue", "green"]

class Map:
    def __init__(self, max_y, max_x):
        self.max_y = max_y
        self.max_x = max_x
        self.game_map = [[WALL_SYMBOL for _ in range(max_x)] for _ in range(max_y)]
        self.rooms = []
        self.items = []  # list of lists (item, (y, x))
        self.enemies = [] # [[enemy, room]]
        self.exit = None  # координаты выхода
        self.is_statistic_open = False
        self.current_level = 1
        self.status_info = []

        self.doors = []   # [(y,x,color_id,is_open)]

        self.visible = [[False for _ in range(max_x)] for _ in range(max_y)]
        self.explored = [[False for _ in range(max_x)] for _ in range(max_y)]

    @staticmethod
    def bresenham_line(x0, y0, x1, y1):
        """Генерирует точки на линии между (x0,y0) и (x1,y1) с использованием алгоритма Брезенхэма"""
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1

        if dx > dy:
            err = dx / 2.0
            while x != x1:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

        points.append((x, y))
        return points

    def update_fov(self, x, y, radius):
        """Обновляет поле видимости с центром в (x,y) и заданным радиусом"""
        # Сначала помечаем все клетки как невидимые
        for j in range(self.max_y):
            for i in range(self.max_x):
                self.visible[j][i] = False
                # self.visible[j][i] = True # MOD: FOG REMOVED

        # Помечаем текущую позицию как видимую и исследованную
        self.visible[y][x] = True
        self.explored[y][x] = True

        # Проверяем все клетки в круге
        for j in range(max(0, y - radius), min(self.max_y, y + radius + 1)):
            for i in range(max(0, x - radius), min(self.max_x, x + radius + 1)):
                # Проверяем, находится ли клетка в пределах радиуса
                if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                    # Получаем линию от центра до текущей клетки
                    line = self.bresenham_line(x, y, i, j)
                    for (cx, cy) in line:
                        # Помечаем клетку как видимую и исследованную
                        self.visible[cy][cx] = True
                        self.explored[cy][cx] = True
                        # Если клетка непроходима, прерываем луч
                        if not self.is_passable(cx, cy) and (cx, cy) != (i, j):
                            break


    def is_passable(self, x, y):
        if 0 <= x < self.max_x and 0 <= y < self.max_y:
            cell = self.game_map[y][x]
            if cell in DOOR_CLOSED.values():
                return False

            return cell in (FLOOR_SYMBOL, CORRIDOR_SYMBOL,
                            EXITO, *DOOR_OPEN.values())
        return False



    def find_path(self, start, end):
        queue = deque([[start]])
        seen = {start}
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if (x, y) == end:
                return path
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if self.is_passable(nx, ny) and (nx, ny) not in seen:
                    queue.append(path + [(nx, ny)])
                    seen.add((nx, ny))
        return None

    def has_path(self, start, end):
        return self.find_path(start, end) is not None
    
    def get_item_types(self):
        item_types = {
            'foods': [],
            'potions': [],
            'scrolls': [],
            'weapons': [],
            'treasures': [],
        }

        for item in ITEMS['foods']:
            item_types['foods'].append(Food(name=item['name'], health_boost=item['health_boost'], description=item['description']))
        for item in ITEMS['potions']:
            item_types['potions'].append(Potion(name=item['name'], time_limit=item['time_limit'], max_health_boost=item['max_health_boost'],
                                                skill_boost=item['skill_boost'], strength_boost=item['strength_boost'], description=item['description']))
        for item in ITEMS['scrolls']:
            item_types['scrolls'].append(Scroll(name=item['name'], max_health_boost=item['max_health_boost'],
                                                skill_boost=item['skill_boost'], strength_boost=item['strength_boost'], description=item['description']))
        for item in ITEMS['weapons']:
            item_types['weapons'].append(Weapon(name=item['name'], strength_boost=item['strength_boost'], description=item['description']))
        for item in ITEMS['treasures']:
            item_types['treasures'].append(Treasure(name=item['name'], value=item['value'], description=item['description']))

        return item_types
    

    def correct_level_indx(self, indx, player):
        try:
            if 100 + (4 * self.current_level) / player.damage > 2.5:
                indx['scroll_indx'] += 2
                indx['potion_indx'] += 2
        except:
            pass
        
        try:
            if player.hits_recieved / player.enemies_killed > 5:
                indx['scroll_indx'] += 2
                indx['potion_indx'] += 2
        except:
            pass

        if player.current_health < 30:
            indx['food_indx'] += 2

        return indx


    def get_level_indx(self, player):
        indx = {
            'treasure_indx': 0,
            'scroll_indx': 0,
            'food_indx': 0,
            'potion_indx': 0,
        }
        if self.current_level < 5:
            indx['treasure_indx'] = 1
            indx['scroll_indx'] = 3
            indx['food_indx'] = 3
            indx['potion_indx'] = 3
        elif self.current_level < 10:
            indx['treasure_indx'] = 2
            indx['scroll_indx'] = 2
            indx['food_indx'] = 2
            indx['potion_indx'] = 2
        elif self.current_level < 15:
            indx['treasure_indx'] = 5
            indx['scroll_indx'] = 1
            indx['food_indx'] = 1
            indx['potion_indx'] = 1
        elif self.current_level < 19:
            indx['treasure_indx'] = 6
            indx['scroll_indx'] = random.randint(0, 1)
            indx['food_indx'] = random.randint(0, 1)
            indx['potion_indx'] = random.randint(0, 1)
        else:
            indx['treasure_indx'] = 8
        
        indx = self.correct_level_indx(indx, player)
        return indx
    

    def generate_items(self, player):
        item_types = self.get_item_types() # it's a dict now, that's more convenient
        indx = self.get_level_indx(player)
        num_of_treasures = random.randint(1, 3) * indx['treasure_indx']
        num_of_scrolls = 1 * indx['scroll_indx']
        num_of_food = 3 * indx['food_indx']
        num_of_weapon = 1
        num_of_potion = random.randint(1, 3) * indx['potion_indx']
        for room in self.rooms:
            num_items = random.randint(1, 2) 
            for _ in range(num_items):
                available_items = []
                if num_of_treasures > 0:
                    idx = random.randint(0, 6)
                    available_items.append(item_types['treasures'][idx])
                if num_of_scrolls > 0:
                    idx = random.randint(0, 8)
                    available_items.append(item_types['scrolls'][idx])
                if num_of_food > 0:
                    idx = random.randint(0, 4)
                    available_items.append(item_types['foods'][idx])
                if num_of_weapon > 0:
                    idx = random.randint(0, 8)
                    available_items.append(item_types['weapons'][idx])
                if num_of_potion > 0:
                    idx = random.randint(0, 9)
                    available_items.append(item_types['potions'][idx])
                if not available_items:
                    break
                item = random.choice(available_items)
                if item.item_type == 'treasure':
                    num_of_treasures -= 1
                elif item.item_type == 'scroll':
                    num_of_scrolls -= 1
                elif item.item_type == 'food':
                    num_of_food -= 1
                elif item.item_type == 'weapon':
                    num_of_weapon -= 1
                elif item.item_type == 'potion':
                    num_of_potion -= 1

                item_y = random.randint(room.y + 1, room.y + room.height - 3)
                item_x = random.randint(room.x + 1, room.x + room.width - 3)
                while self.game_map[item_y][item_x] != FLOOR_SYMBOL:
                    item_y = random.randint(room.y + 1, room.y + room.height - 3)
                    item_x = random.randint(room.x + 1, room.x + room.width - 3)

                self.items.append((item, (item_y, item_x)))

    def get_enemy_indx(self, player):
        enemy_indx = 0
        try:
            if player.hits_recieved / player.enemies_killed > 5:
                enemy_indx += player.hits_recieved / player.enemies_killed * 5
        except:
            pass
        return enemy_indx

    def generate_enemies(self, player):
        indx = self.get_enemy_indx(player)
        rooms_number = [i for i in range(1, len(self.rooms))]
        random.shuffle(rooms_number)
        enemies_number = min(self.current_level, len(self.rooms) - 1)
        rooms_with_enemies = rooms_number[:enemies_number]
        enemy_types = ['g', 'z', 'v', 'm', 's', 'o']
        for room_number in rooms_with_enemies:
            room = self.rooms[room_number]
            available_enemies = min(self.current_level, len(enemy_types) - 1)
            enemy_type = enemy_types[random.randint(0, available_enemies)]
            if enemy_type == 'g':
                enemy = Ghost(self.current_level, room, indx)
            elif enemy_type == 'z':
                enemy = Zombie(self.current_level, room, indx)
            elif enemy_type == 'v':
                enemy = Vampire(self.current_level, room, indx)
            elif enemy_type == 'm':
                enemy = Mimic(self.current_level, room, indx)
            elif enemy_type == 's':
                enemy = Snake_mage(self.current_level, room, indx)
            elif enemy_type == 'o':
                enemy = Ogre(self.current_level, room, indx)
            self.enemies.append(enemy)
            enemy.set_position(room.x + room.width // 2, room.y + room.height // 2, self)

    def generate_rooms(self):

        reserved_area_width = 5  # ширина области для статистики
        reserved_area_height = 5  # высота области для статистики
        reserved_area_x = self.max_x - reserved_area_width  # левая граница области
        reserved_area_y = self.max_y - reserved_area_height  # верхняя граница области

        for _ in range(100):
            room_width = random.randint(10, 30)
            room_height = random.randint(5, 20)
            x = random.randint(1, reserved_area_x - room_width - 1)  # ограничение по ширине
            y = random.randint(1, reserved_area_y - room_height - 1)  # ограничение по высоте

            new_room = Room(x, y, room_width, room_height)
            if any(new_room.intersect(other) for other in self.rooms):
                continue
            if new_room.x >= reserved_area_x or new_room.y >= reserved_area_y:  # проверка пересечения с зоной статистики
                continue
            self.rooms.append(new_room)
            if len(self.rooms) == 9:
                break
        


    # def create_all_map(self):
    #     self.generate_rooms()
    #     for room in self.rooms:
    #         room.draw(self.game_map)

    #     # соединяем коридорами, фиксируем углы
    #     Room.connect_rooms(self.rooms, self.game_map)
    #     Room.fix_corners(self.game_map)

    #     # предметы, враги
    #     self.generate_items()
    #     self.generate_enemies()

    #     # выход
    #     self._place_exit()

    #     self.doors = []          # храним список дверей
    #     self._place_doors_and_keys()

    def create_all_map(self, player):
        self.generate_rooms()
        for room in self.rooms:
            room.draw(self.game_map)
        self.items = [] 
        self.generate_items(player)
        Room.connect_rooms(self.rooms, self.game_map)

        # # 1) ставим двери в случайные проходы
        # self._place_doors()

        # # 2) кладём ключи
        # self._place_keys()


         # 1) ставим двери и ключи до тех пор,
        #    пока validate_level не подтвердит проходимость



        # tries = 0
        # while True:
        #     tries = 1
        #     self._place_doors()
        #     self._place_keys()
        #     start_pos = self.rooms[0].center()
        #     if self.validate_level(start_pos) or tries > 20:   # «непруха» – сдаёмся
        #         break
        #     # soft-lock обнаружен откатываем и пробуем снова
        #     for y,x,_,_ in self.doors:
        #         self.game_map[y][x] = CORRIDOR_SYMBOL
        #     self.doors.clear()
        #     self.items = [it for it in self.items if it[0].item_type != "key"]
        while True:
            self._place_doors()
            self._place_keys()
            if self.validate_level(self.rooms[0].center()):
                break
            # soft-lock → откатываем и пробуем заново
            for y,x,_,_ in self.doors:
                self.game_map[y][x] = CORRIDOR_SYMBOL
            self.doors.clear()
            self.items = [it for it in self.items if it[0].item_type != "key"]

        Room.fix_corners(self.game_map)
        # не в старт комнате
        if len(self.rooms) > 1:
            exit_room = random.choice(self.rooms[1:])  # исключаем первую комнату
            ex, ey = exit_room.center()
            self.exit = (ex, ey)
            self.game_map[ey][ex] = EXITO

    def to_dict(self):
        return {
            "max_x": self.max_x,
            "max_y": self.max_y,
            "game_map": self.game_map,
            "enemies": [[enemy.enemy_type, [enemy.room.x, enemy.room.y, enemy.room.width, enemy.room.height], list(enemy.position)] for enemy in self.enemies], 
            "items": [
                (it[0].item_type, it[0].subtype,
                list(it[1]))
                for it in self.items
            ],
            "exit":    list(self.exit) if self.exit else None,
            "level":   self.current_level
        }

    @classmethod
    def convert_item(sld, type, item):
        res = None
        if type == 'food':
            res = Food(name=item['name'], health_boost=item['health_boost'], description=item['description'])
        if type == 'potion':
            res = Potion(name=item['name'], time_limit=item['time_limit'], max_health_boost=item['max_health_boost'],
                                                skill_boost=item['skill_boost'], strength_boost=item['strength_boost'], description=item['description'])
        if type == 'scroll':
            res = Scroll(name=item['name'], max_health_boost=item['max_health_boost'],
                                                skill_boost=item['skill_boost'], strength_boost=item['strength_boost'], description=item['description'])
        if type == 'weapon':
            res = Weapon(name=item['name'], strength_boost=item['strength_boost'], description=item['description'])
        if type == 'treasure':
            res = Treasure(name=item['name'], value=item['value'], description=item['description'])
        if type == 'key':
            res = Key(color_id=item['color_id'])
        return res

    @classmethod
    def load_enemy(cls, enemy_data, current_level):
        room = Room(enemy_data[1][0], enemy_data[1][1], enemy_data[1][2], enemy_data[1][3])
        if enemy_data[0] == 'ghost':
            enemy = Ghost(current_level, room, 0)
        elif enemy_data[0] == 'zombie':
            enemy = Zombie(current_level, room, 0)
        elif enemy_data[0] == 'vampire':
            enemy = Vampire(current_level, room, 0)
        elif enemy_data[0] == 'mimic':
            enemy = Mimic(current_level, room, 0)
        elif enemy_data[0] == 'snake_mage':
            enemy = Snake_mage(current_level, room, 0)
        elif enemy_data[0] == 'ogre':
            enemy = Ogre(current_level, room, 0)
        enemy.set_position(enemy_data[2][0], enemy_data[2][1])

        return enemy

    @classmethod
    def from_dict(cls, data: dict):
        m = cls(data["max_y"], data["max_x"])
        m.game_map = data["game_map"]
        m.current_level = data.get("level", 1)
        m.exit = tuple(data["exit"]) if data["exit"] else None
        m.enemies = []
        for enemy_data in data["enemies"]:
            enemy = Map.load_enemy(enemy_data, m.current_level)
            m.enemies.append(enemy)
        m.items = []
        for type, subtype, (y, x) in data["items"]:
            for item in ITEMS[type.lower()+'s']:
                if item['name'] == subtype:
                    factory = Map.convert_item(type, item)
                    m.items.append((factory, (y, x)))
        return m





    def _random_floor_cell(self, room):
        while True:
            x = random.randint(room.x+1, room.x+room.width-2)
            y = random.randint(room.y+1, room.y+room.height-2)
            # проверяем - пусто ли
            if self.game_map[y][x] == FLOOR_SYMBOL and \
            all((y,x) != pos for _,pos in self.items):
                return x,y


    def _doors_per_level(self) -> int:
               """
               1-3 уровни  → 3 двери (RGB)
               4-6 уровни  → 4 (RGBY)
               7-9 уровни  → 5 (RGBYO)
               10+ уровни → 6 (RGBYOP)
               """
               max_colors = len(DOOR_KEY_COLORS)
               return min(3 + (self.current_level-1)//3, max_colors)


    # def _place_doors(self, amount=3):
    #     self.doors.clear()
    #     colors = random.sample(DOOR_KEY_COLORS, k=amount)
    def _place_doors(self):
        self.doors.clear()
        colors = random.sample(
            DOOR_KEY_COLORS,
            k=self._doors_per_level()
        )
        for cid in colors:
            door_room = random.choice(self.rooms[1:])          # не стартовая
            xy = self._find_door_tile(door_room)
            if not xy:                                         # редко, но вдруг
                continue
            x, y = xy
            self.game_map[y][x] = DOOR_CLOSED[cid]
            self.doors.append([y, x, cid, False])              # y,x,color,open?



    def _place_keys(self):
        from domain.map_generation.key import Key
        for _, _, cid, _ in self.doors:
            # Комната, отличная от комнаты двери
            while True:
                key_room = random.choice(self.rooms[1:])
                kx, ky = self._random_floor_cell(key_room)
                if self.game_map[ky][kx] == FLOOR_SYMBOL:
                    self.items.append((Key(cid), (ky, kx)))
                    break



    def validate_level(self, start_pos):
        """True, если все двери разблокируемы своими ключами."""
        # копия карты: будем временно «открывать» двери
        gmap = [row[:] for row in self.game_map]

        def bfs(src, tgt, opened=set()):
            q = deque([src]); seen={src}
            while q:
                x,y = q.popleft()
                if (x,y)==tgt: return True
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny = x+dx, y+dy
                    if not (0<=nx< self.max_x and 0<=ny< self.max_y): continue
                    cell = gmap[ny][nx]
                    if (nx,ny) in seen: continue
                    # стена?
                    if cell in (WALL_SYMBOL, VERTICAL_WALL, HORIZONTAL_WALL,
                                TOP_LEFT_CORNER, TOP_RIGHT_CORNER,
                                LOW_LEFT_CORNER, LOW_RIGHT_CORNER):
                        continue
                    # закрытая дверь, а её цвета ещё нет в opened?
                    if cell in DOOR_CLOSED.values():
                        cid = [k for k,v in DOOR_CLOSED.items() if v==cell][0]
                        if cid not in opened:
                            continue
                    seen.add((nx,ny))
                    q.append((nx,ny))
            return False

        opened_colors = set()
        sx,sy = start_pos
        for y,x,cid,_ in self.doors:            # порядок не важен
            key_pos = None
            for itm,(iy,ix) in self.items:
                if isinstance(itm, Key) and itm.color_id==cid:
                    key_pos = (ix,iy); break
            if key_pos is None:                 # ключ кудато делся
                return False
            # 1) можно ли добраться до KEY со всеми уже открытыми дверями?
            if not bfs((sx,sy), key_pos, opened_colors):
                return False
            opened_colors.add(cid)              # считаем ключ подняли
            # 2) теперь открытую дверь добавляем во множество
            if not bfs(key_pos, (x,y), opened_colors):
                return False
        return True


    # def _find_door_tile(self, room):
    #     """Возвращает координату (x,y) клетки, где коридор соприкасается со стеной."""
    #     for x in range(room.x, room.x + room.width):
    #         for y in [room.y - 1, room.y + room.height]:      # верх/низ
    #             if 0 <= y < self.max_y and self.game_map[y][x] == CORRIDOR_SYMBOL:
    #                 return (x, y)
    #     for y in range(room.y, room.y + room.height):
    #         for x in [room.x - 1, room.x + room.width]:       # лево/право
    #             if 0 <= x < self.max_x and self.game_map[y][x] == CORRIDOR_SYMBOL:
    #                 return (x, y)
    #     return None  # если вдруг коридора нет

    def _find_door_tile(self, room):
        """Возвращает координату (x,y) клетки, где коридор соприкасается со стеной."""
        for x in range(room.x, room.x + room.width):
            for y in (room.y-1, room.y + room.height):
                if 0 <= y < self.max_y and self.game_map[y][x] == CORRIDOR_SYMBOL:
                    return x, y
        for y in range(room.y, room.y + room.height):
            for x in (room.x-1, room.x + room.width):
                if 0 <= x < self.max_x and self.game_map[y][x] == CORRIDOR_SYMBOL:
                    return x, y
        return None

    def _place_doors_and_keys(self):
            """
            Создаёт по одной двери и соответствующему ключу.
            Простая стратегия: берем random room != start_room для двери,
            а ключ кладём в другую room != door_room.
            """
            if len(self.rooms) < 3:
                return

            start_room = self.rooms[0]
            color = random.choice(DOOR_KEY_COLORS)
            while True:
                door_room = random.choice([r for r in self.rooms if r is not start_room])
                key_room  = random.choice([r for r in self.rooms if r is not door_room])

                # 1) Временные координаты
                door_xy = self._find_door_tile(door_room)
                if door_xy is None:
                    return                              # на всякий случай

                dx, dy = door_xy
                self.game_map[dy][dx] = color[0].upper()
                self.doors.append(((dy, dx), color))
                kx = random.randint(key_room.x + 1, key_room.x + key_room.width - 2)
                ky = random.randint(key_room.y + 1, key_room.y + key_room.height - 2)

                # 2) Проверяем путь: key - door - exit
                #    (door клетка временно делается проходимой)
                self.game_map[dy][dx] = FLOOR_SYMBOL
                reachable = self.has_path((kx, ky), self.exit)
                self.game_map[dy][dx] = WALL_SYMBOL

                if reachable:
                    break