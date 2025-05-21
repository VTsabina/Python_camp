from domain.entities.items import Item
from config.constants import KEY_SYMBOLS, COLOR_INDEX

class Key(Item):
    def __init__(self, color_id: int):
        self.color_id = color_id
        super().__init__("key", subtype=f"{COLOR_INDEX[color_id].title()} key", description=f"{COLOR_INDEX[color_id].title()} key. Good thing if you need to open smth")

    def get_symbol(self):
        return KEY_SYMBOLS[self.color_id]
    
    def apply_effect(self, player):
        pass
