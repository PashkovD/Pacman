from enum import Enum

from pacman.misc.skins import Skin


class SkinEnum(Enum):
    DEFAULT = Skin("default", {})
    EDGE = Skin("edge", {0: 12, 1: 5})
    POKEBALL = Skin("pokeball", {2: 12, 3: 5})
    WINDOWS = Skin("windows", {3: 12, 4: 5})
    HALF_LIFE = Skin("half_life", {4: 12, 5: 5})
    CHROME = Skin("chrome", {5: 12, 6: 5})