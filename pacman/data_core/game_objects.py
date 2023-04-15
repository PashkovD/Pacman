from typing import List, Iterable

from pacman.data_core.interfaces import IDrawable, ILogical, IEventful

import pygame as pg


class GameObjects(List):
    __included_types = (IDrawable, IEventful, ILogical)

    # region List methods

    def append(self, item) -> None:
        if self.__check_type(item):
            super().append(item)

    def insert(self, index, item) -> None:
        self.__check_type(item)
        super().insert(index, item)

    def extend(self, iterable: Iterable) -> None:
        for item in iterable:
            self.__check_type(item)
        super().extend(iterable)

    def __iadd__(self, other):
        for item in other:
            self.__check_type(item)
        return super().__iadd__(other)

    # endregion

    # region Custom

    def __check_type(self, item) -> bool:
        return isinstance(item, self.__included_types)

    def update(self):
        filtered: Iterable[ILogical] = filter(lambda x: isinstance(x, ILogical), self)
        for obj in filtered:
            obj.update()

    def event_handler(self, event: pg.event.Event):
        filtered: Iterable[IEventful] = filter(lambda x: isinstance(x, IEventful), self)
        for obj in filtered:
            obj.event_handler(event)

    def draw(self, screen: pg.Surface):
        filtered: Iterable[IDrawable] = filter(lambda x: isinstance(x, IDrawable), self)
        for obj in filtered:
            obj.draw(screen)

    # endregion
