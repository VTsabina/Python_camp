# Модуль, который принимает ввод пользователя (нажатия клавиш)
#  и преобразует их в команды для игрового цикла. 
#  Это помогает отделить обработку ввода от логики отображения.

import curses
from config.constants import BACKPACK_WIDTH

class InputHandler:

    def handle_move_input(self, session, key):
        x, y = session.player.get_position()
        new_x, new_y = x, y
        if key in ['w', 'W', 'KEY_UP']:
            new_y -= 1
        elif key in ['s', 'S', 'KEY_DOWN']:
            new_y += 1
        elif key in ['a', 'A', 'KEY_LEFT']:
            new_x -= 1
        elif key in ['d', 'D', 'KEY_RIGHT']:
            new_x += 1
        
        return new_x, new_y
    

    def handle_inventory_open(self, session, key, stdscr):
        if key in ['i', 'I']:
            if session.player.inventory.is_open == False:
                session.player.inventory.is_open = True


    def handle_stat_request(self, session, key, stdscr):
        if key in ['m', 'M']:
            if session.game_map.is_statistic_open == False:
                session.game_map.is_statistic_open = True


    def handle_input(self, session, stdscr):
        continue_flag = False
        try:
            key = stdscr.getkey()
        except curses.error:
            continue_flag = True
        if key.lower() == 'q':
            session.exit_requested = True

        new_x, new_y = self.handle_move_input(session, key)
        self.handle_inventory_open(session, key, stdscr)
        self.handle_stat_request(session, key, stdscr)

        return new_x, new_y, continue_flag
    
    def confirm_exit(self, stdscr):
        continue_flag = False
        break_flag = False
        stdscr.addstr(5, 0, "Вы на выходе! Нажмите E для перехода.")
        stdscr.refresh()
        try:
            confirm = stdscr.getkey()
        except curses.error:
            continue_flag = True
        if confirm.lower() == 'e':
            stdscr.addstr(6, 0, "Уровень завершён! Переход на следующий уровень...")
            stdscr.refresh()
            curses.napms(1000)  # пауза 1 секунда для показа сообщения
            break_flag = True
        return continue_flag, break_flag
    
    def check_stats_closed(self, session, stdscr):
        while True:
            try:
                key = stdscr.getkey()
                if key in ('m', 'M'):
                    session.game_map.is_statistic_open = False
                    return
            except curses.error:
                continue
    
    def shift_cursor(self, player, items):
        if (player.inventory.cursor_y * (BACKPACK_WIDTH // 2 - 1) + player.inventory.cursor_x + 1) < len(items):
            if (player.inventory.cursor_x + 1) < (BACKPACK_WIDTH // 2 - 1):
                player.inventory.cursor_x += 1
            else:
                if (player.inventory.cursor_y + 1) * (BACKPACK_WIDTH // 2 - 1) < len(items):
                    player.inventory.cursor_x = 0
                    player.inventory.cursor_y += 1
                    

    def use_active(self, win, active_item, player):
        if active_item:
            if active_item.item_type != 'weapon':
                if active_item.item_type != 'key':
                    active_item.apply_effect(player)
                    player.inventory.remove_item(active_item)
                win.refresh()
            else:
                if player.equipped_weapon == None:
                    player.equip_weapon(active_item, map)
                else:
                    player.equipped_weapon = None
                    player.damage = player.strength

    def navigate_inventory(self, win, map, player, items, active_item, stdscr):
        continue_flag = False
        try:
            key = stdscr.getkey()
            if key in ['w', 'W', 'KEY_UP']:
                if player.inventory.cursor_y > 0:
                    player.inventory.cursor_y -= 1
            elif key in ['s', 'S', 'KEY_DOWN']:
                if (player.inventory.cursor_y + 1) * (BACKPACK_WIDTH // 2 - 1) < len(items):
                    player.inventory.cursor_y += 1
            elif key in ['a', 'A', 'KEY_LEFT']:
                if player.inventory.cursor_x > 0:
                    player.inventory.cursor_x -= 1
            elif key in ['d', 'D', 'KEY_RIGHT']:
                self.shift_cursor(player, items)
            elif key in ['e', 'E']:
                self.use_active(win, active_item, player)
            elif key in ['i', 'I']:
                player.inventory.is_open = False
                return
        except curses.error:
            continue_flag = True
            
        return continue_flag