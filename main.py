import pygame
from controller.game_controller import GameController



def main():
    pygame.init()

    from pathlib import Path
    pygame.mixer.music.load(str(Path(__file__).resolve().parent / "assets" / "music" / "Menu principale.mp3"))  # 5.3 Je charge la musique du menu
    pygame.mixer.music.play(-1)                          # 5.3 Je la joue en boucle

    pygame.display.set_caption("Projet Python - Jeu de course 2D")

    controller = GameController()
    controller.run()

    pygame.quit()


if __name__ == "__main__":
    main()

