import pygame

class ImgCon:
    ICON = "res/gfx/resicon.png"
    ICON_MED = "res/gfx/medicon-removebg.png"

    GOOBERT_SPRITESHEET = "res/gfx/spritesheets/spacey_goobert_spritesheet.bmp"
    GOOBERT_SLEEBING = "res/gfx/spacey_goobert_sleebing.png"

    LASER = "res/gfx/laser.png"

    # - Stars
    BIG_ICE_STAR = "res/gfx/background/stars/big_ice_star.png"
    SMOL_PURPLE_STAR = "res/gfx/background/stars/smol_purple_star.png"
    SMOL_STAR_ONE = "res/gfx/background/stars/smol_star_one.png"
    STAR_FADING_PURPLE = "res/gfx/background/stars/star_fading_purple.png"
    STAR_FADING_PURPLE_BIG = "res/gfx/background/stars/star_fading_purple_big.png"

    # - Planets
    CUTE_PURPLE_PLANET = "res/gfx/background/planets/cute_purple_planet.png"
    SMILING_COLORFUL_PLANET = "res/gfx/background/planets/smiling_colorful_planet.png"

    # - Meteors
    PURPLE_METEOR = "res/gfx/background/meteors/purple_meteor_cut.png"

    @staticmethod
    def makeImage(image_file: str) -> pygame.Surface:
        return pygame.image.load(image_file)