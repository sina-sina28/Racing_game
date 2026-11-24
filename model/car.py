import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE,
    CAR_BRAKE,CAR_REVERSE_ACCELERATION, CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED, CAR_FRICTION,
    CAR_MAX_STEERING, CAR_STEER_STEP, CAR_STEER_RETURN, CAR_TURN_FACTOR,
    CAR_DRIFT_REALIGN, CAR_DRIFT_END_ANGLE, CAR_MIN_DRIFT_SPEED,
    DEFAULT_TRACTION, DEFAULT_SEUIL_DERAPAGE, DEFAULT_FROTTEMENT_DERAPAGE
)


class Car:
    """Voiture d'un joueur : position, vitesse, orientation, adhérence et dérapage."""

    def __init__(self, start_col: int, start_row: int):
        """Crée une voiture à l'arrêt, au centre de la case de départ.

        Args:
            start_col: colonne de la case de départ.
            start_row: ligne de la case de départ.
        """
        # Position du centre de la voiture, en pixels
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        # Vitesse réelle à l'écran (pixels par frame), séparée de l'orientation
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.angle: float = 0.0     # Orientation en degrés : 0 = vers la droite, augmente vers la gauche
        self.steering: float = 0.0  # Braquage des roues en degrés : positif = à gauche
        self.throttle: float = 0.0  # Accélération demandée pendant cette frame (négative = frein)
        self.is_drifting: bool = False  # État de l'automate : False = ADHÈRE, True = DÉRAPE
        # Propriétés du terrain sous la voiture (route par défaut)
        self.traction: float = DEFAULT_TRACTION
        self.seuil_derapage: float = DEFAULT_SEUIL_DERAPAGE
        self.frottement_derapage: float = DEFAULT_FROTTEMENT_DERAPAGE
        self.sprite = self.build_sprite()

    # --- Commandes du joueur ---

    def accelerate(self) -> None:
        """Demande une accélération vers l'avant pour cette frame."""
        self.throttle = CAR_ACCELERATION

    def brake(self) -> None:
        """Freine si la voiture avance, sinon accélère en marche arrière."""
        if self.get_speed() > 0:
            self.throttle = -CAR_BRAKE  # Freiner : effet fort
        else:
            # Reculer : aussi doux que l'accélération avant, et non pas avec la force du frein
            self.throttle = -CAR_REVERSE_ACCELERATION

    def turn_left(self) -> None:
        """Tourne les roues vers la gauche (augmente le braquage)."""
        self.steering += CAR_STEER_STEP

    def turn_right(self) -> None:
        """Tourne les roues vers la droite (diminue le braquage)."""
        self.steering -= CAR_STEER_STEP

    # --- Passer du repère de l'écran au repère de la voiture ---

    def forward_vector(self) -> tuple[float, float]:
        """Renvoie le vecteur de longueur 1 qui pointe vers l'avant de la voiture."""
        rad = math.radians(self.angle)
        return math.cos(rad), -math.sin(rad)  # Moins : y augmente vers le bas de l'écran

    def left_vector(self) -> tuple[float, float]:
        """Renvoie le vecteur de longueur 1 qui pointe vers la gauche de la voiture."""
        rad = math.radians(self.angle)
        return -math.sin(rad), -math.cos(rad)

    def local_velocity(self) -> tuple[float, float]:
        """Découpe la vitesse en une partie vers l'avant et une partie sur le côté.

        Returns:
            (v_long, v_lat) : vitesse vers l'avant, et vitesse de glissade vers la gauche.
        """
        fx, fy = self.forward_vector()
        lx, ly = self.left_vector()
        # Produit scalaire : la part de la vitesse dans chaque direction
        return self.vx * fx + self.vy * fy, self.vx * lx + self.vy * ly

    def set_local_velocity(self, v_long: float, v_lat: float) -> None:
        """Reconstruit vx et vy à partir des parties avant et latérale."""
        fx, fy = self.forward_vector()
        lx, ly = self.left_vector()
        self.vx = v_long * fx + v_lat * lx
        self.vy = v_long * fy + v_lat * ly

