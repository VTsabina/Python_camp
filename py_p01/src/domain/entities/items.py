from config.constants import (
    TREASURE, SCROLL, FOOD, POTION, WEAPON,
    TREASURE_FOR_SHOW, SCROLL_FOR_SHOW, FOOD_FOR_SHOW, POTION_FOR_SHOW, WEAPON_FOR_SHOW, KEY_FOR_SHOW
)

class Item:
    def __init__(self, item_type, subtype='something', time_limit=0, health_boost=0, max_health_boost=0,
                 skill_boost=0, strength_boost=0, value=0, description='Just some junk you found'):
        self.item_type = item_type
        self.subtype = subtype
        self.health_boost = health_boost
        self.max_health_boost = max_health_boost
        self.skill_boost = skill_boost
        self.strength_boost = strength_boost
        self.time_limit = time_limit
        self.value = value
        self.symbol = self.get_symbol()
        self.description = description

    def get_symbol(self):
        if self.item_type == 'treasure':
            return TREASURE
        elif self.item_type == 'scroll':
            return SCROLL
        elif self.item_type == 'food':
            return FOOD
        elif self.item_type == 'weapon':
            return WEAPON
        elif self.item_type == 'potion':
            return POTION
        return ' '
    
    def get_symbol_for_show(self):
        if self.item_type == 'treasure':
            return TREASURE_FOR_SHOW
        elif self.item_type == 'scroll':
            return SCROLL_FOR_SHOW
        elif self.item_type == 'food':
            return FOOD_FOR_SHOW
        elif self.item_type == 'weapon':
            return WEAPON_FOR_SHOW
        elif self.item_type == 'potion':
            return POTION_FOR_SHOW
        elif self.item_type == 'key':
            return KEY_FOR_SHOW
        return ' '

    def apply_effect(self, player): # to override
        pass


class Food(Item):
    def __init__(self, name, health_boost, description=None):
        super().__init__(item_type='food', subtype=name, health_boost=health_boost, description=description)

    def apply_effect(self, player):
        player.heal(self.health_boost)
        player.food_eaten += 1


class Potion(Item):
    def __init__(self, name, time_limit=30, max_health_boost=0,
                 skill_boost=0, strength_boost=0, description=None):
        super().__init__(item_type='potion', subtype=name, time_limit=time_limit, health_boost=max_health_boost, skill_boost=skill_boost, strength_boost=strength_boost,
                         max_health_boost=max_health_boost, description=description)

    def apply_effect(self, player):
        buff = [self.max_health_boost, self.skill_boost, self.strength_boost, self.time_limit]
        player.current_bufs.append(buff)
        player.strength += self.strength_boost
        player.skill += self.skill_boost
        player.max_health += self.max_health_boost
        player.heal(self.max_health_boost)
        player.potions_drunk += 1


class Scroll(Item):
    def __init__(self, name, max_health_boost=0,
                 skill_boost=0, strength_boost=0, description=None):
        super().__init__(item_type='scroll', subtype=name, health_boost=max_health_boost, skill_boost=skill_boost, strength_boost=strength_boost,
                         max_health_boost=max_health_boost, description=description)

    def apply_effect(self, player):
        player.strength += self.strength_boost
        player.skill += self.skill_boost
        player.max_health += self.max_health_boost
        player.heal(self.max_health_boost)
        player.scrolls_read += 1


class Weapon(Item):
    def __init__(self, name, strength_boost, description=None):
        super().__init__(item_type='weapon', subtype=name, strength_boost=strength_boost, description=description)

    def apply_effect(self, player):
        player.equip_weapon(self)


class Treasure(Item):
    def __init__(self, name, value, description=None):
        super().__init__(item_type='treasure', subtype=name, value=value, description=description)

    def apply_effect(self, player):
        player.add_treasure(self.value)