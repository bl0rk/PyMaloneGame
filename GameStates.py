import pygame, sys, time
from pygame.locals import *

from utils.GameStateHandler import *
from utils.ImagesHandler import ImgCon
from utils.SoundsHandler import Sounds
from utils.ColorConstants import ColorCons
from utils.Fonts import Fonts
from utils.Entities import TextEntity, ButtonEntitiy, BackgroundGoober, PlayerEntity, ImageEntity, ProgressBar, TypeWriter, checkCollisions
from utils.Background import Background
from utils.enemies import EnemyHandler

class SplashScreen(GameState):
    ID: str = "SPLASH_SCREEN"

    def __init__(self, _game):
        super().__init__(_game)

    def gameLoop(self):
        DISPLAY = self.game.screen
        timer = 0
        last_time = time.time()

        renMes = Fonts.MAIN_FONT_MEDIUM.render("A Game by blorky dorky.", True, ColorCons.GREEN_COLOR)
        startMessage = TextEntity(DISPLAY.get_width()/2 - renMes.get_width()/2, DISPLAY.get_height() + renMes.get_height(), renMes)

        textMinHeight = ((DISPLAY.get_height()/3)*2) - (startMessage.renderedText.get_height()/2+75)

        increaseHeightBy = textMinHeight / 50

        while timer < 200:
            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            timer += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            DISPLAY.fill(ColorCons.MAIN_SCREEN_COLOR)
            tempImage = ImgCon.makeImage(ImgCon.ICON_MED)
            DISPLAY.blit(tempImage.copy(), (DISPLAY.get_width()/2 - tempImage.get_width()/2, DISPLAY.get_height()/2 - tempImage.get_height()))
            del tempImage

            if startMessage.y <= textMinHeight:
                startMessage.y = textMinHeight

            if startMessage.y > textMinHeight:
                startMessage.y -= increaseHeightBy * dt
                if not startMessage.y >= textMinHeight:
                    Sounds.playSound(Sounds.makeSound(Sounds.SPLASH_BOOP))

            DISPLAY.blit(startMessage.renderedText, startMessage.getPos())

            pygame.display.update()

        return MainMenu.ID

class MainMenu(GameState):
    ID: str = "MAIN_MENU"

    def __init__(self, game):
        super().__init__(game)

    def gameLoop(self):
        DISPLAY = self.game.screen
        last_time = time.time()

        self.queueAdd([ # Background Elements.
            Background(star_images=[
                ImgCon.makeImage(ImgCon.BIG_ICE_STAR),
                ImgCon.makeImage(ImgCon.SMOL_PURPLE_STAR),
                ImgCon.makeImage(ImgCon.SMOL_STAR_ONE),
                ImgCon.makeImage(ImgCon.STAR_FADING_PURPLE),
                ImgCon.makeImage(ImgCon.STAR_FADING_PURPLE_BIG)
            ]),
            BackgroundGoober(DISPLAY.get_width() / 2, DISPLAY.get_height() / 2, ImgCon.makeImage(ImgCon.GOOBERT_SPRITESHEET))
        ])

        tempText = Fonts.MAIN_FONT_MEDIUM.render("Start game :3", True, ColorCons.PINK)
        tempText2 = Fonts.PILOTC_HI_LARGE.render("Sierra-22b", True, ColorCons.GREEN_COLOR)
        tempText3 = Fonts.MAIN_FONT_SMALL.render("Beta-Version: 0.1", True, ColorCons.GREEN_COLOR)
        tempText4 = Fonts.MAIN_FONT_SMALL.render("(For malone my dear cutie <3)", True, ColorCons.GREEN_COLOR)

        START_BUTTON = ButtonEntitiy(DISPLAY.get_width()/2-tempText.get_width()/2-10, DISPLAY.get_height()/3-tempText.get_height()/2-10, tempText.copy(), ColorCons.GREEN_COLOR)

        self.queueAdd([ # Text and Buttons.
            START_BUTTON,
            TextEntity(DISPLAY.get_width()/2-tempText2.get_width()/2, DISPLAY.get_height()/8-tempText2.get_height()/2, tempText2.copy()),
            TextEntity(0, DISPLAY.get_height()-tempText3.get_height(), tempText3.copy()),
            TextEntity(DISPLAY.get_width()/2+5-tempText4.get_width()/2, DISPLAY.get_height()/4.3-tempText4.get_height()/2, tempText4.copy())
        ])

        del tempText, tempText2, tempText3, tempText4

        while self.game.gameRunning:
            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if checkCollisions(START_BUTTON.x, START_BUTTON.y, START_BUTTON.width, START_BUTTON.height, mouseX, mouseY, 3, 3):
                        return Introduction.ID

            DISPLAY.fill(ColorCons.MAIN_GAME_BACKGROUND)

            self.updateEntities(DISPLAY, dt)

            self.drawEntities(DISPLAY)

            pygame.display.update()

            pygame.time.delay(10)

