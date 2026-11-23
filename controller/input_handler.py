import pygame


MAPPING = {
    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:   "brake",  # Flèche du bas : freiner / reculer
    pygame.K_LEFT:   "turn_left",   # Braquer à gauche
    pygame.K_RIGHT:  "turn_right",  # Braquer à droite
}


class InputHandler:

    def __init__(self):
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
