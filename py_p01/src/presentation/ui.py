# ui.py — curses-frontend

# Модуль для отрисовки игрового мира с помощью библиотеки curses.
#  Отдельная функция отвечает за отображение карты, персонажей, предметов 
#  и пользовательского интерфейса (например, панели состояния или инвентаря).

import curses
import random

from domain.game_session        import GameSession
from domain.map_generation.key   import Key
from .input_handler              import InputHandler
from datalayer.save_load         import save_attempts, save_in_progress
from datalayer.save_load   import load_in_progress, load_attempts, save_in_progress, save_attempts
from domain.map_generation.map import Map
from domain.entities.player     import Player

from config.constants import (
    # тайлы карты
    WALL_SYMBOL, TOP_LEFT_CORNER, TOP_RIGHT_CORNER,
    LOW_LEFT_CORNER,  LOW_RIGHT_CORNER, VERTICAL_WALL, HORIZONTAL_WALL,
    FLOOR_SYMBOL, CORRIDOR_SYMBOL,

    # гейм-плей
    VISIBILITY_RADIUS, BACKPACK_HEIGHT, BACKPACK_WIDTH, TREASURE,

    # двери / ключи
    DOOR_COLORS, DOOR_CLOSED, DOOR_OPEN
)

from .logos_misc import (
    START_LOGO, GAME_OVER_LOGO, WIN_LOGO, GAME_OVER_LOGO, CONTROLS_DICT, QUIT_LOGO
)



class GameUI:
    def __init__(self, *, levels: int = 21) -> None:
        self.session        = GameSession(levels=levels)
        self.input_handler  = InputHandler()
        self._colors_ready  = False
        self._level_cleared = False


    # ────────────────────────── подсветка / палитра ─────────────────────────
    def _init_colors(self) -> None:
        """Инициализируем все цветовые пары ровно один раз за игру."""
        if self._colors_ready:
            return
        self._colors_ready = True

        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1,  curses.COLOR_GREEN,   -1)   # игрок @, HP>60%
        curses.init_pair(2,  curses.COLOR_RED,     -1)   # danger, зелья, low HP
        curses.init_pair(3,  curses.COLOR_WHITE,   -1)   # стены, каркас
        curses.init_pair(4,  curses.COLOR_YELLOW,  -1)   # сокровища, скроллы
        curses.init_pair(5,  curses.COLOR_CYAN,    -1)   # оружие
        curses.init_pair(6,  curses.COLOR_GREEN,   -1)   # пол «точки»
        curses.init_pair(7,  curses.COLOR_WHITE,   -1)   # коридор «кирпич»
        curses.init_pair(8,  curses.COLOR_MAGENTA, -1)   # враги по-умолчанию
        curses.init_pair(9,  curses.COLOR_YELLOW,  -1)   # HP-bar 30–60 %

        # двери/ключи — начинаем с 10
        for cid, col in DOOR_COLORS.items():
            curses.init_pair(10 + cid, col, -1)



    # ───────────────────────────── status bar ───────────────────────────────
    def _print_status_bar(self, stdscr):
        lines    = self.session.game_map.status_info[:4]
        width    = stdscr.getmaxyx()[1] - 4
        for r in range(4):
            stdscr.addstr(r, 0, ' ' * (width + 4))
        for idx, txt in enumerate(reversed(lines)):
            stdscr.addstr(idx, 2, txt[:width])

