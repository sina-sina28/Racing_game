import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel


class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.CIRCUIT_SELECTION:
            self._draw_circuit_selection(model)                # 1 On affiche les deux circuits
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))


    def _draw_circuit_selection(self, model: GameModel) -> None:
        """Affiche les deux circuits et montre lequel est choisi."""
        cx = WINDOW_WIDTH // 2                                          # 1 On prend le milieu de l’écran

        title = self.font.render("Choix du circuit", True, COLOR_ACCENT)
        self.screen.blit(title, title.get_rect(center=(cx, 160)))

        for index, name in enumerate(model.circuit_names):
            selected = index == model.selected_circuit                   # 1 On regarde si ce circuit est choisi
            color = COLOR_ACCENT if selected else COLOR_TEXT

            rect = pygame.Rect(cx - 140, 280 + index * 65, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)

            if selected:
                pygame.draw.rect(self.screen, color, rect, 2, border_radius=8)  # 1 On encadre le circuit choisi

            label = self.font.render(name, True, color)
            self.screen.blit(label, label.get_rect(center=rect.center))

        hint = self.font.render(
            "↑ ↓ Choisir   Entrée Valider   Échap Retour",
            True,
            COLOR_TEXT,
        )
        self.screen.blit(hint, hint.get_rect(center=(cx, 480)))

    def _draw_racing(self, model: GameModel) -> None:

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        if model.circuit is None:
            return
        surf, rect = model.car.get_rotated_sprite()
        self.screen.blit(surf, rect)
