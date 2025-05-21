import random
from config.constants import (ZOMBIE, ORGE, VAMPIRE, SNAKE_MAGE, GHOST, MIMIC, TREASURE, SCROLL, FOOD, POTION, WEAPON)

class Enemy:
    def __init__(self, enemy_type, health, skill, strength, hostility, room):
        self.enemy_type = enemy_type
        self.health = health
        self.skill = skill
        self.strength = strength
        self.hostility = hostility  # радиус агрессии
        self.position = (0, 0)
        self.is_alive = True
        self.is_resting = False
        self.first_attack = True if enemy_type == 'vampire' else False
        self.is_active = False if enemy_type == 'mimic' else True
        self.teleport_timer = 0
        self.is_invisible = False
        self.sleep_attack_chance = 0.3 if enemy_type == 'snake_mage' else 0
        self.attack_cooldown = 0
        self.room = room

    def get_symbol(self):
        symbols = {
            'zombie': ZOMBIE,
            'ogre': ORGE,
            'vampire': VAMPIRE,
            'snake_mage': SNAKE_MAGE,
            'ghost': GHOST,
            'mimic': MIMIC
        }
        if self.is_invisible:
            return ' '
        elif self.enemy_type == 'mimic' and not self.is_active:
            return self.fake_face
        return symbols.get(self.enemy_type, ' ')

    def get_position(self):
        return self.position

    def set_position(self, x, y, game_map=None):
        if game_map is None or game_map.is_passable(x, y):
            self.position = (x, y)
            return True
        return False

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.is_alive = False

    def calculate_movement(self, player_pos, game_map):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            return
        elif self._should_chase(player_pos, game_map):
            if self.enemy_type == 'mimic' and not self.is_active:
                self.is_active =True
            if self.enemy_type == 'ghost' and self.is_invisible:
                self.is_invisible = False
            self._chase_player(player_pos, game_map)
        else:
            if self.enemy_type == 'mimic' and self.is_active:
                self.is_active = False
            self._patrol(game_map)

    def _should_chase(self, player_pos, game_map):
        distance = abs(self.position[0] - player_pos[0]) + abs(self.position[1] - player_pos[1])
        return distance <= self.hostility and game_map.has_path(self.position, player_pos)

    def _chase_player(self, player_pos, game_map):
        path = game_map.find_path(self.position, player_pos)
        if path and len(path) > 1:
            next_pos = path[1]
            if self.room.x < next_pos[0] < self.room.x + self.room.width and self.room.y < next_pos[1] < self.room.y + self.room.height:
                if next_pos[0] != player_pos[0] and next_pos[1] != player_pos[1]:
                    self.set_position(next_pos[0], next_pos[1], game_map)

    def _patrol(self, game_map):
        if self.enemy_type == 'ghost':
            self._ghost_pattern(game_map)
        elif self.enemy_type == 'ogre':
            self._ogre_pattern(game_map)
        elif self.enemy_type == 'snake_mage':
            self._snake_pattern(game_map)
        elif self.enemy_type == 'mimic':
            self._mimic_pattern()
        else:
            self._basic_pattern(game_map)

    def _ghost_pattern(self, game_map):
        invis = random.randint(0, 5)
        if invis < 2:
            self.is_invisible = True
        else:
            self.is_invisible = False
        self.teleport_timer += 1
        if self.teleport_timer >= 2:
            self.teleport_timer = 0
            x = random.randint(0, self.room.width - 1)
            y = random.randint(0, self.room.height - 1)
            self.set_position(self.room.x + x, self.room.y + y, game_map)

    def _ogre_pattern(self, game_map):
        moves = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(moves)
        dx, dy = moves[0]
        x = self.position[0] + dx
        y = self.position[1] + dy
        if  self.room.x < x < self.room.x + self.room.width and self.room.y < y < self.room.y + self.room.height:
            self.set_position(x, y, game_map)

    def _snake_pattern(self, game_map):
        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        x = self.position[0] + dx
        y = self.position[1] + dy
        if  self.room.x < x < self.room.x + self.room.width and self.room.y < y < self.room.y + self.room.height:
            self.set_position(x, y, game_map)

    def _mimic_pattern(self): #MIMIC
        pass

    def _basic_pattern(self, game_map):
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(moves)
        dx, dy = moves[0]
        x = self.position[0] + dx
        y = self.position[1] + dy
        if  self.room.x < x < self.room.x + self.room.width and self.room.y < y < self.room.y + self.room.height:
            self.set_position(x, y, game_map)


    def perform_attack(self, player, game_map):
        if self.enemy_type == 'vampire' and self.first_attack:
            self.first_attack = False
            game_map.status_info.insert(0, f"{self.enemy_type.title()} is skipping his first attack!")
        elif self.enemy_type == 'ogre' and self.is_resting:
            self.is_resting = False
            game_map.status_info.insert(0, f"{self.enemy_type.title()} is resting and skipping his attack!")
        else:
            hit_chance = (self.skill / (self.skill + player.skill)) * 100
            if random.randint(1, 100) <= hit_chance:
                damage = self.strength
                self._apply_special_effects(player, damage)
                player.take_damage(damage)
                game_map.status_info.insert(0, f"{self.enemy_type.title()} attacks you for {damage} XP!")
                player.hits_received += 1

                if self.enemy_type == 'ogre':
                    self.is_resting = True
                    self.attack_cooldown = 1
            else:
                game_map.status_info.insert(0, f"Lucky you, {self.enemy_type} failed his attack!")

    def _apply_special_effects(self, player, damage):
        if self.enemy_type == 'vampire':
            new_max_health = max(10, player.max_health - damage // 2)
            player.max_health = new_max_health
            player.current_health = min(player.current_health, new_max_health)
        elif self.enemy_type == 'snake_mage' and random.random() < self.sleep_attack_chance:
            player.set_skip_next_turn(True)

    def calculate_treasure_drop(self):
        base_value = (self.hostility * 0.4 + self.strength * 0.3 +
                      self.skill * 0.2 + self.health * 0.1) / 100
        treasure_amount = base_value * random.uniform(0.8, 1.2)
        return max(100, int(round(treasure_amount * 1000)))
    
class Snake_mage(Enemy):
    def __init__(self, current_level, room, indx):
        health = 80 + (4 * current_level) - indx
        if health < 25:
            health = 25
        skill = 50 + (5 * current_level) - (indx / 3)
        if skill < 35:
            skill = 35
        strength = 12 + (2 * current_level)
        hostility = 5
        super().__init__(enemy_type='snake_mage', health=health, skill=skill, strength=strength, hostility=hostility, room=room)

class Zombie(Enemy):
    def __init__(self, current_level, room, indx):
        health = 92 + (4 * current_level) - indx
        if health < 30:
            health = 30
        skill = 15 + (5 * current_level) - (indx / 5)
        if skill < 5:
            skill = 5
        strength = 9 + (2 * current_level)
        hostility = 4
        super().__init__(enemy_type='zombie', health=health, skill=skill, strength=strength, hostility=hostility, room=room)

class Vampire(Enemy):
    def __init__(self, current_level, room, indx):
        health = 92 + (4 * current_level) - indx
        if health < 30:
            health = 30
        skill = 40 + (5 * current_level) - (indx / 3)
        if skill < 20:
            skill = 20
        strength = 9 + (2 * current_level)
        hostility = 5
        super().__init__(enemy_type='vampire', health=health, skill=skill, strength=strength, hostility=hostility, room=room)

class Ghost(Enemy):
    def __init__(self, current_level, room, indx):
        health = 50 + (4 * current_level) - indx
        if health < 20:
            health = 20
        skill = 50 + (5 * current_level) - (indx / 3)
        if skill < 35:
            skill = 35
        strength = 5 + (2 * current_level)
        hostility = 3
        super().__init__(enemy_type='ghost', health=health, skill=skill, strength=strength, hostility=hostility, room=room)
    
class Ogre(Enemy):
    def __init__(self, current_level, room, indx):
        health = 100 + (4 * current_level) - indx
        if health < 40:
            health = 40
        skill = 15 + (5 * current_level) - (indx / 5)
        if skill < 5:
            skill = 5
        strength = 14 + (2 * current_level)
        hostility = 4
        super().__init__(enemy_type='ogre', health=health, skill=skill, strength=strength, hostility=hostility, room=room)

class Mimic(Enemy):
    def __init__(self, current_level, room, indx):
        health = 92 + (4 * current_level) - indx
        if health < 30:
            health = 30
        skill = 50 + (5 * current_level) - (indx / 3)
        if skill < 25:
            skill = 25
        strength = 5 + (2 * current_level)
        hostility = 3
        super().__init__(enemy_type='mimic', health=health, skill=skill, strength=strength, hostility=hostility, room=room)
        self.fake_face = random.choice([TREASURE, POTION, SCROLL, WEAPON, FOOD])