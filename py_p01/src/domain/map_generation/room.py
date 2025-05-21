import random
from config.constants import (
    WALL_SYMBOL, FLOOR_SYMBOL, CORRIDOR_SYMBOL,
    TOP_LEFT_CORNER, TOP_RIGHT_CORNER, LOW_LEFT_CORNER, LOW_RIGHT_CORNER,
    VERTICAL_WALL, HORIZONTAL_WALL
)

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

    def intersect(self, other):
        return (self.x <= other.x + other.width and
                self.x + self.width >= other.x and
                self.y <= other.y + other.height and
                self.y + self.height >= other.y)

    def draw(self, game_map):
        for j in range(self.height):
            for i in range(self.width):
                sx = self.x + i
                sy = self.y + j
                if 0 <= sy < len(game_map) and 0 <= sx < len(game_map[0]):
                    if (i == 0 and j == 0):
                        game_map[sy][sx] = TOP_LEFT_CORNER
                    elif (i == self.width - 1 and j == 0):
                        game_map[sy][sx] = TOP_RIGHT_CORNER
                    elif (i == 0 and j == self.height - 1):
                        game_map[sy][sx] = LOW_LEFT_CORNER
                    elif (i == self.width - 1 and j == self.height - 1):
                        game_map[sy][sx] = LOW_RIGHT_CORNER
                    elif i == 0 or i == self.width - 1:
                        game_map[sy][sx] = VERTICAL_WALL
                    elif j == 0 or j == self.height - 1:
                        game_map[sy][sx] = HORIZONTAL_WALL
                    else:
                        game_map[sy][sx] = FLOOR_SYMBOL

    @staticmethod
    def create_h_tunnel(x1, x2, y, game_map):
        """Создает горизонтальный коридор."""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= y < len(game_map) and 0 <= x < len(game_map[0]):
                if game_map[y][x] == WALL_SYMBOL or game_map[y][x] in (
                        TOP_LEFT_CORNER, TOP_RIGHT_CORNER, LOW_LEFT_CORNER, LOW_RIGHT_CORNER, VERTICAL_WALL,
                        HORIZONTAL_WALL):
                    game_map[y][x] = CORRIDOR_SYMBOL

                if 0 <= y - 1 < len(game_map) and 0 <= y + 1 < len(game_map):
                    if game_map[y - 1][x] == WALL_SYMBOL:
                        game_map[y - 1][x] = HORIZONTAL_WALL
                    if game_map[y + 1][x] == WALL_SYMBOL:
                        game_map[y + 1][x] = HORIZONTAL_WALL

    @staticmethod
    def create_v_tunnel(y1, y2, x, game_map):
        """Создает вертикальный коридор."""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= y < len(game_map) and 0 <= x < len(game_map[0]):
                if game_map[y][x] == WALL_SYMBOL or game_map[y][x] in (
                        TOP_LEFT_CORNER, TOP_RIGHT_CORNER, LOW_LEFT_CORNER, LOW_RIGHT_CORNER, VERTICAL_WALL,
                        HORIZONTAL_WALL):
                    game_map[y][x] = CORRIDOR_SYMBOL

                if 0 <= x - 1 < len(game_map[0]) and 0 <= x + 1 < len(game_map[0]):
                    if game_map[y][x - 1] == WALL_SYMBOL:
                        game_map[y][x - 1] = VERTICAL_WALL
                    if game_map[y][x + 1] == WALL_SYMBOL:
                        game_map[y][x + 1] = VERTICAL_WALL

    @staticmethod
    def connect_rooms(rooms, game_map):
        """Соединяет комнаты"""
        for i in range(1, len(rooms)):
            prev_center = rooms[i-1].center()
            curr_center = rooms[i].center()
            '''Вероятно ненужная дичь, замедляющая соединение тоннелей'''
            if random.randint(0, 1) == 1:
                Room.create_h_tunnel(prev_center[0], curr_center[0], prev_center[1], game_map)
                Room.create_v_tunnel(prev_center[1], curr_center[1], curr_center[0], game_map)
            else:
                Room.create_v_tunnel(prev_center[1], curr_center[1], prev_center[0], game_map)
                Room.create_h_tunnel(prev_center[0], curr_center[0], curr_center[1], game_map)



    @staticmethod
    def fix_corners(game_map):
        max_y = len(game_map)
        max_x = len(game_map[0]) if max_y > 0 else 0
        for y in range(max_y):
            for x in range(max_x):
                if game_map[y][x] == CORRIDOR_SYMBOL:
                    if y > 0 and game_map[y-1][x] == HORIZONTAL_WALL:
                        if x > 0 and game_map[y][x-1] == VERTICAL_WALL:
                            game_map[y-1][x-1] = TOP_LEFT_CORNER
                        if x < max_x - 1 and game_map[y][x+1] == VERTICAL_WALL:
                            game_map[y-1][x+1] = TOP_RIGHT_CORNER
                    if y < max_y - 1 and game_map[y+1][x] == HORIZONTAL_WALL:
                        if x > 0 and game_map[y][x-1] == VERTICAL_WALL:
                            game_map[y+1][x-1] = LOW_LEFT_CORNER
                        if x < max_x - 1 and game_map[y][x+1] == VERTICAL_WALL:
                            game_map[y+1][x+1] = LOW_RIGHT_CORNER


