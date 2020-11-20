from typing import List, Union, Callable, Tuple

import pygame

from misc.constants import Color, BUTTON_DEFAULT_COLORS, Font, ButtonColor
from objects.base import DrawableObject


class BaseButton(DrawableObject):
    def __init__(self, game, geometry: Union[tuple, pygame.Rect], function: Callable[[], None]) -> None:
        super().__init__(game)
        if type(geometry) == tuple:
            self.rect = pygame.Rect(*geometry)
        else:
            self.rect = geometry
        self.function = function

    def parse_rect(self, geometry: Union[tuple, pygame.Rect]) -> pygame.Rect:
        if type(geometry) == tuple:
            return pygame.Rect(*geometry)
        elif type(geometry) == pygame.Rect:
            return geometry
        raise TypeError('Invalid geometry type (can only be tuple or pygame.Rect')

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.click()

    def process_draw(self) -> None:
        pygame.draw.rect(self.game.screen, Color.WHITE, self.rect, 0)

    def click(self) -> None:
        self.function()


class Button(BaseButton):
    STATE_INITIAL = 0
    STATE_HOVER = 1
    STATE_CLICK = 2

    def __init__(self, game, geometry: Union[tuple, pygame.Rect],
                 function: Callable[[], None], text: str = 'Define me',
                 colors: Union[dict, ButtonColor] = BUTTON_DEFAULT_COLORS,
                 center: Tuple[float, float] = None) -> None:
        super().__init__(game, geometry, function)
        self.text = text
        self.font = pygame.font.Font(Font.FILENAME, 60)
        self.colors: ButtonColor = self.parse_colors(colors)
        self.state = self.STATE_INITIAL
        self.surfaces = self.prepare_surfaces()
        self.left_button_pressed = False
        if center:
            self.move_center(*center)

    @staticmethod
    def parse_colors(colors: Union[dict, ButtonColor]) -> ButtonColor:
        if type(colors) == dict:
            result = ButtonColor()
            result.from_dict(colors)
            return result
        elif type(colors) == ButtonColor:
            return colors
        else:
            raise TypeError('Invalid button colors type (can only be dict or ButtonColor)')

    def mouse_hover(self, pos: Tuple[Union[int, float], Union[int, float]]) -> bool:
        return bool(self.rect.collidepoint(pos))

    def process_mouse_motion(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEMOTION:
            return
        if self.mouse_hover(event.pos):
            if not self.left_button_pressed:
                self.state = self.STATE_HOVER
        else:
            self.state = self.STATE_INITIAL

    def process_mouse_button_down(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if event.button == pygame.BUTTON_LEFT:
            self.left_button_pressed = True
        if self.mouse_hover(event.pos):
            self.state = self.STATE_CLICK

    def process_mouse_button_up(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONUP:
            return
        if event.button == pygame.BUTTON_LEFT:
            self.left_button_pressed = False
        if self.mouse_hover(event.pos) and event.button == pygame.BUTTON_LEFT:
            self.state = self.STATE_INITIAL

    def process_event(self, event: pygame.event.Event) -> None:
        self.process_mouse_motion(event)
        self.process_mouse_button_down(event)
        self.process_mouse_button_up(event)
        super().process_event(event)

    def update_text(self, text: str) -> None:
        self.text = text
        self.prepare_surfaces()

    def prepare_surfaces(self) -> List[pygame.Surface]:
        surfaces = []
        for index in range(len(self.colors.get_members_list())):
            surfaces.append(self.prepare_surface(index))
        return surfaces

    def prepare_surface(self, state_index: int) -> pygame.Surface:
        surface = pygame.surface.Surface(self.rect.size)
        zero_rect = surface.get_rect()

        text_surface = self.font.render(self.text, True, self.colors[state_index].text)
        zero_text_rect = text_surface.get_rect()
        zero_text_rect.center = zero_rect.center

        pygame.draw.rect(surface, self.colors[state_index].background, zero_rect, 0)
        surface.blit(text_surface, zero_text_rect)

        return surface

    def process_draw(self) -> None:
        self.game.screen.blit(self.surfaces[self.state], self.rect.topleft)

    def select(self):
        self.state = self.STATE_HOVER

    def deselect(self):
        self.state = self.STATE_INITIAL

    def activate(self):
        self.state = self.STATE_CLICK