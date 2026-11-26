import pygame


MAPPING = {
    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:   "brake",  # Flèche du bas : freiner / reculer
    pygame.K_LEFT:   "turn_left",   # Braquer à gauche
    pygame.K_RIGHT:  "turn_right",  # Braquer à droite
}

MAPPING_J1 = {
    pygame.K_z: "accelerate",  # 3.1 J1 avance avec Z ou W
    pygame.K_w: "accelerate",
    pygame.K_s: "brake",
    pygame.K_q: "turn_left",  # 3.1 J1 tourne à gauche avec Q ou A
    pygame.K_a: "turn_left",
    pygame.K_d: "turn_right",
}

class InputHandler:

    def __init__(self, mapping=MAPPING):
        self.mapping = mapping  # 3.1 Chaque joueur utilise ses propres touches
        
    def get_inputs(self) -> dict:
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
