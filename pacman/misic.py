from abc import ABC
from random import shuffle
from secrets import choice

from pygame.event import Event

from pacman.data_core import Dirs, PathUtil
from pacman.events.events import EvenType
from pacman.misc.serializers import SettingsStorage, SkinStorage
from pacman.misc.singleton import Singleton
from pacman.misc.sound_controller import Sound
from pacman.misc.tmp_skin import SkinEnum


class PtxUtl(ABC):
    @staticmethod
    def norm(path: str) -> str:
        return f"default/{path}"

    @staticmethod
    def fun(path: str) -> str:
        pathes = PathUtil.get_list(f"{Dirs.SOUND}/fun/{path}")
        shuffle(pathes)
        return choice(pathes)

    @staticmethod
    def valve(path: str) -> str:
        return f"valve/{path}"

    @staticmethod
    def win(path: str) -> str:
        return f"windows/{path}"

    @staticmethod
    def stalker(path: str) -> str:
        pathes = PathUtil.get_list(f"{Dirs.SOUND}/stalker/{path}")
        shuffle(pathes)
        return choice(pathes)


class Music(Singleton):
    def __init__(self):
        self.CLICK = Sound(PtxUtl.norm("click"))
        self.BACK = Sound(PtxUtl.norm("back"), 3)
        self.SEED = Sound(PtxUtl.norm("seed"), 4)
        self.INTRO = Sound(PtxUtl.norm("intro"))
        self.DEATH = Sound(PtxUtl.norm("death"))
        self.FRUIT = Sound(PtxUtl.norm("eat_fruit"), 4)
        self.GHOST = Sound(PtxUtl.norm("eat_ghost"), 4)
        self.LOSE = Sound(PtxUtl.norm("lose"), 2)
        self.WIN = Sound(PtxUtl.norm("lose"), 2)
        self.FRIGHTENED = Sound(PtxUtl.norm("frightened"), 6)

        self.__reload_sound(False)

    def __set_default(self):
        self.BACK.set(PtxUtl.norm("back"))
        self.SEED.set(PtxUtl.norm("seed"))
        self.INTRO.set(PtxUtl.norm("intro"))
        self.DEATH.set(PtxUtl.norm("death"))
        self.FRUIT.set(PtxUtl.norm("eat_fruit"))
        self.GHOST.set(PtxUtl.norm("eat_ghost"))
        self.LOSE.set(PtxUtl.norm("lose"))
        self.WIN.set(PtxUtl.norm("lose"))
        self.FRIGHTENED.set(PtxUtl.norm("frightened"))

    def update_random_sounds(self):
        if SettingsStorage().fun:
            self.SEED.set(PtxUtl.fun("seed"))
            self.INTRO.set(PtxUtl.fun("intro"))
            self.DEATH.set(PtxUtl.fun("death"))
            self.LOSE.set(PtxUtl.fun("lose"))
            self.WIN.set(PtxUtl.fun("win"))
        elif SkinStorage().equals(SkinEnum.STALKER):
            self.INTRO.set(PtxUtl.stalker("intro"))
            self.DEATH.set(PtxUtl.stalker("death"))
            self.FRUIT.set(PtxUtl.stalker("eat_fruit"))
            self.GHOST.set(PtxUtl.stalker("eat_ghost"))
            self.LOSE.set(PtxUtl.stalker("lose"))
            self.WIN.set(PtxUtl.stalker("win"))

    def __reload_sound(self, with_default: bool = True):
        if with_default:
            self.__set_default()
        self.update_random_sounds()
        if SettingsStorage().fun:
            return
        if SkinStorage().equals(SkinEnum.POKEBALL):
            self.INTRO.set("pokeball/intro")
        elif SkinStorage().equals(SkinEnum.VALVE):
            self.BACK.set(PtxUtl.valve("back"))
            self.SEED.set(PtxUtl.valve("seed"))
            self.INTRO.set(PtxUtl.valve("intro"))
            self.DEATH.set(PtxUtl.valve("death"))
            self.FRUIT.set(PtxUtl.valve("eat_fruit"))
            self.GHOST.set(PtxUtl.valve("eat_ghost"))
            self.FRIGHTENED.set(PtxUtl.valve("frightened"))
        elif SkinStorage().equals(SkinEnum.WINDOWS):
            self.SEED.set(PtxUtl.win("seed"))
            self.INTRO.set(PtxUtl.win("intro"))
            self.DEATH.set(PtxUtl.win("death"))
            self.FRUIT.set(PtxUtl.win("eat_fruit"))
            self.GHOST.set(PtxUtl.win("eat_ghost"))

    def event_handler(self, event: Event):
        if event.type == EvenType.UPDATE_SOUND:
            self.__reload_sound()
