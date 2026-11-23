WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.05

CAR_BRAKE = 0.1              # Force du frein, qui sert aussi pour la marche arrière
CAR_MAX_SPEED = 6.0          # Vitesse maximale en avant (pixels par frame)
CAR_MAX_REVERSE_SPEED = 2.5  # Vitesse maximale en arrière, plus faible qu'en avant
CAR_FRICTION = 0.02          # Ralentissement naturel quand on n'appuie sur rien

CAR_WIDTH = 30
CAR_HEIGHT = 50


class GameState:
    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
