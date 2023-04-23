from typing import Tuple, Union
import pygame as pg
from pygame import Surface

from pacman.data_core.interfaces import IDrawable
from pacman.objects import MovementObject


class ImageObject(MovementObject, IDrawable):
    def __init__(self, image: Union[str, pg.Surface] = None, pos: Tuple[int, int] = (0, 0)) -> None:
        super().__init__()
        if isinstance(image, str):
            self.__filename = image
            self.image = pg.image.load(self.__filename).convert_alpha()
        elif isinstance(image, pg.Surface):
            self.image = image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def scale(self, x, y) -> "ImageObject":
        self.image = pg.transform.scale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

    def smoothscale(self, x, y) -> "ImageObject":
        self.image = pg.transform.smoothscale(self.image, (x, y))
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

    def rotate(self, angle) -> "ImageObject":
        self.image = pg.transform.rotate(self.image, angle)
        topleft = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        return self

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)
