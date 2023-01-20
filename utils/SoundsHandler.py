import pygame

class Sounds:
    """NOTICE: All sounds need to be either ogg audio files or uncompressed wav audio files."""
    SPLASH_BOOP = r"res\sfx\splashboop.wav"
    LASER = r"res\sfx\laser.wav"

    @staticmethod
    def makeSound(sound_file: str) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(sound_file)

    @staticmethod
    def playSound(sound: pygame.mixer.Sound):
        pygame.mixer.Sound.play(sound)