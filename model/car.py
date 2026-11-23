import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE,
    CAR_BRAKE, CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED, CAR_FRICTION
)



class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        self.speed += CAR_ACCELERATION

    def brake(self) -> None:
        """Freine la voiture, puis la fait reculer une fois arrêtée."""
        # Une seule méthode suffit : si la vitesse passe sous 0, la voiture recule
        self.speed -= CAR_BRAKE        

    def update_position(self) -> None:
        """Met à jour la vitesse (frottement, limites) puis déplace la voiture."""
        self.apply_friction()
        self.limit_speed()
        self.y += self.speed  # Pour l'instant, la voiture ne bouge que verticalement

    def apply_friction(self) -> None:
        """Ramène doucement la vitesse vers 0 quand on n'accélère pas."""
        if self.speed > 0:
            # max(0) : évite que la voiture se mette à reculer toute seule
            self.speed = max(0.0, self.speed - CAR_FRICTION)
        elif self.speed < 0:
            # min(0) : évite que la voiture se mette à avancer toute seule
            self.speed = min(0.0, self.speed + CAR_FRICTION)

    def limit_speed(self) -> None:
        """Garde la vitesse entre la vitesse max en arrière et en avant."""
        self.speed = max(-CAR_MAX_REVERSE_SPEED, min(self.speed, CAR_MAX_SPEED))


    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
