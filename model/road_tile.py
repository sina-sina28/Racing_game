import pygame

from constants import TILE_SIZE
from model.terrain import RoadTerrain


class RoadTile:
    """Une case contenant un terrain et éventuellement un bloc spécial."""

    BLOCK_COLORS = {
        "P1": (40, 120, 235),
        "P2": (230, 65, 75),
        "C1": (165, 75, 220),
        "C2": (165, 75, 220),
        "F": (230, 55, 55),
        "B1": (250, 210, 35),
        "B2": (250, 210, 35),
    }

    def __init__(self, col, row, terrain=None, block=None):

        self.col = col
        self.row = row

        self.terrain = terrain if terrain is not None else RoadTerrain()

        self.block = block

        self.sprite = None

    def get_sprite(self, tile_size=TILE_SIZE):

        if self.sprite is not None and self.sprite.get_size() == (tile_size, tile_size):
            return self.sprite

        surface = pygame.Surface((tile_size, tile_size))

        # Display the terrain colour.
        surface.fill(self.terrain.color)

        # Draw the grid border.
        pygame.draw.rect(
            surface,
            (35, 35, 40),
            surface.get_rect(),
            1
        )

        # Display a special block if one exists.
        if self.block is not None:

            marker_color = self.BLOCK_COLORS.get(
                self.block.label,
                (235, 235, 235)
            )

            marker_rect = surface.get_rect().inflate(-12, -12)

            pygame.draw.rect(
                surface,
                marker_color,
                marker_rect,
                border_radius=5
            )

            font = pygame.font.SysFont(
                "Arial",
                max(14, tile_size // 4),
                bold=True
            )

            label = font.render(
                self.block.label,
                True,
                (15, 15, 15)
            )

            surface.blit(
                label,
                label.get_rect(center=surface.get_rect().center)
            )

        self.sprite = surface

        return self.sprite