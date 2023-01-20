import pygame
from typing import Tuple, Dict
import random

from utils.Sprites import SpriteHandler, Sprite
from utils.ImagesHandler import ImgCon

def checkCollisions(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    return (a_x + a_width > b_x) and (a_x < b_x + b_width) and (a_y + a_height > b_y) and (a_y < b_y + b_height)

class Entity:
    x: float
    y: float

    def getPos(self):
        return self.x, self.y

    def draw(self, surface: pygame.Surface):
        pass

    def update(self, surface: pygame.Surface, delta_time: float):
        pass

class TextEntity(Entity):
    renderedText: pygame.Surface

    def __init__(self, x: float, y: float, text: pygame.Surface):
        self.x = x
        self.y = y
        self.renderedText = text

    def draw(self, surface: pygame.Surface):
        surface.blit(self.renderedText, self.getPos())

class ImageEntity(Entity):
    image: pygame.Surface

    def __init__(self, x: float, y: float, image: pygame.Surface):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.getPos())

class ButtonEntitiy(Entity):
    renderedText: pygame.Surface
    rect: pygame.rect.Rect
    color: Tuple

    def __init__(self, x: float, y: float, text: pygame.Surface, color: Tuple):
        self.x = x
        self.y = y
        self.width = text.get_width()+20
        self.height = text.get_height()+20

        self.renderedText = text
        self.color = color

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height), 2)
        surface.blit(self.renderedText, (self.x+10, self.y+10))

class AnimatedEntity(Entity):
    sprite: Sprite
    animation_time: float

    def __init__(self, x: float, y: float, spritesheet: pygame.Surface, sprite_width: int, animation_time: float):
        self.x = x
        self.y = y
        self.sprite = Sprite(SpriteHandler(spritesheet).sprite_row(pygame.Rect((0, 0, sprite_width, sprite_width)), 1))

        self.animation_time = animation_time
        self.current_time = 0

    def _update_time_dependent(self, dt):
        """Updates the Sprite per the given animation time in the constructor."""

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.sprite.nextSprite()

class BackgroundGoober(AnimatedEntity):
    def __init__(self, x: float, y: float, spritesheet: pygame.Surface):
        super().__init__(x=x, y=y, spritesheet=spritesheet, sprite_width=120, animation_time=3)

        self.MIDPOINT_Y = y - self.sprite.getSprite().get_height() / 2
        self.START_X = x - self.sprite.getSprite().get_width() / 2

        self.directionX = 0.6
        self.directionY = 0.4

    def draw(self, surface: pygame.Surface):
        surface.blit(self.sprite.getSprite(), self.getPos())

    def update(self, surface: pygame.Surface, delta_time: float):
        self._update_time_dependent(delta_time)

        # Moving on Y-Axis
        self.y += (self.directionY * delta_time)
        if self.y < self.MIDPOINT_Y-70:
            self.y = self.MIDPOINT_Y-70
            self.directionY = random.randint(6, 12)/10
        elif self.y > self.MIDPOINT_Y+70:
            self.y = self.MIDPOINT_Y+70
            self.directionY = -random.randint(6, 12)/10

        # Moving on X-Axis
        self.x = self.x + (self.directionX * delta_time)
        if self.x > self.START_X+70:
            self.x = self.START_X+70
            self.directionX = -random.randint(6, 12)/10
        elif self.x < self.START_X-70:
            self.x = self.START_X-70
            self.directionX = random.randint(6, 12)/10

