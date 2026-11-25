WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.07          # Accélération vers l'avant

CAR_BRAKE = 0.1                  # Force du frein
CAR_REVERSE_ACCELERATION = 0.05  # Marche arrière : 2 fois plus douce que le frein, environ 70 % de l'accélération avant
CAR_MAX_SPEED = 6.0              # Vitesse maximale en avant (pixels par frame)
CAR_MAX_REVERSE_SPEED = 2.5      # Vitesse maximale en arrière, plus faible qu'en avant
CAR_FRICTION = 0.02              # Ralentissement naturel quand on n'appuie sur rien

CAR_WIDTH = 30
CAR_HEIGHT = 50

CAR_MAX_STEERING = 30.0   # Braquage maximal des roues (degrés)
CAR_STEER_STEP = 4.0      # Braquage ajouté à chaque frame où l'on tourne
CAR_STEER_RETURN = 2.0    # Retour du volant vers le centre à chaque frame
CAR_TURN_FACTOR = 0.015   # Lien entre vitesse x braquage et rotation de la voiture

# --- Dérapage ---
CAR_DRIFT_REALIGN = 0.05     # Vitesse de réalignement pendant un dérapage (multipliée par la traction)
CAR_DRIFT_END_ANGLE = 5.0    # Écart (degrés) sous lequel le dérapage peut s'arrêter
CAR_MIN_DRIFT_SPEED = 0.2    # Sous cette vitesse, la voiture arrête de déraper

# --- Terrain par défaut (route), en attendant les cases de B ---
DEFAULT_TRACTION = 1.0              # Facilité à accélérer et freiner
DEFAULT_SEUIL_DERAPAGE = 150.0      # Vitesse x braquage au-delà duquel on dérape
DEFAULT_FROTTEMENT_DERAPAGE = 0.05  # Part de la vitesse perdue à chaque frame en dérapage

# --- Boost ---
CAR_BOOST_DURATION = 90        # Durée du boost en frames (1,5 s à 60 FPS)
CAR_BOOST_ACCELERATION = 0.15  # Poussée en plus à chaque frame pendant le boost
CAR_BOOST_MAX_SPEED = 9.0      # Vitesse max pendant le boost (6.0 sans boost)
CAR_BOOST_FADE = 0.1           # Perte de vitesse par frame après le boost, jusqu'à la vitesse max normale

class GameState:
    MENU = "menu"
    RACING = "racing"
    CIRCUIT_SELECTION = "circuit_selection"  # 1 Le joueur choisit son circuit avant la course
    PAUSED = "paused"                        # 2 Le jeu est en pause
# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)

