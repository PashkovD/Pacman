from random import randint

import pygame as pg

from misc import Font
from objects import Text, ButtonController, Button
from scenes import Base


class Scene(Base.Scene):
    __data = [
        "Архипов Евгений",
        "Смирнов Андрей",
        "Грачев Егор",
        "Александров Даниил",
        "Егоров Александр",
        "Сергеев Сергей",
        "Бурдонов Арсений",
        "Игнатов Иван",
        "Лещенко Вячеcлав",
        "Полиехов Андрей",
        "Акимов Денис",
        "Богомолов Алексей",
        "Вартанян Владимир",
        "Дмитрий Пашков",
        "Киселева Алиса",
        "Николайчев Павел",
        "Оркин Родион",
        "Плоцкий Богдан",
        "Татаринов Игорь",
        "Терпунов Артём",
        "Тимченко Савелий",
        "Щеников Иван",
        "Хаяо Миядзаки",
        "Джонатан Джостар",
        "Тору Иватани",
        "Фил Спенсер",
        "☭",
        "Польская корова",
        "Хирохико Араки"
    ]

    def __init__(self, game) -> None:
        super().__init__(game)
        self.game = game
        self.__on_screen = 0
        self.start_pos = -30
        self.__speed = 0.3
        self.__alpha_delta = -15
        self.__students = []
        self.__students2 = self.__data.copy()

    def create_objects(self) -> None:
        self.__create_buttons()

    def __create_buttons(self) -> None:
        self.__back_button = Button(self.game, pg.Rect(0, 0, 180, 40),
                                    self.__start_menu, 'MENU', center=(self.game.width // 2, 250),
                                    text_size=Font.BUTTON_TEXT_SIZE)
        self.__button_controller = ButtonController(self.game, [self.__back_button])
        self.objects.append(self.__button_controller)

    def __get_random_student_y(self) -> int:
        return randint(25, self.game.height - 75)

    def __create_student(self) -> None:
        students = list(set(self.__students2) - set((obj.text for obj in self.__students)))
        label = str(students[randint(0, len(students) - 1)])
        self.__students2.pop(self.__students2.index(label))
        student = Text(self.game, label, Font.CREDITS_SCENE_SIZE, font=Font.DEFAULT)

        is_student_y_correct = False
        tries = 0
        while not is_student_y_correct:
            student.move_center(self.start_pos, randint(25, self.game.height - 75))

            is_student_y_correct = True
            for student2 in self.__students:
                if abs(student.rect.centery - student2.rect.centery) <= \
                    (student.rect.height + student2.rect.height) / 2:
                    is_student_y_correct = False
                    break

            tries += 1

            if tries > 100:
                break

        student.speed = self.__speed + randint(-5, 15) / 100
        student.ttl = 0
        self.__students.append(student)
        self.objects.append(student)
        self.__on_screen += 1

    def on_activate(self) -> None:
        self.create_objects()
        self.__button_controller.reset_state()

    def __process_students(self) -> None:
        students_to_delete = []

        for index, student in enumerate(self.__students):
            if student.rect.x >= self.game.width:
                students_to_delete.append(index)
                self.__on_screen -= 1
            elif student.rect.x != -105:
                student.ttl += 1
                student.move(student.ttl * student.speed + self.start_pos, student.rect.y)
                student.surface.set_alpha(
                    min(
                        255,
                        self.game.width - (
                            (
                                student.rect.midbottom[0] - self.game.width // 2
                            )
                            ** 2 * 0.06 - self.__alpha_delta
                        )
                    )
                )

        for index in sorted(students_to_delete, reverse=True):
            self.objects.remove(self.__students[index])
            del self.__students[index]

    def additional_logic(self) -> None:
        if len(self.__students2) == 0:
            self.__students2 = self.__data.copy()
        elif len(self.__students) == len(self.__students2) and not self.__on_screen:
            self.__students.clear()
        elif pg.time.get_ticks() % 190 == 0 and not len(self.__students) == len(self.__students2):
            self.__create_student()
        self.__process_students()

    def additional_event_check(self, event: pg.event.Event) -> None:
        if self.game.current_scene == self:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.__start_menu()

    def __start_menu(self) -> None:
        self.game.set_scene(self.game.scenes.MENU)
        self.__on_screen = 0
        self.__students = []
        self.objects = []