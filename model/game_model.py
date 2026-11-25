from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU

        self.circuit_names = ("Circuit 1", "Circuit 2")  # 1 Les deux circuits du menu
        self.selected_circuit = 0                        # 1 Au début, on choisit le premier circuit

        self.circuit: Circuit | None = None
        self.car: Car | None = None

    def load_circuit(self) -> None:
        cols = GRID_COLS               # 1 Le premier circuit garde sa largeur de départ
        if self.selected_circuit == 1:
            cols = 12                  # 1 Le deuxième circuit a 12 colonnes

        grid = [
            [RoadTile(col=col, row=row) for col in range(cols)]
            for row in range(GRID_ROWS)
        ]
        self.circuit = Circuit(grid=grid)
        self.spawn_car()
    def spawn_car(self) -> None:
        self.car = Car(7, 1)

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update_position()
