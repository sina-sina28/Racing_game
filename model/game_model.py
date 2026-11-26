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

        self.circuit_names = ("Circuit 1", "Circuit 2")  # 1 Les deux circuits du menu
        self.selected_circuit = 0                        # 1 Au début, on choisit le premier circuit

        self.circuit: Circuit | None = None
        self.car: Car | None = None

        self.car_2: Car | None = None  # 3.1 La deuxième voiture sera créée au départ

    def load_circuit(self) -> None:
        cols = GRID_COLS               # 1 Le premier circuit garde sa largeur de départ
        if self.selected_circuit == 1:
            cols = 12                  # 1 Le deuxième circuit a 12 colonnes

        grid = [
            [RoadTile(col=col, row=row) for col in range(cols)]
            for row in range(GRID_ROWS)
        ]
        self.circuit = Circuit(grid=grid)

        self.checkpoints = {(9, 1), (9, 2)}  # 4.1 Les deux points de passage de la grille de test
        self.visited = {1: set(), 2: set()}  # 4.1 Chaque joueur commence avec zéro point visité
        self.last_checkpoint = {1: None, 2: None}  # 4.1 Au départ, personne n’a atteint de point

        self.finish_tile = (10, 2)  # 4.2 On place l’arrivée sur cette case de test
        self.laps = {1: 0, 2: 0}     # 4.2 Chaque joueur commence à zéro tour

        self.laps_to_win = 3  # 4.3 Sur nos circuits de test, il faut finir 3 tours
        self.winner = None  # 4.3 Au départ, personne n’a gagné

        self.spawn_car()
    def spawn_car(self) -> None:
        self.car = Car(7, 1)
        self.car_2 = Car(7, 2)  # 3.1 J2 démarre une case plus bas que J1

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

    def check_checkpoint(self, player, car):

        if self.winner is not None:
            return               # 4.3 On a déjà un gagnant, la course est finie

        tile = self.circuit.get_tile_at_pixel(car.x, car.y)  # 4.1 On cherche la case sous la voiture
        if tile is None:
            return

        point = (tile.col, tile.row)
        if point in self.checkpoints:
            self.visited[player].add(point)  # 4.1 On garde ce point pour ce joueur
            self.last_checkpoint[player] = point  # 4.1 On retient son dernier point de passage

        elif point == self.finish_tile:
            if self.visited[player] == self.checkpoints:
                self.laps[player] += 1         # 4.2 Le joueur a vu tous les points, il gagne un tour
                self.visited[player].clear()   # 4.2 Il doit repasser par les points au tour suivant

                if self.laps[player] >= self.laps_to_win:
                    self.winner = player             # 4.3 On garde le numéro du gagnant
                    self.state = GameState.FINISHED  # 4.3 Les voitures s’arrêtent

    def update(self) -> None:
        """Met à jour le jeu pendant la course : terrain sous la voiture, puis physique."""
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.update_car_terrain(self.car)  # D'abord le terrain, pour que la physique l'utilise
        self.car.update_position()

        self.update_car_terrain(self.car_2)  # 3.1 On regarde le terrain sous J2
        self.car_2.update_position()  # 3.1 On déplace aussi la deuxième voiture

        self.check_checkpoint(1, self.car)  # 4.1 On vérifie où J1 vient d’arriver
        self.check_checkpoint(2, self.car_2)  # 4.1 On fait pareil pour J2



