import pygame
from utils.Entities import ImageEntity
from random import randint, choice
from typing import Dict, Union, List

class Star(ImageEntity):
    ID: int

    def __init__(self, background, _id: int, x: float, y: float, image: pygame.Surface):
        super(Star, self).__init__(x=x, y=y, image=image)

        self.BACKGROUND = background
        self.ID = _id

        self.move_by = randint(50, 100) / 2

    def update(self, surface: pygame.Surface, delta_time: float):

        self.x = self.x - (self.move_by * delta_time)

        if self.x < -self.image.get_width():
            self.BACKGROUND.mark_for_deletion(self.ID)

class Background:
    objectsDict: Dict[int, Union[Star]] = {}
    starList: List[pygame.Surface]

    def __init__(self, star_images: List[pygame.Surface], animation_time: float = 5):
        self.starList = star_images

        self.animation_time = animation_time
        self.current_time = 0

    def mark_for_deletion(self, _id: int):
        if not self.objectsDict.get(_id):
            return
        del self.objectsDict[_id]

    def draw(self, surface: pygame.Surface):
        for entity in self.objectsDict.copy().values():
            entity.draw(surface)

    def update(self, surface: pygame.Surface, delta_time: float):
        for entitiy in self.objectsDict.copy().values():
            entitiy.update(surface, delta_time)

        self.current_time += delta_time
        if self.current_time >= self.animation_time:
            self.current_time = 0
            new_star = self._new_star(surface)
            self.objectsDict[new_star.ID] = new_star

    def _new_star(self, surface: pygame.Surface) -> Star:
        star_image = choice(self.starList)

        return Star(background=self, _id=randint(0, 500), x=surface.get_width()+star_image.get_width(), y=randint(0, surface.get_height()), image=star_image)