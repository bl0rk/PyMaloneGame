import pygame

from utils.ImagesHandler import ImgCon

class Game:
    screen: pygame.Surface
    gameRunning: bool

    def __init__(self):
        pygame.init()
        pygame.display.set_icon(ImgCon.makeImage(ImgCon.ICON))
        pygame.display.set_caption("Quest to Sierra-22b")

        self.screen = pygame.display.set_mode((1000, 700))

        from utils.GameStateHandler import GameStateHandler
        from GameStates import SplashScreen, MainMenu, MainGame, Sleeby, EndScreen, Introduction

        self.gameRunning = True

        self.gameStateHandler = GameStateHandler(self, {
            SplashScreen.ID: SplashScreen,
            MainMenu.ID: MainMenu,
            Introduction.ID: Introduction,
            MainGame.ID: MainGame,
            Sleeby.ID: Sleeby,
            EndScreen.ID: EndScreen,
        }, SplashScreen.ID)

        self.gameLoop()

    def gameLoop(self):
        _next = self.gameStateHandler.getGameState().gameLoop()
        while self.gameRunning:
            _next = self.gameStateHandler.setCurrentState(_next).gameLoop()
            if not _next:
                self.gameRunning = False