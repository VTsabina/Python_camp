# Здесь определяются все глобальные константы, 
# такие как размеры экрана, символы для стен, пола, коридоров и т.д.

# Константы для отображения и настроек игры

# … существующие импорты / константы …

import curses

# DOOR_KEY_COLORS = ["red", "blue", "green", "yellow", "orange", "purple"]

# DOOR_CLOSED = {
#     "red":    "R",   "blue": "B",   "green": "G",
#     "yellow": "Y",   "orange": "O", "purple": "P"
# }
# DOOR_OPEN = {c.lower(): "+" for c in DOOR_CLOSED}
# KEY_SYMBOLS = {
#     "red": "r", "blue": "b", "green": "g",
#     "yellow": "y", "orange": "o", "purple": "p"
# }



KEY_SYMBOLS = {0: "r", 1: "g", 2: "b",
               3: "y", 4: "o", 5: "p"}
COLOR_INDEX = {0: "red", 1: "green", 2: "blue",
               3: "yellow", 4: "white", 5: "purple"}
DOOR_CLOSED = {0: "R", 1: "G", 2: "B",
               3: "Y", 4: "O", 5: "P"}
DOOR_OPEN   = {0: "+", 1: "+", 2: "+",
               3: "+", 4: "+", 5: "+"}


DOOR_KEY_COLORS = list(KEY_SYMBOLS.keys())         # [0,1,2,3,4,5]


DOOR_COLORS = {
    0: curses.COLOR_RED,      # R
    1: curses.COLOR_GREEN,     # G
    2: curses.COLOR_BLUE,    # B
    3: curses.COLOR_YELLOW,   # Y
    4: curses.COLOR_WHITE,  # O
    5: curses.COLOR_MAGENTA,     # P
}



WALL_SYMBOL = '.'
FLOOR_SYMBOL = ' '
CORRIDOR_SYMBOL = ' '

CORRIDOR_WIDTH = 2
TOP_LEFT_CORNER = '╔'
TOP_RIGHT_CORNER = '╗'
LOW_LEFT_CORNER = '╚'
LOW_RIGHT_CORNER = '╝'
VERTICAL_WALL = '║'
HORIZONTAL_WALL = '═'

TREASURE_FOR_SHOW = '💎'
SCROLL_FOR_SHOW = '📜'
FOOD_FOR_SHOW = '🍕'
POTION_FOR_SHOW = '🧪'
WEAPON_FOR_SHOW = '🏹'
KEY_FOR_SHOW = '⚿'

EXITO = 'E'

TREASURE = 't'
SCROLL = 's'
FOOD = 'f'
POTION = 'P'
WEAPON = 'W'

# ВЫ ХА
PLAYER = '@'
VISIBILITY_RADIUS = 8

# Backpack
BACKPACK_WIDTH = 20
BACKPACK_HEIGHT = 6

# Монстры
ZOMBIE =     'Z'
ORGE =       'O'
VAMPIRE =    'V'
SNAKE_MAGE = 'S'
GHOST =      'G'
MIMIC =      'M'

# Размеры экрана (по умолчанию)
DEFAULT_MAP_WIDTH = 80
DEFAULT_MAP_HEIGHT = 24

