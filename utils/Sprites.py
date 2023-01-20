import pygame
from typing import Tuple, List

class SpriteHandler:
    """Warning: All Sprites in Sprite Sheets given to the Sprite Handler must be identical squares."""
    spriteSheet: pygame.Surface

    def __init__(self, sprite_sheet: pygame.Surface):
        self.spriteSheet = sprite_sheet

    def image_at(self, rectangle: Tuple) -> pygame.Surface:
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.spriteSheet, (0, 0), rect)
        image.set_colorkey(image.get_at((0, 0)), pygame.RLEACCEL)

        return image

    def sprite_row(self, rect_base: pygame.Rect, row: int) -> List[pygame.Surface]:
        GETTER_Y = (rect_base.height * row) - rect_base.height
        POS_X = 0

        sprite_list = []

        while POS_X < self.spriteSheet.get_width() and POS_X + rect_base.width <= self.spriteSheet.get_width():
            sprite_list.append(self.image_at((POS_X, GETTER_Y, rect_base.width, rect_base.height)))
            POS_X += rect_base.width

        return sprite_list

class Sprite:
    sprite_list: List[pygame.Surface]

    def __init__(self, sprite_list: List[pygame.Surface]):
        self.sprite_list = sprite_list
        self.currentSprite = 0

    def getSprite(self):
        return self.sprite_list[self.currentSprite]

    def nextSprite(self):
        self.currentSprite = (self.currentSprite + 1) % len(self.sprite_list)

        return self.getSprite()