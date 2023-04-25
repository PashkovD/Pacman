from typing import Tuple

from .base import Base
from ...misc.serializers import SettingsStorage


class Clyde(Base):
    seed_percent_in_home = 15
    love_point_in_scatter_mode = (0, 32)

    def __init__(self, game, start_pos: Tuple[int, int], seed_count):
        frightened_time = 8000
        chase_time = 0
        scatter_time = 0
        if SettingsStorage().difficulty == 1:
            frightened_time = 4000
            chase_time = 0
            scatter_time = 0
        elif SettingsStorage().difficulty == 2:
            frightened_time = 2000
            chase_time = 0
            scatter_time = 0
        super().__init__(game, start_pos, seed_count, frightened_time, chase_time, scatter_time)
        self.mode = "Chase"
        self.shift_y = 1
        self.set_direction("up")
        self.is_in_home = True

    def home_ai(self, eaten_seed):
        super().home_ai(eaten_seed)
        if self.can_leave_home(eaten_seed):
            self.set_direction("left")
            self.go()
            scene = self.game.current_scene
            if self.rect.centerx == scene.pinky.start_pos[0]:
                self.set_direction("up")
            if self.rect.centery == scene.blinky.start_pos[1]:
                self.set_direction("left")
                self.is_in_home = False
                self.collision = True

    def ghosts_ai(self) -> None:
        super().ghosts_ai()
        scene = self.game.current_scene
        pacman = scene.pacman
        if self.mode == "Scatter":
            self.love_cell = self.love_point_in_scatter_mode
            if self.two_cells_dis(self.get_cell(), pacman.get_cell()) >= 8:
                self.mode = "Chase"
        elif self.mode == "Chase":
            self.love_cell = pacman.get_cell()
            if self.two_cells_dis(self.get_cell(), pacman.get_cell()) <= 8:
                self.mode = "Scatter"