class MainGame(GameState):
    ID: str = "MAIN_GAME"

    def __init__(self, game):
        super().__init__(game)

    def playerControlling(self, player: PlayerEntity, event: pygame.event.Event, dt: float):
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                player.move(0, -player.acceleration)
            if event.key == K_s:
                player.move(0, player.acceleration)

            if event.key == K_a:
                player.move(-player.acceleration, 0)
            if event.key == K_d:
                player.move(player.acceleration, 0)

            if event.key == K_SPACE:
                player.shootLaser()
                laser_sound = Sounds.makeSound(Sounds.LASER)
                laser_sound.set_volume(0.3)
                Sounds.playSound(laser_sound)

        if event.type == pygame.KEYUP:
            if event.key == K_w:
                player.move(0, player.acceleration)
            if event.key == K_s:
                player.move(0, -player.acceleration)

            if event.key == K_a:
                player.move(player.acceleration, 0)
            if event.key == K_d:
                player.move(-player.acceleration, 0)

    def gameLoop(self): # Somehow inherits the entityQueue from MainMenu.
        DISPLAY = self.game.screen
        last_time = time.time()

        self.queueAdd([ # Background
            Background(star_images=[
                ImgCon.makeImage(ImgCon.BIG_ICE_STAR),
                ImgCon.makeImage(ImgCon.SMOL_PURPLE_STAR),
                ImgCon.makeImage(ImgCon.SMOL_STAR_ONE),
                ImgCon.makeImage(ImgCon.STAR_FADING_PURPLE),
                ImgCon.makeImage(ImgCon.STAR_FADING_PURPLE_BIG)
            ], animation_time=3)
        ])

        GOOBERT_SPRITESHEET = ImgCon.makeImage(ImgCon.GOOBERT_SPRITESHEET)
        player = PlayerEntity(x=DISPLAY.get_width()/4-GOOBERT_SPRITESHEET.get_width()/6, # GOOBERT_SPRITESHEETS has 6 sprites.
                              y=DISPLAY.get_height()/2-GOOBERT_SPRITESHEET.get_height(), # GOOBERT_SPRITESHEETS has one row.
                              image=GOOBERT_SPRITESHEET.copy())

        enemyHandler = EnemyHandler(player)

        self.queueAdd([ # Main Gameplay elements.
            enemyHandler,
            player
        ])

        outerOne = pygame.rect.Rect(DISPLAY.get_width()-25, DISPLAY.get_height()/4, 25, 250)

        progress_to_sierra = ProgressBar(DISPLAY.get_width()-25, DISPLAY.get_height()/4, ColorCons.DARK_BLUE, ColorCons.PURPLE, 500, outerOne, "height")

        self.queueAdd([ # Display elements.
            progress_to_sierra
        ])

        gameTimePassed = 0

        while self.game.gameRunning:
            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            gameTimePassed += dt
            progress_to_sierra.cur_val = gameTimePassed / 15

            if progress_to_sierra.cur_val >= progress_to_sierra.max_val:
                return EndScreen.ID

            if player.sleebing:
                return Sleeby.ID

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.playerControlling(player, event, dt)

            for _id, enemy in enemyHandler.enemyList.copy().items():
                for laser in player.lasers.copy().values():
                    if checkCollisions(laser.x, laser.y, laser.image.get_width(), laser.image.get_height(), enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height()):
                        enemyHandler.mark_for_deletion(_id)
                        player.markForDeletion(laser.ID)

            DISPLAY.fill(ColorCons.MAIN_GAME_BACKGROUND)

            self.updateEntities(DISPLAY, dt)

            self.drawEntities(DISPLAY)

            pygame.display.update()

            pygame.time.delay(10)

