from typing import Dict, List, Union
import pygame
from utils.Entities import Entity
from utils.Background import Background
from utils.enemies import EnemyHandler

class GameState:
    """Defines a Game State. Requires the `game` object and an ID. Needs to be Entered into the GameStateHandler."""
    ID: str
    entitiyQueue: List[Union[Entity, Background, EnemyHandler]] = []

    def __init__(self, game):
        self.game = game
        self.entitiyQueue = []

    def gameLoop(self) -> str:
        pass

    def interactionHandler(self):
        """Handles interactions like keyboard input or mouse input."""
        pass

    def queueAdd(self, to_add: list):
        """Adds Entities to the entity queue."""
        self.entitiyQueue += to_add

    def drawEntities(self, surface: pygame.Surface):
        for entitiy in self.entitiyQueue:
            entitiy.draw(surface)

    def updateEntities(self, surface: pygame.Surface, delta_time: float):
        for entity in self.entitiyQueue:
            entity.update(surface, delta_time)

    def _clearState(self):
        pass

class GameStateHandler:
    currentState: GameState
    gameStates: Dict[str, GameState]

    def __init__(self, game, states: Dict[str, GameState], current_state: str):

        for _id, state in states.items():
            states[_id] = state

        self.game = game

        self.gameStates = {} | states
        # self.currentState = self.gameStates.get(current_state)
        self.currentState = self.setCurrentState(current_state)

    def getGameState(self):
        return self.currentState

    def setCurrentState(self, state_id: str):
        self.currentState = self.gameStates.copy()[state_id](self.game)
        # self.currentState = self.gameStates.get(state_id)
        return self.currentState