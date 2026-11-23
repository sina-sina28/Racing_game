import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE,
    CAR_BRAKE, CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED, CAR_FRICTION
)



class Car:
    """Voiture d'un joueur : position, vitesse, angle et déplacement sur le circuit."""

    def __init__(self, start_col: int, start_row: int):
        """Crée une voiture à l'arrêt, au centre de la case de départ.

        Args:
            start_col: colonne de la case de départ.
            start_row: ligne de la case de départ.
        """
        # Position du centre de la voiture, en pixels
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0               # En pixels par frame, négative en marche arrière
        self.angle: float = 0.0               # Orientation en degrés
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        """Augmente la vitesse de la voiture (appelée à chaque frame où l'on accélère)."""
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
        """Crée l'image de la voiture : un rectangle rouge aux coins arrondis.

        Returns:
            Une surface transparente de taille CAR_WIDTH x CAR_HEIGHT.
        """
        # SRCALPHA : le fond est transparent, seuls les pixels dessinés sont visibles (Dans notre cas, les coins sont invisibles sinon ils apparaîtraient en noir).
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Renvoie l'image tournée selon l'angle de la voiture, et sa position à l'écran.

        Returns:
            L'image tournée et le rectangle où la dessiner, centré sur (x, y).
        """
        # pygame tourne dans le sens inverse des aiguilles d'une montre,
        # d'où le signe moins : un angle positif tourne vers la droite
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        # L'image tournée est plus grande : on la recentre pour qu'elle ne "saute" pas
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
