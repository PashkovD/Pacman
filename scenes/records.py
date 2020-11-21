import pygame as pg

from misc.constants import Color
from misc.path import get_image_path
from objects.button import Button
from objects.button import ButtonController
from objects.image import ImageObject
from objects.text import Text
from scenes.base import BaseScene


class RecordsScene(BaseScene):
    def create_objects(self) -> None:
        self.records = self.game.records.data
        self.create_title()
        self.create_error_label()
        self.create_text_labels()
        self.create_medals()
        self.create_buttons()

    def create_text_labels(self) -> None:
        self.one_text = Text(self.game, str(self.records[4]), 30, (60, 45), Color.GOLD)
        self.two_text = Text(self.game, str(self.records[3]), 30, (60, 80), Color.SILVER)
        self.three_text = Text(self.game, str(self.records[2]), 30, (60, 115), Color.BRONZE)
        self.four_text = Text(self.game, '4: ' + str(self.records[1]), 30, (25, 150), Color.WHITE)
        self.five_text = Text(self.game, '5: ' + str(self.records[0]), 30, (25, 185), Color.WHITE)

    def create_medals(self) -> None:
        self.gold_medal = ImageObject(self.game, get_image_path('1_golden', 'medal'), 16, 45)
        self.gold_medal.scale(35, 35)
        self.silver_medal = ImageObject(self.game, get_image_path('2_silver', 'medal'), 16, 80)
        self.silver_medal.scale(35, 35)
        self.bronze_medal = ImageObject(self.game, get_image_path('3_bronze', 'medal'), 16, 115)
        self.bronze_medal.scale(35, 35)
        self.stone_medal = ImageObject(self.game, get_image_path('4_stone', 'medal'), 16, 150)
        self.stone_medal.scale(35, 35)
        self.wooden_medal = ImageObject(self.game, get_image_path('5_wooden', 'medal'), 16, 185)
        self.wooden_medal.scale(35, 35)

    def create_buttons(self) -> None:
        self.back_button = Button(self.game, pg.Rect(self.game.width // 2, 200, 120, 45),
                                  self.start_menu, 'BACK', center=(self.game.width // 2, 250))
        self.button_controller = ButtonController(self.game, [self.back_button])
        self.objects.append(self.button_controller)

    def create_title(self) -> None:
        title = Text(self.game, 'RECORDS', 30, color=Color.WHITE)
        title.move_center(self.game.width // 2, 25)
        self.objects.append(title)

    def create_error_label(self) -> None:
        self.error_text = Text(self.game, 'NO RECORDS', 30, color=Color.RED)
        self.error_text.move_center(self.game.width // 2, 100)

    def start_menu(self) -> None:
        self.game.set_scene(self.game.SCENE_MENU)

    def on_activate(self) -> None:
        self.button_controller.reset_state()

    def process_draw(self) -> None:
        super().process_draw()

        if self.records[4] == 0:
            self.error_text.process_draw()

        if self.records[4] != 0:
            self.one_text.process_draw()
            self.gold_medal.process_draw()

        if self.records[3] != 0:
            self.two_text.process_draw()
            self.silver_medal.process_draw()

        if self.records[2] != 0:
            self.three_text.process_draw()
            self.bronze_medal.process_draw()

        if self.records[1] != 0:
            self.four_text.process_draw()
            self.stone_medal.process_draw()

        if self.records[0] != 0:
            self.five_text.process_draw()
            self.wooden_medal.process_draw()