# ───────────────────────────── карта / тайлы ────────────────────────────
    _WALLS = {WALL_SYMBOL, VERTICAL_WALL, HORIZONTAL_WALL,
              TOP_LEFT_CORNER, TOP_RIGHT_CORNER,
              LOW_LEFT_CORNER, LOW_RIGHT_CORNER}

    def _draw_cell(self, stdscr, ch: str, x: int, y: int):
        scr_y = y + 5
        gm    = self.session.game_map

        try:
            if gm.visible[y][x]:
                # ── видимая клетка ───────────────────────────────────────
                if ch in DOOR_CLOSED.values():                 # закрытая
                    cid  = [c for c, sym in DOOR_CLOSED.items() if sym == ch][0]
                    stdscr.addstr(scr_y, x, ch,
                                  curses.color_pair(10 + cid) | curses.A_BOLD)

                elif ch in DOOR_OPEN.values():                 # открытая
                    stdscr.addstr(scr_y, x, ch,
                                  curses.color_pair(10) | curses.A_DIM)

                elif ch in self._WALLS:                        # стены
                    stdscr.addstr(scr_y, x, ch, curses.color_pair(3))

                elif ch == CORRIDOR_SYMBOL:                    # коридор
                    stdscr.addstr(scr_y, x, '·',
                                  curses.color_pair(7) | curses.A_DIM)

                elif ch == FLOOR_SYMBOL:                       # пол
                    stdscr.addstr(scr_y, x, '▒',
                                  curses.color_pair(6) | curses.A_DIM)

                else:                                          # всё остальное
                    stdscr.addstr(scr_y, x, ch)

            else:
                if ch in (VERTICAL_WALL, HORIZONTAL_WALL, TOP_LEFT_CORNER, TOP_RIGHT_CORNER, LOW_LEFT_CORNER, LOW_RIGHT_CORNER) and gm.explored[y][x]: 
                    stdscr.addstr(scr_y, x, ch, curses.color_pair(3))
                else:
            # ── туман ───────────────────────────────────────────────
                    stdscr.addstr(scr_y, x, '▒',
                                curses.color_pair(3) | curses.A_DIM)

        except curses.error:
            # вывалились за окно – молча игнорим
            pass


    def _draw_map(self, stdscr):
        gm = self.session.game_map
        for y in range(gm.max_y):
            for x in range(gm.max_x):
                self._draw_cell(stdscr, gm.game_map[y][x], x, y)

    
    # ───────────────────────────── стартовые logo ────────────────────────────

    
    def _show_start_logo(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Рисуем лого, обрезая каждую строку по ширине экрана
        for i, line in enumerate(START_LOGO):
            if i >= height:
                break
            safe_line = line[:width]
            try:
                stdscr.addstr(i, 0, safe_line)
            except curses.error:
                # если всё-еще не влезает — пропускаем
                pass
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        stdscr.refresh()

    def _show_controls(self, stdscr):
        self._init_colors()
        # подсказки по управлению
        offset = 1
        for j, (key, desc) in enumerate(CONTROLS_DICT.items()):
            y = offset + j
            # клавиши зелёни
            stdscr.addstr(y, 0, f"{key}", curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(y, len(key), ": ")
            stdscr.addstr(y, len(key) + 2, desc)
        footer_y = offset + len(CONTROLS_DICT) + 1
        stdscr.addstr(footer_y, 0,
                      "Нажмите любую клавишу, чтобы начать…")
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        stdscr.refresh()

    # ───────────────────────────── конечный экран ─────────────────────────────
    def _show_win_logo(self, stdscr):
        """Логотип при полном прохождении всех уровней живым"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        for i, line in enumerate(WIN_LOGO):
            if i >= height: break
            try: stdscr.addstr(i, 0, line[:width])
            except curses.error: pass
        stdscr.addstr(min(height-1, len(WIN_LOGO)+1), 0, "Вы победили! Нажмите любую клавишу…")
        stdscr.refresh()
        stdscr.getch()

    def _show_loss_logo(self, stdscr):
        """Логотип при смерти игрока"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        for i, line in enumerate(GAME_OVER_LOGO):
            if i >= height: break
            try: stdscr.addstr(i, 0, line[:width])
            except curses.error: pass
        stdscr.addstr(min(height-1, len(GAME_OVER_LOGO)+1), 0, "Вы погибли! Нажмите любую клавишу…")
        stdscr.refresh()
        stdscr.getch()

    def _show_quit_logo(self, stdscr):
        """Логотип при аварийном выходе по q"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        for i, line in enumerate(QUIT_LOGO):
            if i >= height: break
            try: stdscr.addstr(i, 0, line[:width])
            except curses.error: pass
        stdscr.addstr(min(height-1, len(QUIT_LOGO)+1), 0, "Ня пака")
        stdscr.refresh()
        stdscr.getch()

    
    # ───────────────────────────── items / ключи ────────────────────────────
    def _draw_items(self, stdscr):
        gm = self.session.game_map
        for item, (iy, ix) in gm.items:
            if not gm.visible[iy][ix]:
                continue

            if isinstance(item, Key):
                attr = curses.color_pair(10 + item.color_id) | curses.A_BOLD
            elif item.item_type == 'potion':
                attr = curses.color_pair(2)
            elif item.item_type == 'weapon':
                attr = curses.color_pair(5)
            else:
                attr = curses.color_pair(4)

            stdscr.addstr(iy + 5, ix, item.symbol, attr)

    # ───────────────────────────── HP-bar / HUD ─────────────────────────────
    def _draw_health(self, stdscr):
        p        = self.session.player
        bottom_y = self.session.game_map.max_y
        ratio    = p.current_health / p.max_health
        filled   = int(30 * ratio)
        bar      = '█' * filled + '░' * (30 - filled)

        clr = 1 if ratio > .6 else 9 if ratio > .3 else 2
        stdscr.addstr(bottom_y + 2, 0, f"Level: {self.session.current_level}")
        stdscr.addstr(bottom_y + 3, 0, f"Health: {p.current_health}/{p.max_health}")
        stdscr.addstr(bottom_y + 4, 0, "HP:", curses.A_BOLD)
        stdscr.addstr(bottom_y + 4, 4, f"[{bar}]", curses.color_pair(clr))

    # ───────────────────────────── враги ────────────────────────────────────
    _ENEMY_CLR = {
        'zombie':      1,
        'vampire':     2,
        'ghost':       8,
        'ogre':        4,
        'snake_mage':  8,
        'mimic':       8,
    }

    def _draw_enemy(self, stdscr, enemy):
        if not enemy.is_alive:
            return
        ex, ey = enemy.get_position()
        if not self.session.game_map.visible[ey][ex]:
            return
        clr = self._ENEMY_CLR.get(enemy.enemy_type, 8)
        stdscr.addstr(ey + 5, ex, enemy.get_symbol(),
                      curses.color_pair(clr) | curses.A_BOLD)

    # ───────────────────────────── основной кадр ────────────────────────────
    def _render(self, stdscr):
        self._init_colors()
        gm = self.session.game_map
        gm.update_fov(*self.session.player.get_position(), VISIBILITY_RADIUS)

        self._print_status_bar(stdscr)
        self._draw_map(stdscr)
        self._draw_items(stdscr)

        # игрок
        px, py = self.session.player.get_position()
        stdscr.addstr(py + 5, px, '@', curses.color_pair(1))

        # враги
        for e in gm.enemies:
            self._draw_enemy(stdscr, e)

        self._draw_health(stdscr)

    # ───────────────────────────── inventory UI ─────────────────────────────
    def _inventory_window(self):
        win = curses.newwin(BACKPACK_HEIGHT + 2, BACKPACK_WIDTH + 20, 5, 5)
        win.attron(curses.color_pair(3))
        win.border()
        return win

    def _show_inventory(self, stdscr):
        curses.curs_set(0)
        player = self.session.player

        while player.inventory.is_open:
            stdscr.refresh()
            items = sum(list(player.inventory.items.values())[1:], [])   # skip treasure

            win = self._inventory_window()
            win.addstr(0, 2, " INVENTORY ", curses.A_BOLD)

            for i in range(1, BACKPACK_HEIGHT - 1):
                for j in range(1, BACKPACK_WIDTH - 1, 2):
                    idx = (i - 1) * (BACKPACK_WIDTH // 2 - 1) + (j // 2)
                    if idx < len(items):
                        itm = items[idx]
                        attr = curses.A_REVERSE if \
                              (player.inventory.cursor_y *
                               (BACKPACK_WIDTH // 2 - 1) + player.inventory.cursor_x) == idx else 0
                        win.addstr(i, j, itm.get_symbol_for_show(), attr)

            win.addstr(BACKPACK_HEIGHT - 1, 1,
                       f"{TREASURE}: {player.treasure_value}",
                       curses.color_pair(4) | curses.A_BOLD)
            active_item = player.inventory.get_item_at_cursor()
            if active_item:
                win.addstr(BACKPACK_HEIGHT, 1, active_item.subtype, curses.A_ITALIC)
            win.refresh()

            self.input_handler.navigate_inventory(win, self.session.game_map,
                                                  player, items,
                                                  active_item,
                                                  stdscr)


    # ───────────────────────────── (это мой) бой ──────────────────────────
    def _fight(self, stdscr, enemy):
        while self.session.player.is_alive and enemy.is_alive:
            gm = self.session.game_map
            gm.status_info.insert(0, f"Attention: {enemy.enemy_type} attacks!")
            self._render(stdscr)
            enemy.perform_attack(self.session.player, gm)
            if not self.session.player.is_alive:
                break

            self._render(stdscr)
            stdscr.getch()

            gm.status_info.insert(0, f"You attack {enemy.enemy_type}!")
            self._render(stdscr)
            self.session.player.attack(enemy, gm)

            if not enemy.is_alive:
                self.session.player.add_treasure(enemy.calculate_treasure_drop())
                gm.enemies.remove(enemy)
                gm.status_info.insert(0, f"{enemy.enemy_type} defeated!")
                self.session.player.enemies_killed += 1

            self._render(stdscr)
            stdscr.getch()

    # ───────────────────────────── один шаг игры ────────────────────────────
    def _game_step(self, stdscr):
        player   = self.session.player
        gm       = self.session.game_map

        # обработка ввода
        new_x, new_y, skip = self.input_handler.handle_input(self.session, stdscr)
        if skip:
            return
        if self.session.exit_requested:
            return

        # инвентарь / статистика
        if player.inventory.is_open:
            self._show_inventory(stdscr)
            return
        if gm.is_statistic_open:
            self._show_stats(stdscr)
            return

        # перемещение, сбор лута и т.д.
        self.session.game_step(new_x, new_y)

        # враги ходят / атакуют
        for enemy in gm.enemies:
            enemy.calculate_movement(player.get_position(), gm)
            if abs(player.get_position()[0] - enemy.get_position()[0]) + \
               abs(player.get_position()[1] - enemy.get_position()[1]) <= 1:
                gm.status_info.insert(0, f"You met {enemy.enemy_type}!")
                self._render(stdscr)
                stdscr.getch()
                self._fight(stdscr, enemy)
                break

        # проверяем выход
        if gm.exit and player.get_position() == gm.exit:
            continue_flag, break_flag = self.input_handler.confirm_exit(stdscr)

            if continue_flag:
                return

            if break_flag:
                self._level_cleared = True
                return

    # ───────────────────────────── level / loop ─────────────────────────────
    def _play_level(self, stdscr):
        self._level_cleared = False
        self.session.init_level()
        while (self.session.player.is_alive
            and not self.session.exit_requested
            and not self._level_cleared):
            self._render(stdscr)
            stdscr.refresh()
            self._game_step(stdscr)



    # ───────────────────────────── stats screen ─────────────────────────────
    def _show_stats(self, stdscr):
        gm   = self.session.game_map
        gm.is_statistic_open = True

        win = curses.newwin(BACKPACK_HEIGHT + 2, BACKPACK_WIDTH + 20, 5, 5)
        win.border()
        win.addstr(0, 2, " STATS ", curses.A_BOLD)
        p = self.session.player
        win.addstr(1, 2, f"Strength : {p.strength}")
        win.addstr(2, 2, f"Agility  : {p.skill}")
        win.addstr(3, 2, f"Treasure : {p.treasure_value}")
        win.addstr(4, 2, f"Damage   : {p.damage}")
        win.refresh()

        self.input_handler.check_stats_closed(self.session, stdscr)
        gm.is_statistic_open = False

    # ───────────────────────────── цикл всей игры ───────────────────────────

    def start_game(self, stdscr):
        curses.curs_set(0)        # прячем курсор
        max_y, max_x = stdscr.getmaxyx()

        # 1) Отрисуем стартовый экран (логотип + управление) в любом случае
        self._show_start_logo(stdscr)
        self._show_controls(stdscr)

        # 2) Попробуем загрузить сохранённую игру
        loaded_state = load_in_progress()
        self.session.attempts = load_attempts()

        loaded = False
        if loaded_state:
            stdscr.clear()
            stdscr.addstr(0, 0, "Найдена сохранённая игра. Продолжить? (y/n): ")
            stdscr.refresh()
            key = None
            while key not in ('n', 'N', 'y', 'Y'):
                key = stdscr.getkey()
                if key.lower() == 'y':
                    # воспроизводим map и player из словарей
                    self.session.current_level = loaded_state['current_level']
                    self.session.game_map = Map.from_dict(loaded_state['map'])
                    self.session.player   = Player.from_dict(loaded_state['player'])
                    loaded = True
                # если отказались — просто начнём новый сеанс
                elif key.lower() == 'n':
                    stdscr.clear()
                    stdscr.refresh()


        # 3) Основной цикл уровней
        while self.session.current_level <= self.session.levels:
            if not loaded:
                # если игра новая — генерим уровень «с нуля»
                self.session.generate_level(max_y - 5, max_x)
            else:
                # единожды загрузили — дальше уже идём по своим
                loaded = False

            self._play_level(stdscr)

            if self.session.exit_requested:
                save_in_progress(self.session.get_state())
                break

            if not self.session.player.is_alive:
                self.session.record_attempt(False)
                save_in_progress(None)
                break

            self.session.current_level += 1

        # 4) Эндскрин победы или поражения
        if self.session.exit_requested:
            # нажали 'q'
            self._show_quit_logo(stdscr)
        elif not self.session.player.is_alive:
            # умерли в бою
            self.session.record_attempt(False)
            self._show_loss_logo(stdscr)
        else:
            # прошли все уровни
            self.session.record_attempt(True)
            self._show_win_logo(stdscr)

        # 5) Сохраняем прогресс и статистику
        if self.session.player.is_alive:
            save_in_progress(self.session.get_state())
        self.session.record_attempt(self.session.player.is_alive)
        save_attempts(self.session.attempts)

    # ───────────────────────────── загрузка save ────────────────────────────
    def init_saved_data(self, saved_state):
        self.session.init_saved_state(saved_state)



    # ─────────────────────── таблица всех попыток ────────────────────────
    def display_statistics(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0,
            "Таблица статистики прохождений (отсортирована по сокровищам):\n\n",
            curses.A_BOLD)

        attempts = sorted(self.session.attempts,
                          key=lambda s: s["treasure"],
                          reverse=True)

        header = ("        Date        | Level | Treasure | Moves | Killed | "
                  "Food | Potions | Scrolls | Hits-deliv | Hits-recv\n"
                  "----------------------------------------------------------------"
                  "-------------------------\n")
        stdscr.addstr(header, curses.color_pair(3) | curses.A_BOLD)

        for row,i in zip(attempts, range(3, curses.LINES-2)):
            line = (f"{row['date']} | {row['level']:5} | {row['treasure']:8} | "
                    f"{row['move_count']:5} | {row['enemies_killed']:6} | "
                    f"{row['food_eaten']:4} | {row['potions_drunk']:7} | "
                    f"{row['scrolls_read']:7} | {row['hits_delivered']:10} | "
                    f"{row['hits_received']:9}\n")
            try:
                stdscr.addstr(i, 0, line)
            except curses.error:
                break       # если терминал низкий – выводим сколько влезет

        stdscr.addstr(curses.LINES-1, 0, "Нажмите любую клавишу для выхода…")
        stdscr.refresh()
        stdscr.getch()