class Sleeby(GameState):
    ID: str = "SLEEBY_STATE"

    def __init__(self, game):
        super().__init__(game)

    def gameLoop(self):
        DISPLAY = self.game.screen
        last_time = time.time()

        SLEEBY_GOOBERT = ImgCon.makeImage(ImgCon.GOOBERT_SLEEBING)
        sleeby_goober = ImageEntity(DISPLAY.get_width() / 2 - SLEEBY_GOOBERT.get_width() / 2,
                                    DISPLAY.get_height() / 2 - SLEEBY_GOOBERT.get_height() / 2,
                                    SLEEBY_GOOBERT)

        tempText = Fonts.MAIN_FONT_MEDIUM.render("Uh Oh! Seems like the cutie fell asleep...", True, ColorCons.GREEN_COLOR)
        tempText2 = Fonts.MAIN_FONT_SMALL.render("Return to Main Menu (don't wake the goober)", True, ColorCons.PINK)

        return_button = ButtonEntitiy(DISPLAY.get_width()/2 - tempText2.get_width()/2, DISPLAY.get_height()/4*3 - tempText2.get_height()/2, tempText2, ColorCons.GREEN_COLOR)

        self.queueAdd([
            Background(star_images=[
                ImgCon.makeImage(ImgCon.BIG_ICE_STAR),
                ImgCon.makeImage(ImgCon.SMOL_PURPLE_STAR),
                ImgCon.makeImage(ImgCon.SMOL_STAR_ONE),
                ImgCon.makeImage(ImgCon.STAR_FADING_PURPLE),
                ImgCon.makeImage(ImgCon.STAR_FADING_PURPLE_BIG)
            ], animation_time=7),
            sleeby_goober,
            TextEntity(DISPLAY.get_width()/2-tempText.get_width()/2, DISPLAY.get_height()/4-tempText.get_height()/2, tempText.copy()),
            return_button
        ])

        del tempText

        while self.game.gameRunning:
            dt = time.time() - last_time
            dt *= 30
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if checkCollisions(return_button.x, return_button.y, return_button.width, return_button.height, mouseX, mouseY, 3, 3):
                        return MainMenu.ID

            DISPLAY.fill(ColorCons.MAIN_GAME_BACKGROUND)

            self.updateEntities(DISPLAY, dt)

            self.drawEntities(DISPLAY)

            pygame.display.update()

            pygame.time.delay(10)

