import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler
from controller.input_handler import InputHandler, MAPPING_J1   # 3.1 ajouter mapping de joueur1

class GameController:

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)

        self.input_j1 = InputHandler(MAPPING_J1)  # 3.1 Les lettres pour J1
        self.input_j2 = InputHandler()            # 3.1 Les flèches pour J2

        self.running = True

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:

        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)

        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.CIRCUIT_SELECTION:  # 1 Gere les touches de l’ecran de selection
            self.handle_circuit_selection_key(key)

        elif state == GameState.RACING:
            if key == pygame.K_ESCAPE:
                self.model.state = GameState.PAUSED  # 2 Échap met la course en pause

            elif key == pygame.K_SPACE:  # 3.3 J1 appuie sur Espace pour utiliser son objet
                print("J1 : commande objet")
            elif key == pygame.K_RETURN:  # 3.3 J2 appuie sur Entrée pour utiliser son objet
                print("J2 : commande objet")

        elif state == GameState.PAUSED:
            if key == pygame.K_ESCAPE:
                self.model.state = GameState.RACING  # 2 Échap reprend la course
            elif key == pygame.K_m:
                self.model.state = GameState.MENU  # 2 M revient au menu

        elif state == GameState.FINISHED and key == pygame.K_m:
            self.model.state = GameState.MENU        # 5.2 Après la victoire, M ramène au menu

    def handle_menu_key(self, key: int) -> None:
        if key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT_SELECTION  # 1 Entree ouvre le choix du circuit
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_circuit_selection_key(self, key: int) -> None:
        """Gère les touches pendant le choix du circuit."""
        if key == pygame.K_UP and self.model.selected_circuit > 0:
            self.model.selected_circuit -= 1  # 1 Sélectionne le circuit précédent
        elif key == pygame.K_DOWN:
            last_index = len(self.model.circuit_names) - 1  # 1 Indice du dernier circuit
            if self.model.selected_circuit < last_index:
                self.model.selected_circuit += 1  # 1 Sélectionne le circuit suivant
        elif key == pygame.K_RETURN:
            self.model.load_circuit()  # 1 Charge le circuit choisi
            self.model.state = GameState.RACING  # 1 Lance la course
        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU  # 1 Revient au menu principal

    def update(self) -> None:
        if self.model.state != GameState.RACING:
            return

        self.apply_input(self.model.car, self.input_j1.get_inputs())  # 3.1 J1 contrôle sa voiture
        self.apply_input(self.model.car_2, self.input_j2.get_inputs())  # 3.1 J2 contrôle la sienne
        
        self.model.update()

    def apply_input(self, car, player_input) -> None:
        """Transmet les actions du joueur à sa voiture."""
        if player_input['accelerate']:
            car.accelerate()
        if player_input['brake']:
            car.brake()
        if player_input['turn_left']:
            car.turn_left()
        if player_input['turn_right']:
            car.turn_right()

    def render(self) -> None:
        self.view.draw(self.model)

    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()
