from .base import Base
import pygame as pg

class Blinky(Base):
    love_point_in_runaway_mode = (33, -3)
    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            self.collision = True
            self.go()

    def ghosts_ai(self, pacman, blinky) -> None:
        if self.mode == 'Scater':
            self.love_cell = self.love_point_in_runaway_mode
            if pg.time.get_ticks() - self.ai_timer <= 7000:
                self.update_ai_timer()
                self.toggle_mode()
        if self.mode == 'Chase':
            self.love_cell = pacman.get_cell()
            if pg.time.get_ticks() - self.ai_timer <= 20000:
                self.update_ai_timer()
                self.toggle_mode()