class EndScreen(GameState):
    ID: str = "END_SCREEN"

    def __init__(self, game):
        super().__init__(game)

    def gameLoop(self) -> str:
        DISPLAY = self.game.screen
        last_time = time.time()

        typeWriter = TypeWriter(DISPLAY, 0, "The (short) Journey nears it's end...", Fonts.MAIN_FONT_MEDIUM, ColorCons.GREEN_COLOR, 5)
        typeWriter.y = DISPLAY.get_height()/2-typeWriter.get_width_height()[1]/2

        dummi_player = PlayerEntity(DISPLAY.get_width() / 2 - 120, DISPLAY.get_height() / 2 - 120, ImgCon.makeImage(ImgCon.GOOBERT_SPRITESHEET))

        self.queueAdd([
            Background(star_images=[
                ImgCon.makeImage(ImgCon.BIG_ICE_STAR),
                ImgCon.makeImage(ImgCon.SMOL_PURPLE_STAR),
                ImgCon.makeImage(ImgCon.SMOL_STAR_ONE),
                ImgCon.makeImage(ImgCon.STAR_FADING_PURPLE),
                ImgCon.makeImage(ImgCon.STAR_FADING_PURPLE_BIG)
            ], animation_time=15),
            dummi_player,
            typeWriter
        ])

        toWriteText = [
            "Our little Goobert will finally arrive...",
            "Sierra-22b, the world of comfort is not far away now.",
            "Whatever will await our dear goober, we will see.",
            "But finally, he is at rest, comfy, happy.",
            "As he deserves.",
            ". . . . .",
            "- Well, this most likely wasn't a long Journey for you. -",
            "- But for me, this was quite an experience and i'm happy i've had it. -",
            "- The fact this is a gift only makes it better. -",
            "- hope you had fun <3 -",
            "...",
            "- Log End -",
            "..."
        ]

        while self.game.gameRunning:
            dt = time.time() - last_time
            dt *= 30
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if len(typeWriter.currentText) == typeWriter.textIndex:
                if not toWriteText:
                    return MainMenu.ID
                typeWriter.setNewText(toWriteText.pop(0))

            DISPLAY.fill((0, 0, 0))

            self.updateEntities(DISPLAY, dt)

            self.drawEntities(DISPLAY)

            pygame.display.update()

            pygame.time.delay(10)

        return MainMenu.ID

class Introduction(GameState):
    ID: str = "INTRODUCTION"

    def __init__(self, game):
        super().__init__(game)

    def gameLoop(self) -> str:
        DISPLAY = self.game.screen
        last_time = time.time()

        tempButtonText = Fonts.MAIN_FONT_MEDIUM.render("- Start Game -", True, ColorCons.PINK)

        startGameButton = ButtonEntitiy(DISPLAY.get_width()/2-tempButtonText.get_width()/2, DISPLAY.get_height()/4*3-tempButtonText.get_height()/2,
                                        tempButtonText.copy(), ColorCons.GREEN_COLOR)

        tempTexts = [
            Fonts.MAIN_FONT_MEDIUM.render("- Introduction -", True, ColorCons.GREEN_COLOR),
            Fonts.MAIN_FONT_MEDIUM.render("The space cat named goobert has an >Important< Mission!", True, ColorCons.GREEN_COLOR),
            Fonts.MAIN_FONT_MEDIUM.render("With earth having been left cold, dead and uncomfy-", True, ColorCons.GREEN_COLOR),
            Fonts.MAIN_FONT_MEDIUM.render("Goobert has made himself on his way to the floorpida system-", True, ColorCons.GREEN_COLOR),
            Fonts.MAIN_FONT_MEDIUM.render("And most importantly the most comfiest planet that resides within!", True, ColorCons.GREEN_COLOR),
            Fonts.MAIN_FONT_MEDIUM.render("- SIERRA-22B -", True, ColorCons.GREEN_COLOR),
            Fonts.MAIN_FONT_MEDIUM.render("----- | -----", True, ColorCons.GREEN_COLOR),
            Fonts.MAIN_FONT_SMALL.render("(Controls: W;A;S;D movement, _SPACE_ shooting.)", True, ColorCons.GREEN_COLOR),
            Fonts.MAIN_FONT_SMALL.render("Survive until you reach Sierra.", True, ColorCons.GREEN_COLOR)
        ]

        to_add = []
        POS_Y = 20
        _height = tempTexts[0].get_height()+10
        for text in tempTexts:
            to_add.append(TextEntity(DISPLAY.get_width()/2-text.get_width()/2, POS_Y, text))
            POS_Y += _height

        to_add.append(startGameButton)
        self.queueAdd(to_add)

        del tempButtonText, tempTexts, to_add, POS_Y, _height

        while self.game.gameRunning:
            dt = time.time() - last_time
            dt *= 30
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if checkCollisions(startGameButton.x, startGameButton.y, startGameButton.width, startGameButton.height, mouseX, mouseY, 3, 3):
                        return MainGame.ID

            DISPLAY.fill((0, 0, 0))

            self.updateEntities(DISPLAY, dt)

            self.drawEntities(DISPLAY)

            pygame.display.update()

            pygame.time.delay(10)