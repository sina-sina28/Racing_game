from constants import (
    GameState, GRID_ROWS, GRID_COLS,
    DEFAULT_TRACTION, DEFAULT_SEUIL_DERAPAGE, DEFAULT_FROTTEMENT_DERAPAGE
)
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.car: Car | None = None

    def load_circuit(self) -> None:
        grid = [[RoadTile(col=col_idx, row=row_idx)
                for row_idx in range(GRID_COLS)] for col_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        self.car = Car(7, 1)

    def update_car_terrain(self, car: Car) -> None:
        """Donne à la voiture les propriétés du terrain de la case sous elle."""
        tile = self.circuit.get_tile_at_pixel(car.x, car.y)
        if tile is None:
            return  # Hors de la carte, c'est le vide : géré par la partie circuit (B)
        # getattr : tant que les cases n'ont pas de terrain, on garde les valeurs de la route
        car.set_terrain(
            getattr(tile, "traction", DEFAULT_TRACTION),
            getattr(tile, "seuil_derapage", DEFAULT_SEUIL_DERAPAGE),
            getattr(tile, "frottement_derapage", DEFAULT_FROTTEMENT_DERAPAGE),
        )

    def update(self) -> None:
        """Met à jour le jeu pendant la course : terrain sous la voiture, puis physique."""
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.update_car_terrain(self.car)  # D'abord le terrain, pour que la physique l'utilise
        self.car.update_position()
