import curses
from config.constants import (BACKPACK_HEIGHT, BACKPACK_WIDTH, TREASURE)

class Inventory:
    def __init__(self):
        self.items = {
            'treasure': 0,
            'food': [],
            'potion': [],
            'scroll': [],
            'weapon': [],
            'key': []
        }
        self.cursor_x = 0  # Позиция по горизонтали
        self.cursor_y = 0  # Позиция по вертикали
        self.is_open = False

    def default_pos(self):
        self.cursor_x = 0
        self.cursor_y = 0
    
    def get_cursor(self):
        return self.cursor_x, self.cursor_y
    
    def set_cursor(self, new_x, new_y):
        self.cursor_x = new_x
        self.cursor_y = new_y

    def add_item(self, item):
        if len(self.items[item.item_type]) <= 9:
            self.items[item.item_type].append(item)
            return True
        return False

    def remove_item(self, item):
        if item in self.items.get(item.item_type, []):
            self.items[item.item_type].remove(item)

    def get_item_at_cursor(self):
        items = list(self.items.values())
        items.pop(0)  # Убираем 'treasure' из списка
        items = sum(items, [])  # Объединяем все списки предметов в один

        # Рассчитываем индекс элемента на основе позиции курсора
        index = self.cursor_y * (BACKPACK_WIDTH // 2 - 1) + self.cursor_x

        # Проверяем, что индекс находится в пределах доступных элементов
        if index < len(items):
            return items[index]

        return None  # Если индекс вне границ, возвращаем None