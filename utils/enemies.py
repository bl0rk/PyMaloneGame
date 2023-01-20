import pygame
from utils.Entities import ImageEntity, checkCollisions, PlayerEntity
from typing import Dict
from random import randint, choice
from utils.ImagesHandler import ImgCon

class EnemyAttack(ImageEntity):
    def __init__(self, handler, x: float, y: float, image: pygame.Surface, speed: float, position: pygame.math.Vector2, _id: int):
        super().__init__(x, y, image)

        self.HANDLER = handler
        self.ID = _id

        self.SPEED = speed
        self.POSITION = position

    def update(self, surface: pygame.Surface, delta_time: float):
        self.POSITION += self.SPEED*delta_time

        self.x = int(self.POSITION.x)
        self.y = int(self.POSITION.y)

        if not checkCollisions(0, 0, surface.get_width(), surface.get_height(), self.x, self.y, self.image.get_width(), self.image.get_height()):
            self.HANDLER.delete_attack(self.ID)

        PLAYER = self.HANDLER.player

        if checkCollisions(PLAYER.x, PLAYER.y, PLAYER.sprite.getSprite().get_width(), PLAYER.sprite.getSprite().get_height(), self.x, self.y, self.image.get_width(), self.image.get_height()):
            PLAYER.sleebing = True
            self.HANDLER.delete_attack(self.ID)

class Enemy(ImageEntity):
    def __init__(self, handler, x: float, y: float, image: pygame.Surface, _id: int):
        super().__init__(x, y, image)

        self.HANDLER = handler
        self.ID = _id

        self.attack_time = 50
        self.attack_current_time = 0

        self.max_distance = 0

    def update(self, surface: pygame.Surface, delta_time: float):
        if not self.max_distance:
            self.max_distance = randint(int(surface.get_width()/4*2), int(surface.get_width()/4*3))

        if self.x > self.max_distance:
            self.x -= 20*delta_time

        self.attack_current_time += delta_time
        if self.attack_current_time >= self.attack_time:
            self.attack_current_time = 0
            self.attackPlayer()

        if checkCollisions(self.HANDLER.player.x, self.HANDLER.player.y, self.HANDLER.player.sprite.getSprite().get_width(), self.HANDLER.player.sprite.getSprite().get_height(),
                           self.x, self.y, self.image.get_width(), self.image.get_height()):
            self.HANDLER.player.sleebing = True
            self.HANDLER.mark_for_deletion(self.ID)

    def attackPlayer(self):
        PLAYER_POS = self.HANDLER.player.getPos()
        START = pygame.math.Vector2((self.x+(self.image.get_width()/2), self.y+(self.image.get_height()/2)))

        DISTANCE = PLAYER_POS - START

        position = pygame.math.Vector2(START)

        SPEED = 10

        _speed = DISTANCE.normalize() * SPEED

        ID = randint(0, 200)

        self.HANDLER.enemyAttackList[ID] = EnemyAttack(handler=self.HANDLER, x=position.x,
                                                       y=position.y, image=pygame.transform.scale(ImgCon.makeImage(ImgCon.PURPLE_METEOR), (50, 50)),
                                                       speed=_speed, position=position, _id=ID)

class EnemyHandler:
    enemyList: Dict[int, Enemy]
    enemyAttackList: Dict[int, EnemyAttack]

    def __init__(self, player: PlayerEntity):
        self.spawnEnemies = True

        self.animation_time = 100
        self.current_time = 0

        self.player = player

        self.enemyList = {}
        self.enemyAttackList = {}

    def draw(self, surface: pygame.Surface):
        for enemy in self.enemyList.copy().values():
            enemy.draw(surface)

        for attack in self.enemyAttackList.copy().values():
            attack.draw(surface)

    def update(self, surface: pygame.Surface, delta_time: float):
        for enemy in self.enemyList.copy().values():
            enemy.update(surface, delta_time)

        for attack in self.enemyAttackList.copy().values():
            attack.update(surface, delta_time)

        if not self.spawnEnemies: return

        self.current_time += delta_time
        if self.current_time >= self.animation_time:
            self.current_time = 0
            if len(self.enemyList.copy().values()) > 6: # Hard capacity on allowed enemies.
                return

            new_enemy = self._spawn(surface)
            self.enemyList[new_enemy.ID] = new_enemy

    def _spawn(self, surface: pygame.Surface) -> Enemy:
        image = choice([ImgCon.makeImage(ImgCon.CUTE_PURPLE_PLANET), ImgCon.makeImage(ImgCon.SMILING_COLORFUL_PLANET)])

        return Enemy(handler=self, x=surface.get_width(), y=randint(0, surface.get_height()-140), image=pygame.transform.scale(image, (160, 140)), _id=randint(0, 200))

    def mark_for_deletion(self, _id):
        if not self.enemyList.get(_id):
            return
        del self.enemyList[_id]

    def delete_attack(self, _id):
        if not self.enemyAttackList.get(_id):
            return
        del self.enemyAttackList[_id]