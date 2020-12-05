import pygame as pg
import random

from misc import LevelLoader, CELL_SIZE, Font, get_path, Health
from objects import SeedContainer, Map, ImageObject, Text, Pacman
from objects.ghosts import *
from scenes import base
from objects.fruits import Fruit
from misc import Sounds, Maps


class Scene(base.Scene):
    intro_sound = Sounds.INTRO
    pacman_channel = pg.mixer.Channel(0)
    intro_channel = pg.mixer.Channel(1)
    gameover_channel = pg.mixer.Channel(2)
    siren_channel = pg.mixer.Channel(3)

    def create_static_objects(self):
        self.__load_from_map()
        self.__create_sounds()
        self.__create_static_text()
        self.__create_start_anim()
        self.__create_hud()
        self.__create_health()
        self.__pre_init()
        self.create_objects()

    def __pre_init(self):
        self.__timer_reset_pacman = 0
        self.__seeds_eaten = 0
        self.__max_seeds_eaten_to_prefered_ghost = 7
        self.__work_ghost_counters = True
        self.__first_run_ghost = True
        self.fruit = Fruit(self.game, self.__fruit_position)

    def __create_health(self):
        self.hp = Health(3, 3)
        self.__hp_hud = []
        self.__prepare_lives_meter()

    def __create_static_text(self):
        self.__scores_label_text = Text(
            self.game, 'SCORE', Font.MAIN_SCENE_SIZE, rect=pg.Rect(10, 0, 20, 20)
        )

        self.__high_scores_label_text = Text(
            self.game, 'HIGHSCORE', Font.MAIN_SCENE_SIZE, rect=pg.Rect(130, 0, 20, 20)
        )
        self.static_object.append(self.__scores_label_text)
        self.static_object.append(self.__high_scores_label_text)

    def __load_from_map(self):
        self.__loader = LevelLoader(Maps.levels[self.game.level_id])
        self.__map_data = self.__loader.get_map_data()
        self.__seed_data = self.__loader.get_seed_data()
        self.__energizer_data = self.__loader.get_energizer_data()
        self.__movements_data = self.__loader.get_movements_data()
        self.__player_position = self.__loader.get_player_position()
        self.__ghost_positions = self.__loader.get_ghost_positions()
        self.__fruit_position = self.__loader.get_fruit_position()
        self.__map = Map(self.game, self.__map_data)

    def __prepare_lives_meter(self) -> None:
        self.__hp_hud = []
        for i in range(int(self.hp)):
            hp_image = ImageObject(self.game, get_path('1', 'png', 'images', 'pacman', 'walk'), (5 + i * 20, 270))
            hp_image.rotate(180)
            self.__hp_hud.append(hp_image)

    def __create_sounds(self):
        self.timer = 0
        self.intro_sound = pg.mixer.Sound(random.choice(Sounds.INTRO))
        self.intro_sound.set_volume(0.5)

    def __create_start_anim(self):
        self.text = ['READY', 'GO!']
        for i in range(2):
            self.text[i] = Text(self.game, self.text[i], 30, font=Font.TITLE, rect=pg.Rect(20, 0, 20, 20))
            self.text[i].move_center(self.game.width // 2, self.game.height // 2)
            self.text[i].surface.set_alpha(0)
            self.static_object.append(self.text[i])
        self.state_text = 1

    def create_objects(self) -> None:
        self.objects = []
        self.siren_channel.unpause()
        #self.text[len(self.text)-1].surface.set_alpha(0)
        self.__create_map()
        self.__create_ghost()

        self.objects.append(self.fruit)
        self.pacman = Pacman(self.game, self.__player_position)
        self.objects.append(self.pacman)

    def __create_map(self):
        self.__seeds = SeedContainer(self.game, self.__seed_data, self.__energizer_data)
        self.objects.append(self.__map)
        self.objects.append(self.__seeds)

    def __create_ghost(self):
        self.blinky = Blinky(self.game, self.__ghost_positions[3])
        self.pinky = Pinky(self.game, self.__ghost_positions[1])
        self.inky = Inky(self.game, self.__ghost_positions[0])
        self.clyde = Clyde(self.game, self.__ghost_positions[2])

        self.__ghosts = [
            self.blinky,
            self.pinky,
            self.inky,
            self.clyde
        ]

        self.__not_prefered_ghosts = self.__ghosts.copy()
        self.__prefered_ghost = self.pinky
        self.__count_prefered_ghost = 0

        for ghost in self.__ghosts:
            self.objects.append(ghost)
            self.objects.append(ghost.gg_text)

    def __create_hud(self):
        self.__high_scores_value_text = Text(self.game, str(self.game.records.data[-1]), Font.MAIN_SCENE_SIZE,
                                             rect=pg.Rect(130, 8, 20, 20))
        self.static_object.append(self.__high_scores_value_text)

        self.__scores_value_text = Text(
            self.game, str(self.game.score), Font.MAIN_SCENE_SIZE, rect=pg.Rect(10, 8, 20, 20))
        self.static_object.append(self.__scores_value_text)

    @property
    def movements_data(self):
        return self.__movements_data

    def additional_event_check(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.mixer.pause()
            self.game.scenes.set(self.game.scenes.PAUSE)

    def __change_prefered_ghost(self) -> None:
        self.__count_prefered_ghost += 1
        self.__not_prefered_ghosts.pop(0)
        if self.__count_prefered_ghost < 4:
            self.__prefered_ghost = self.__ghosts[self.__count_prefered_ghost]
        else:
            self.__prefered_ghost = None
            self.__count_prefered_ghost = 0

    def __process_collision(self) -> None:
        self.fruit.process_collision(self.pacman)
        seed_eaten = self.__seeds.process_collision(self.pacman)
        for ghost in self.__ghosts:
            if ghost.collision_check(self.pacman)[0]:
                if ghost.collision_check(self.pacman)[1]:
                    self.__timer_reset_pacman = pg.time.get_ticks()
                    if not self.pacman.dead:
                        self.game.sounds.pacman1.play()
                        self.siren_channel.pause()
                        self.pacman.death()
                        self.__prepare_lives_meter()
                    for ghost2 in self.__ghosts:
                        ghost2.invisible()
                else:
                    if ghost.mode == 'Frightened':
                        ghost.gg_text.text = str(200 * 2 ** self.game.score.fear_count)
                        self.game.score.eat_ghost()
                    ghost.toggle_mode_to_eaten()

        if seed_eaten == 1:
            if self.__prefered_ghost is not None and self.__work_ghost_counters:
                self.__prefered_ghost.counter()
                self.__prefered_ghost.update_timer()
            elif not self.__work_ghost_counters and self.__prefered_ghost is not None:
                self.__seeds_eaten += 1
                self.__prefered_ghost.update_timer()
        elif seed_eaten == 2:
            self.game.score.activate_fear_mode()
            for ghost in self.__ghosts:
                ghost.toggle_mode_to_frightened()

    def __start_label(self) -> None:
        current_time = pg.time.get_ticks() / 1000
        if pg.time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.state_text *= -1
        if self.state_text == 1:
            if current_time - self.timer < self.intro_sound.get_length() / 4 * 3:
                self.text[0].surface.set_alpha(255)
            else:
                self.text[0].surface.set_alpha(0)
                self.text[1].surface.set_alpha(255)
        else:
            if current_time - self.timer < self.intro_sound.get_length() / 4 * 3:
                self.text[0].surface.set_alpha(0)
            else:
                self.text[1].surface.set_alpha(0)

    def __play_music(self):
        if not self.siren_channel.get_busy():
            self.siren_channel.play(Sounds.SIREN)

    def process_logic(self) -> None:
        if not self.intro_channel.get_busy():
            if self.pacman.dead_anim.anim_finished and int(self.hp) < 1:
                self.pacman_channel.stop()
                self.gameover_channel.play(Sounds.GAMEOVER)
                self.game.scenes.set(self.game.scenes.GAMEOVER)
            super(Scene, self).process_logic()
            self.__play_music()
            self.__process_collision()
            if pg.time.get_ticks() - self.__timer_reset_pacman >= 3000 and self.pacman.animator.anim_finished:
                self.create_objects()
                self.__seeds_eaten = 0
                self.__work_ghost_counters = False
                self.__max_seeds_eaten_to_prefered_ghost = 7
                for ghost in self.__ghosts:
                    ghost.work_counter = False
            if self.__seeds_eaten == self.__max_seeds_eaten_to_prefered_ghost and self.__prefered_ghost is not None:
                self.__prefered_ghost.is_can_leave_home = True
                if self.__max_seeds_eaten_to_prefered_ghost == 7:
                    self.__max_seeds_eaten_to_prefered_ghost = 17
                elif self.__max_seeds_eaten_to_prefered_ghost == 17:
                    self.__max_seeds_eaten_to_prefered_ghost = 32

            if self.__seeds.is_field_empty():
                self.gameover_channel.play(Sounds.GAMEOVER)
                self.game.scenes.set(self.game.scenes.ENDGAME, reset=True)
        else:
            self.__start_label()
            self.inky.update_timer()
        if self.__prefered_ghost is not None and self.__prefered_ghost.can_leave_home():
            self.__change_prefered_ghost()
        if self.__prefered_ghost is not None and self.__prefered_ghost.can_leave_home():
            self.__change_prefered_ghost()
        for ghost in self.__not_prefered_ghosts:
            if ghost != self.__prefered_ghost:
                ghost.update_timer()

    def additional_draw(self) -> None:
        super().additional_draw()
        for hp in self.__hp_hud:
            hp.process_draw()

    def additional_logic(self) -> None:
        self.__scores_value_text.text = str(self.game.score)
        self.__prepare_lives_meter()

    def on_activate(self) -> None:
        self.intro_channel.unpause()
        if self.pacman.animator != self.pacman.dead_anim:
            self.siren_channel.unpause()
        if self.pacman.animator == self.pacman.dead_anim:
            self.pacman_channel.unpause()

    def on_reset(self) -> None:
        pg.mixer.stop()
        self.game.score.reset()
        self.game.scenes.MAIN.recreate()
        self.timer = pg.time.get_ticks() / 1000
        self.intro_channel.play(self.intro_sound)