ITEMS = {
    'foods': [ # name, health_boost, description
        {
            'name': "Apple", 
            'health_boost': 5, 
            'description': 'An apple a day, because it may be last day of your life here'
        },
        {
            'name': "Banana", 
            'health_boost': 8, 
            'description': 'All credits to minions'
        },
        {
            'name': "Bread", 
            'health_boost': 10, 
            'description': "Sooooo tasty while it's fresh, but you found this one in the antient dangeon..."
        },
        {
            'name': "Cheese", 
            'health_boost': 15, 
            'description': "If you can't fix your dinner with cheese, you defenetly just need more cheese"
        },
        {
            'name': "KFC-Chicken", 
            'health_boost': 20, 
            'description': "At least at the game KFC-chicken will increase our health..."
        }
    ],

    'potions': [ # name, time_limit=30, max_health_boost=0, skill_boost=0, strength_boost=0, description
        {
            'name': "Small Health Potion", 
            'time_limit': 30, 
            'max_health_boost': 10, 
            'skill_boost': 0, 
            'strength_boost': 0, 
            'description': "It's possibly placebo, but who cares"
        },
        {
            'name': "Health Potion of Trolls", 
            'time_limit': 30, 
            'max_health_boost': 25, 
            'skill_boost': 0, 
            'strength_boost': 0, 
            'description': "You found this one down the bridge, no doubt it's good idea to drink it"
        }, 
        {
            'name': "Ultimate Health Potion", 
            'time_limit': 15, 'max_health_boost': 50, 
            'skill_boost': 0, 
            'strength_boost': 0, 
            'description': "Fast and furious"
        },
        {
            'name': "Potion of Sword Master", 
            'time_limit': 30, 
            'max_health_boost': 0, 
            'skill_boost': 0, 
            'strength_boost': 15, 
            'description': "Organic, vegan, gluten free, sugar free steroid junk"
        },
        {
            'name': "Sacred Potion of King-Warrior", 
            'time_limit': 30, 
            'max_health_boost': 0, 
            'skill_boost': 0, 
            'strength_boost': 30, 
            'description': "Found in the tomb, no way it could be a trick"
        },
        {
            'name': "God of War's Potion", 
            'time_limit': 15, 
            'max_health_boost': 0, 
            'skill_boost': 0, 
            'strength_boost': 50, 
            'description': "For those who's just tired of stuff and needs a 15-sec lasting Ragnarok to restore the mental health"
        },
        {
            'name': "Potion of Hidden vilage", 
            'time_limit': 30, 
            'max_health_boost': 0, 
            'skill_boost': 15, 
            'strength_boost': 0, 
            'description': "If you don't see enemy, it doesn't see you eather, right?"
        },
        {
            'name': "Secret Potion of West Mountain", 
            'time_limit': 30, 
            'max_health_boost': 0, 
            'skill_boost': 25, 
            'strength_boost': 0, 
            'description': "Who placed this bottle in the cave at tho top of the mountain? He had to be skilled enough"
        },
        {
            'name': "Adrenaline bottle", 
            'time_limit': 15, 
            'max_health_boost': 0, 
            'skill_boost': 50, 
            'strength_boost': 0, 
            'description': "Energy drink of Middle Ages"
        },
        {
            'name': "Enchantiiiiiiiix", 
            'time_limit': 30, 
            'max_health_boost': 0, 
            'strength_boost': 15, 
            'skill_boost': 15, 
            'description': "Magic powder to maximum (beware of V)"
        }
    ],

    'scrolls': [ # name, max_health_boost, skill_boost, strength_boost, description
        {
            'name': "Scroll of the Dragon",
            'max_health_boost': 5,
            'skill_boost': 0,
            'strength_boost': 0,
            'description': "Can be replaced with regular workout"
        },
        {
            'name': "Antient Scroll of Life",
            'max_health_boost': 10,
            'skill_boost': 0,
            'strength_boost': 0,
            'description': "Was much more powerfull before getting antient"
        },
        {
            'name': "Philosopher's Scroll",
            'max_health_boost': 15,
            'skill_boost': 0,
            'strength_boost': 0,
            'description': "Power of healthy thinking and meditation"
        },
        {
            'name': "Ninja Scroll",
            'max_health_boost': 0,
            'skill_boost': 5,
            'strength_boost': 0,
            'description': "Too bad for real ninjas, but okay for you"
        },
        {
            'name': "Thief's Scroll",
            'max_health_boost': 0,
            'skill_boost': 10,
            'strength_boost': 0,
            'description': "You don't need to join dark side if you can steel their cookies"
        },
        {
            'name': "Scroll of Soft-Skills",
            'max_health_boost': 0,
            'skill_boost': 15,
            'strength_boost': 0,
            'description': "Ultimate skill to avoid troubles"
        },
        {
            'name': "Not very powerfull Scroll",
            'max_health_boost': 0,
            'skill_boost': 0,
            'strength_boost': 5,
            'description': "It's not very powerfull, but has a good heart, be nice to him"
        },
        {
            'name': "Powerfull Scroll",
            'max_health_boost': 0,
            'skill_boost': 0,
            'strength_boost': 10,
            'description': "Well that's not the one who's gonna be nice to you, so just use it"
        },
        {
            'name': "Hulk's Scroll",
            'max_health_boost': 0,
            'skill_boost': 0,
            'strength_boost': 15,
            'description': "HUUUUUUULK SMAAAAAASH"
        }
    ],

    'weapons': [ # name, strength_boost, description
        {
            'name': "Simple Sword",
            'strength_boost': 10,
            'description': "Easy but classic piece of steel"
        },
        {
            'name': "Brocken Sword",
            'strength_boost': 6,
            'description': "Piece of steel that used to know some better times"
        },
        {
          	'name': "Nothern Axe",
          	'strength_boost': 12, 
          	'description': "For true berserks, +2 ice damage"
      	},
      	{
          	'name': "Thief's Knife", 
          	'strength_boost': 8, 
          	'description': "Why not if you're skilled enough"
      	},
      	{
          	'name': "Morgenshtern", 
          	'strength_boost': 20, 
          	'description': "Hard to controll but cool"
      	},
      	{
          	'name': "Zweihander", 
          	'strength_boost': 25, 
          	'description': "For those who don't like shields. Oh no, we don't have shields in this game..."
      	},
      	{
          	'name': "Diamond Sword", 
          	'strength_boost': 30, 
          	'description': "Minecraft the Movie strongly recommended (First shown in Russia 12.04.2025)"
      	},
      	{
          	'name': "Wooden stick", 
          	'strength_boost': 5, 
          	'description': "Looks like someone's not enough lucky for good loot"
      	},
      	{
            'name': "Tea-bag", 
            'strength_boost': 2, 
            'description': "Нервный срыв — неиссякаемый источник суперспособностей или как забить человека до смерти чайным пакетиком"
      }
    ],

    'treasures': [ # name, value, description
        {
            "name": "Old Coin", 
            "value": 5, 
            "description": "At least it's still shiny"
        },
        {
            "name": "Silver Coin", 
            "value": 30, 
            "description": "Someone must be upset for loosing it"
        },
        {
            "name": "Bag of Coins", 
            "value": 60, 
            "description": "Now you can finally afford a cat"
        },
        {
            "name": "Golden Bar", 
            "value": 100, 
            "description" : "It's an old dangeon,noone needs it here,right?"
        },
        {
            "name": "Magic Book", 
            "value": 300, 
            "description": "Useless for you,but the magicians will pay well for it"
        },
        {
            "name": "Pokemon Cards Pack", 
            "value": 400, 
            "description": "Contains legendary Snorlax!!! You are gonna rrrrrich!!!"
        },
        {
            "name": "Diamond necklace", 
            "value": 500, 
            "description": "I wonder if the owner is still somewhere here"
        }
    ],

    'keys': [
        {
            "name": 'Red key',
            "color_id": 0
        },
        {
            "name": 'Green key',
            "color_id": 1
        },
        {
            "name": 'Blue key',
            "color_id": 2
        },
        {
            "name": 'Yellow key',
            "color_id": 3
        },
        {
            "name": 'White key',
            "color_id": 4
        },
        {
            "name": 'Purple key',
            "color_id": 5
        }
    ]
}
