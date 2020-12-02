from .base import Base
import pygame as pg

class Pinky(Base):
    love_point_in_scatter_mode = (2, -3)
    def process_logic(self) -> None:
        if not self.is_invisible:
            super().process_logic()
            if self.is_in_home and self.can_leave_home():
                self.set_direction("up")
                self.go()
                scene = self.game.current_scene
                if self.rect.centery == scene.blinky.start_pos[1]:
                    self.set_direction("left")
                    self.is_in_home = False
                    self.collision = True

    def ghosts_ai(self, pacman, blinky) -> None:
        super().ghosts_ai()
        if self.mode == 'Scatter':
            self.love_cell = self.love_point_in_scatter_mode
            if pg.time.get_ticks() - self.ai_timer >= 7000:
                self.update_ai_timer()
                self.mode = 'Chase'
        if self.mode == 'Chase':
            rotate = pacman.rotate
            self.love_cell = (pacman.get_cell()[0]+self.direction2[rotate][0]*2, pacman.get_cell()[1]+self.direction2[rotate][1]*2)
            if pg.time.get_ticks() - self.ai_timer >= 20000:
                self.update_ai_timer()
                self.mode = 'Scatter'
