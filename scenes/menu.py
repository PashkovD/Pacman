import sys

import pygame as pg

from objects.button import ButtonController, Button
from objects.text import Text
from scenes.base import BaseScene
from misc.constants import Color, Font


class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

    def create_objects(self) -> None:
        self.create_title()
        self.create_buttons()

    def create_title(self) -> None:
        title = Text(self.game, 'PACMAN', 40, color=Color.WHITE, font=Font.FILENAME)
        title.move_center(self.game.width // 2, 30)
        self.objects.append(title)

    def create_buttons(self) -> None:
        buttons = [
            Button(self.game, pg.Rect(0, 0, 180, 30),
                   self.start_game, 'PLAY',
                   center=(self.game.width // 2, 80),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 30),
                   self.start_levels, 'LEVELS',
                   center=(self.game.width // 2, 120),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 30),
                   self.start_records, 'RECORDS',
                   center=(self.game.width // 2, 160),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 30),
                   self.start_titres, 'CREDITS',
                   center=(self.game.width // 2, 200),
                   text_size=Font.BUTTON_TEXT_SIZE),
            Button(self.game, pg.Rect(0, 0, 180, 30),
                   sys.exit, 'EXIT',
                   center=(self.game.width // 2, 240),
                   text_size=Font.BUTTON_TEXT_SIZE),
        ]
        self.button_controller = ButtonController(self.game, buttons)
        self.objects.append(self.button_controller)

    def on_activate(self) -> None:
        self.button_controller.reset_state()

    def start_game(self) -> None:
        self.game.set_scene('SCENE_GAME')

    def start_records(self) -> None:
        self.game.scenes['SCENE_RECORDS'].create_text_labels()
        self.game.set_scene('SCENE_RECORDS')

    def start_titres(self) -> None:
        self.game.set_scene("SCENE_CREDITS")

    def start_levels(self) -> None:
        self.game.set_scene("SCENE_LEVELS")