class PlayerEntity(AnimatedEntity):
    lasers: Dict[int, ImageEntity]

    def __init__(self, x: float, y: float, image: pygame.Surface):
        super().__init__(x, y, image, 120, 3)

        self.max_speed = 20
        self.acceleration = 4
        self.speedX = 0
        self.speedY = 0

        self.lasers = {}

        self.sleebing = False

    def draw(self, surface: pygame.Surface):
        surface.blit(self.sprite.getSprite(), self.getPos())

    def update(self, surface: pygame.Surface, delta_time: float):
        self._update_time_dependent(delta_time)

        self.x += self.speedX
        self.y += self.speedY
        if self.x > surface.get_width()-self.sprite.getSprite().get_width():
            self.x = surface.get_width()-self.sprite.getSprite().get_width()
        elif self.x < 0:
            self.x = 0

        if self.y > surface.get_height()-self.sprite.getSprite().get_height():
            self.y = surface.get_height()-self.sprite.getSprite().get_height()
        elif self.y < 0:
            self.y = 0

        for laser in self.lasers.copy().values():
            laser.update(surface, delta_time)
            laser.draw(surface)

    def move(self, x, y):
        self.speedX += x
        self.speedY += y

    def shootLaser(self):
        _id = random.randint(0, 500)
        self.lasers[_id] = PlayerAttack(self, self.x + self.sprite.getSprite().get_width(), self.y + self.sprite.getSprite().get_height() / 2, ImgCon.makeImage(ImgCon.LASER), _id)

    def markForDeletion(self, _id):
        if not self.lasers.get(_id):
            return
        del self.lasers[_id]

class PlayerAttack(ImageEntity):
    def __init__(self, player: PlayerEntity, x: float, y: float, image: pygame.Surface, _id: int):
        super().__init__(x, y, image)

        self.player = player
        self.ID = _id

    def update(self, surface: pygame.Surface, delta_time: float):
        self.x += 15*delta_time

        if self.x > surface.get_width():
            self.player.markForDeletion(self.ID)

class ProgressBar(Entity):
    border: pygame.rect.Rect
    outerColor: Tuple
    innerColor: Tuple

    def __init__(self, x: float, y: float, outer_color: Tuple, inner_color: Tuple, max_val: float, outer_rect: pygame.rect.Rect, direction: str = "width"):
        self.x = x
        self.y = y

        self.outerColor = outer_color
        self.innerColor = inner_color

        self.cur_val = 0 # Always starts at 0.
        self.max_val = max_val

        self.border = outer_rect

        self.direction = direction

    def _calc_inner_rect(self) -> float:
        """Note: This only calculates the width of the inner rectangle."""
        if self.direction == "width":
            width = (self.border.width / 100) * ((self.cur_val / self.max_val) * 100)
            return width if width <= self.border.width else self.border.width
        else:
            height = (self.border.height / 100) * ((self.cur_val / self.max_val) * 100)
            return height if height <= self.border.height else self.border.height

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.outerColor, self.border, 2)
        if self.direction == "width":
            pygame.draw.rect(surface, self.innerColor, pygame.Rect(self.x+2, self.y+2, self._calc_inner_rect()-4, self.border.height-4))
        else:
            pygame.draw.rect(surface, self.innerColor, pygame.Rect(self.x + 2, self.y + 2, self.border.width - 4, self._calc_inner_rect() - 4))

class TypeWriter(Entity):
    def __init__(self, _display: pygame.Surface, y: float, text: str, font: pygame.font.Font, color: Tuple, delay_betweeen_letters: float = 20):
        self.DISPLAY = _display
        self.y = y

        self.currentText = text
        self.textIndex = 1 # Starts at one

        self.FONT = font
        self.color = color
        self.letter_delay = delay_betweeen_letters
        self.current_time = 0

    def setNewText(self, text: str):
        self.currentText = text
        self.textIndex = 0

    def _get_text(self) -> str:
        return self.currentText[0:self.textIndex]

    def get_width_height(self) -> Tuple:
        rendered = self.FONT.render(self._get_text(), True, self.color)
        return rendered.get_width(), rendered.get_height()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.FONT.render(self._get_text(), True, self.color), (self.DISPLAY.get_width()/2-self.get_width_height()[0]/2, self.y))

    def update(self, surface: pygame.Surface, delta_time: float):
        self.current_time += delta_time

        if self.current_time >= self.letter_delay:
            if not self.textIndex == len(self.currentText):
                self.textIndex += 1
            self.current_time = 0