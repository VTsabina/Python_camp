# # Главный файл, который импортирует все нужные модули и запускает основной цикл игры. 
# # Здесь происходит инициализация карты, создание объектов, связывание логики и UI,
# #  обработка событий.

import curses
from curses import wrapper
from presentation.ui import GameUI

def main(stdscr):
    ui = GameUI()
    ui.start_game(stdscr)
    ui.display_statistics(stdscr)

if __name__ == '__main__':
    wrapper(main)
