from constants import GameState

from model.car import Car
from model.circuit import Circuit

from model.blocks import (
    CheckpointBlock,
    FinishBlock,
    BoostBlock
)

from model.terrain import VoidTerrain


class GameModel:
    """Gère les joueurs, les terrains et le déroulement de la course."""

    def __init__(self):

        self.state = GameState.MENU

        self.circuit_names = (
            "Circuit 1 - Easy",
            "Circuit 2 - Intermediate",
            "Circuit 3 - Hard"
        )

        self.selected_circuit = 0

        self.circuit = None

        # ------------------------------------------
        # DEUX JOUEURS
        # ------------------------------------------

        self.car = None
        self.car_2 = None

        # ------------------------------------------
        # INFORMATIONS SUR LA COURSE
        # ------------------------------------------

        self.checkpoints = {1, 2}

        self.visited = {
            1: set(),
            2: set()
        }

        # Prochain checkpoint à atteindre par chaque joueur.
        self.next_checkpoint = {
            1: 1,
            2: 1
        }

        # Dernière position enregistrée pour chaque joueur.
        # Les coordonnées sont exprimées en pixels (x, y).

        self.last_checkpoint_position = {
            1: None,
            2: None
        }

        # Orientation enregistrée au dernier checkpoint.
        self.last_checkpoint_angle = {
            1: 0.0,
            2: 0.0
        }

        self.laps = {
            1: 0,
            2: 0
        }

        self.laps_to_win = 3

        self.winner = None

        # Mémorise le bloc spécial occupé par chaque voiture.
        # Évite d'activer plusieurs fois le même bloc.

        self.active_block = {
            1: None,
            2: None
        }

    # ==================================================
    # CHARGEMENT DU CIRCUIT
    # ==================================================

    def load_circuit(self) -> bool:

        """Charge le circuit sélectionné."""

        # Pour le moment, seul le circuit Easy est disponible.
        if self.selected_circuit == 0:
            self.circuit = Circuit.create_easy()
        elif self.selected_circuit == 1:
            self.circuit = Circuit.create_intermediate()
        elif self.selected_circuit == 2:
            self.circuit = Circuit.create_hard()
        else:
             return False

        

        self.checkpoints = set(self.circuit.checkpoint_ids)

        self.laps_to_win = self.circuit.laps_to_win

        # Réinitialise les informations de la course.
        self.laps = {
            1: 0,
            2: 0
        }

        self.visited = {
            1: set(),
            2: set()
        }

        self.next_checkpoint = {
            1: 1,
            2: 1
        }

        self.winner = None

        self.active_block = {
            1: None,
            2: None
        }

        self.last_checkpoint_position = {
            1: None,
            2: None
        }

        self.last_checkpoint_angle = {
            1: 0.0,
            2: 0.0
        }

        self.spawn_cars()

        return True

    # ==================================================
    # PLACEMENT DES VOITURES
    # ==================================================

    def spawn_cars(self):

        """Place les deux voitures sur leurs positions de départ."""

        row_1, col_1 = self.circuit.start_positions[1]

        row_2, col_2 = self.circuit.start_positions[2]

        self.car = Car(col_1, row_1)

        self.car_2 = Car(col_2, row_2)

        # Enregistre les positions et orientations initiales.
        self._save_checkpoint_state(1, self.car)

        self._save_checkpoint_state(2, self.car_2)

    # ==================================================
    # ENREGISTREMENT DU CHECKPOINT
    # ==================================================

    def _save_checkpoint_state(self, player, car):

        """
        Enregistre la position et l'orientation de la voiture.
        Ces informations seront utilisées lors de sa réapparition.
        """

        self.last_checkpoint_position[player] = (
            car.x,
            car.y
        )

        self.last_checkpoint_angle[player] = car.angle

    # ==================================================
    # DÉTECTION DU VIDE
    # ==================================================

    def _is_void(self, tile):

        """
        Vérifie si la voiture est en dehors de la carte
        ou sur une case de type VoidTerrain.
        """

        return (
            tile is None
            or isinstance(tile.terrain, VoidTerrain)
        )

    # ==================================================
    # GESTION DU TERRAIN
    # ==================================================

    def update_car_terrain(self, car):

        """Met à jour les propriétés du terrain sous la voiture."""

        tile = self.circuit.get_tile_at_pixel(
            car.x,
            car.y
        )

        # Le terrain vide est géré par le système de réapparition.
        if self._is_void(tile):
            return

        terrain = tile.terrain

        car.set_terrain(
            terrain.traction,
            terrain.drift_threshold,
            terrain.drift_friction
        )

    # ==================================================
    # RÉAPPARITION AU DERNIER CHECKPOINT
    # ==================================================

    def _respawn_at_last_checkpoint(self, player, car):

        """
        Replace la voiture au dernier checkpoint enregistré.
        Restaure sa position et son orientation.
        Réinitialise sa vitesse et ses effets de mouvement.
        """

        # Récupère la dernière position et orientation enregistrées.
        checkpoint_x, checkpoint_y = self.last_checkpoint_position[player]

        checkpoint_angle = self.last_checkpoint_angle[player]

        # Replace la voiture à sa dernière position enregistrée.
        # Cette méthode réinitialise également ses paramètres de mouvement.

        car.reset_at(
            checkpoint_x,
            checkpoint_y
        )

        # Restaure l'orientation de la voiture.
        car.angle = checkpoint_angle

        # La voiture n'occupe plus son ancien bloc spécial.
        self.active_block[player] = None

        # Met à jour les propriétés du terrain à la nouvelle position.
        self.update_car_terrain(car)

    # ==================================================
    # INTERACTIONS AVEC LES BLOCS
    # ==================================================

    def _process_block(self, player, car, tile):

        block = tile.block

        block_id = block.block_id if block is not None else None

        # La voiture a quitté un bloc spécial.
        if block_id is None:

            self.active_block[player] = None

            return

        # Évite de réactiver un bloc déjà occupé.
        if block_id == self.active_block[player]:

            return

        self.active_block[player] = block_id

        # ------------------------------------------
        # CHECKPOINT
        # ------------------------------------------

        if isinstance(block, CheckpointBlock):

            # Les checkpoints doivent être franchis dans le bon ordre.
            if block.order == self.next_checkpoint[player]:

                self.visited[player].add(block.order)

                # Enregistre la position et l'orientation de la voiture.
                self._save_checkpoint_state(player, car)

                self.next_checkpoint[player] += 1

        # ------------------------------------------
        # LIGNE D'ARRIVÉE
        # ------------------------------------------

        elif isinstance(block, FinishBlock):

            # Un tour est validé uniquement après C1 et C2.
            if self.next_checkpoint[player] == len(self.checkpoints) + 1:

                self.laps[player] += 1

                # Réinitialise la progression pour le tour suivant.
                self.visited[player].clear()

                self.next_checkpoint[player] = 1

                # Vérifie si le joueur a gagné.
                if self.laps[player] >= self.laps_to_win:

                    self.winner = player

                    self.state = GameState.FINISHED

        # ------------------------------------------
        # BOOST
        # ------------------------------------------

        elif isinstance(block, BoostBlock):

            car.apply_boost()

    # ==================================================
    # MISE À JOUR D'UN JOUEUR
    # ==================================================

    def _update_one_car(self, player, car):

        # Vérifie la case actuelle avant le calcul du mouvement.
        current_tile = self.circuit.get_tile_at_pixel(
            car.x,
            car.y
        )

        # Si la voiture est déjà dans le vide, la replacer.
        if self._is_void(current_tile):

            self._respawn_at_last_checkpoint(player, car)

            return

        # Applique les propriétés du terrain actuel.
        self.update_car_terrain(car)

        # Met à jour la physique et la position de la voiture.
        car.update_position()

        # Vérifie immédiatement la nouvelle position.
        new_tile = self.circuit.get_tile_at_pixel(
            car.x,
            car.y
        )

        # Si la voiture tombe dans le vide, la replacer.
        if self._is_void(new_tile):

            self._respawn_at_last_checkpoint(player, car)

            return

        # Met à jour les propriétés du terrain pour la prochaine frame.
        self.update_car_terrain(car)

        # Gère le bloc spécial sur lequel la voiture vient d'arriver.
        self._process_block(player, car, new_tile)

    # ==================================================
    # MISE À JOUR DU JEU


    def update(self):

        """Met à jour les deux voitures et leurs interactions avec le circuit."""

        if (
            self.state != GameState.RACING
            or self.circuit is None
            or self.car is None
            or self.car_2 is None
        ):
            return

        # Mise à jour du joueur 1.
        self._update_one_car(1, self.car)

        # Si le joueur 1 a gagné, arrêter la mise à jour.
        if self.state != GameState.RACING:
            return

        # Mise à jour du joueur 2.
        self._update_one_car(2, self.car_2)