# --- Physique, appelée à chaque frame ---

    def set_terrain(self, traction: float, seuil_derapage: float,
                        frottement_derapage: float) -> None:
            """Met à jour les propriétés du terrain sous la voiture (appelée à chaque frame)."""
            self.traction = traction
            self.seuil_derapage = seuil_derapage
            self.frottement_derapage = frottement_derapage
    
    def reset_at(self, x: float, y: float) -> None:
            """Replace la voiture à l'arrêt à une position donnée (utilisé pour le vide)."""
            self.x, self.y = x, y
            self.vx = self.vy = 0.0  # vitesse/braquage nulle aprés téleportation
            self.steering = 0.0
            self.is_drifting = False

    def update_position(self) -> None:
        """Une frame de physique : volant, accélération, rotation, adhérence, déplacement."""
        self.update_steering()
        self.apply_throttle()
        self.rotate()
        self.update_drift_state()
        self.apply_grip_or_drift()
        self.x += self.vx
        self.y += self.vy

    def apply_throttle(self) -> None:
        """Applique l'accélération demandée, réduite selon la traction du terrain."""
        v_long, v_lat = self.local_velocity()
        v_long += self.throttle * self.traction
        self.throttle = 0.0  # Remis à 0 : sans touche à la prochaine frame, pas d'accélération
        self.set_local_velocity(v_long, v_lat)

    def rotate(self) -> None:
        """Tourne la voiture selon sa vitesse et son braquage.

        Seule l'orientation change : la vitesse (vx, vy) garde sa direction.
        C'est cet écart qui permettra le dérapage.
        """
        v_long, _ = self.local_velocity()
        # Vitesse négative (marche arrière) : la voiture tourne dans l'autre sens
        self.angle = (self.angle + v_long * self.steering * CAR_TURN_FACTOR) % 360
    
    def update_drift_state(self) -> None:
        """Automate de la voiture : passe de ADHÈRE à DÉRAPE, et inversement."""
        v_long, v_lat = self.local_velocity()
        # Tourner trop fort pour sa vitesse, par rapport à ce que permet le terrain
        turning_too_hard = abs(v_long * self.steering) > self.seuil_derapage

        if not self.is_drifting:
            if turning_too_hard:
                self.is_drifting = True
        else:
            # Écart (degrés) entre la direction du mouvement et l'orientation
            slip = math.degrees(math.atan2(abs(v_lat), abs(v_long)))
            realigned = slip < CAR_DRIFT_END_ANGLE and not turning_too_hard
            almost_stopped = math.hypot(v_long, v_lat) < CAR_MIN_DRIFT_SPEED
            if realigned or almost_stopped:
                self.is_drifting = False

    def apply_grip_or_drift(self) -> None:
        """Applique le comportement de l'état actuel : ADHÈRE ou DÉRAPE."""
        v_long, v_lat = self.local_velocity()
        if self.is_drifting:
            # La glissade diminue peu à peu, plus lentement si la traction est faible
            v_lat *= 1 - CAR_DRIFT_REALIGN * self.traction
            # Frottement du terrain pendant la glissade (fort sur route, presque nul sur glace)
            v_long *= 1 - self.frottement_derapage
            v_lat *= 1 - self.frottement_derapage
        else:
            v_lat = 0.0  # Adhère : la voiture va là où elle pointe
        v_long = self.apply_air_friction(v_long)
        v_long = self.limit_speed(v_long)
        self.set_local_velocity(v_long, v_lat)

    def apply_air_friction(self, v_long: float) -> float:
        """Frottement de l'air : ramène doucement la vitesse vers 0."""
        if v_long > 0:
            # max(0) : évite que la voiture se mette à reculer toute seule
            return max(0.0, v_long - CAR_FRICTION)
        if v_long < 0:
            return min(0.0, v_long + CAR_FRICTION)
        return 0.0

    def limit_speed(self, v_long: float) -> float:
        """Garde la vitesse entre la vitesse max en arrière et en avant."""
        return max(-CAR_MAX_REVERSE_SPEED, min(v_long, CAR_MAX_SPEED))

    def update_steering(self) -> None:
        """Ramène le volant vers le centre et limite le braquage."""
        if self.steering > 0:
            # max(0) : le volant s'arrête au centre au lieu de partir de l'autre côté
            self.steering = max(0.0, self.steering - CAR_STEER_RETURN)
        elif self.steering < 0:
            self.steering = min(0.0, self.steering + CAR_STEER_RETURN)
        self.steering = max(-CAR_MAX_STEERING, min(self.steering, CAR_MAX_STEERING))

    # --- Image de la voiture ---

    def build_sprite(self) -> pygame.Surface:
        """Crée l'image de la voiture, tournée vers la droite (angle 0).

        Returns:
            Une surface transparente de taille CAR_HEIGHT x CAR_WIDTH.
        """
        # La voiture regarde vers la droite : sa longueur (CAR_HEIGHT) est sur l'axe x
        surf = pygame.Surface((CAR_HEIGHT, CAR_WIDTH), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_HEIGHT, CAR_WIDTH), border_radius=5)
        # Bande jaune à l'avant, pour voir dans quel sens la voiture pointe
        pygame.draw.rect(surf, (255, 220, 0), (CAR_HEIGHT - 10, 4, 6, CAR_WIDTH - 8))
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Renvoie l'image tournée selon l'angle de la voiture, et sa position à l'écran.

        Returns:
            L'image tournée et le rectangle où la dessiner, centré sur (x, y).
        """
        # pygame tourne dans le sens inverse des aiguilles d'une montre,
        # comme notre convention : pas besoin de signe moins
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        # L'image tournée est plus grande : on la recentre pour qu'elle ne "saute" pas
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
