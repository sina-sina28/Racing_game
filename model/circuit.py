from constants import GRID_COLS, GRID_ROWS, TILE_SIZE

from model.road_tile import RoadTile

from model.terrain import (
    RoadTerrain,
    GrassTerrain,
    DirtTerrain,
    IceTerrain,
    VoidTerrain
)

from model.blocks import (
    StartBlock,
    CheckpointBlock,
    FinishBlock,
    BoostBlock
)


class Circuit:

    def __init__(self, grid, start_positions, checkpoint_ids, laps_to_win=3):

        self.grid = grid

        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

        # Positions : joueur -> (ligne, colonne).
        self.start_positions = start_positions

        self.checkpoint_ids = tuple(checkpoint_ids)

        self.laps_to_win = laps_to_win

    # ==================================================
    # CRÉATION DU CIRCUIT EASY
    # ==================================================

    @classmethod
    def create_easy(cls):

        # Chaque caractère représente une case.
        #
        # R = Route
        # G = Herbe
        # D = Terre
        # I = Glace
        # V = Vide

        layout = [

            "VVVVVVVVVVVVVVVV",

            "VGGGGGGGGGGGGGGV",

            "VGRRRRRRRRRRRRGV",

            "VGRRRRRRRRRRRRGV",

            "VGRRGGGGGVIIRRGV",

            "VGRRVVVGGVIIRRGV",

            "VGRRDDVGGVVVRRGV",

            "VGRRDDVGGGGGRRGV",

            "VGRRRRRRRRRRRRGV",

            "VGRRRRRRRRRRRRGV",

            "VGGGGGGGGGGGGGGV",

            "VVVVVVVVVVVVVVVV"

        ]

        # Vérifie les dimensions de la grille.
        if len(layout) != GRID_ROWS:
            raise ValueError("Nombre de lignes incorrect")

        for row in layout:

            if len(row) != GRID_COLS:
                raise ValueError("Nombre de colonnes incorrect")

        # ==================================================
        # TYPES DE TERRAINS
        # ==================================================

        terrain_classes = {

            "R": RoadTerrain,
            "G": GrassTerrain,
            "D": DirtTerrain,
            "I": IceTerrain,
            "V": VoidTerrain

        }

        # ==================================================
        # BLOCS SPÉCIAUX
        # ==================================================

        start_p1 = StartBlock(1)

        start_p2 = StartBlock(2)

        checkpoint_1 = CheckpointBlock(1)

        checkpoint_2 = CheckpointBlock(2)

        finish = FinishBlock()

        boost_1 = BoostBlock(1)

        boost_2 = BoostBlock(2)

        # Coordonnées sous la forme (ligne, colonne).
        # Les cases adjacentes partagent le même objet bloc.

        blocks_by_cell = {

            # Positions de départ.
            (3, 3): start_p1,
            (2, 3): start_p2,

            # Boost 1.
            (2, 6): boost_1,
            (3, 6): boost_1,

            # Ligne d'arrivée.
            (5, 2): finish,
            (5, 3): finish,

            # Checkpoint 1.
            (5, 12): checkpoint_1,
            (5, 13): checkpoint_1,

            # Checkpoint 2.
            (8, 7): checkpoint_2,
            (9, 7): checkpoint_2,

            # Boost 2.
            (8, 10): boost_2,
            (9, 10): boost_2

        }

        # ==================================================
        # CONSTRUCTION DE LA GRILLE
        # ==================================================

        grid = []

        for row_index, row_text in enumerate(layout):

            tile_row = []

            for col_index, symbol in enumerate(row_text):

                terrain_class = terrain_classes[symbol]

                terrain = terrain_class()

                block = blocks_by_cell.get(
                    (row_index, col_index)
                )

                tile = RoadTile(
                    col=col_index,
                    row=row_index,
                    terrain=terrain,
                    block=block
                )

                tile_row.append(tile)

            grid.append(tile_row)

        # ==================================================
        # POSITIONS DE DÉPART
        # ==================================================

        start_positions = {

            1: (3, 3),

            2: (2, 3)

        }

        return cls(
            grid=grid,
            start_positions=start_positions,
            checkpoint_ids=(1, 2),
            laps_to_win=3
        )

    # ==================================================
    # CRÉATION DU CIRCUIT INTERMEDIATE
    # ==================================================

    @classmethod
    def create_intermediate(cls):

        # Chaque caractère représente une case.
        #
        # R = Route
        # G = Herbe
        # D = Terre
        # I = Glace
        # V = Vide

        layout = [

            "VVVVVVVVVVVVVVVV",

            "VGGVVGDDDRRRGGGV",

            "VGGGGGDRDRRRGGGV",

            "VRRDDDIVVDRRRDDV",

            "VRRVVVVVGDRRRDDV",

            "VRGVVVVVRRVVVVVV",

            "VDGVVVVVRRRRRRVV",

            "VDDVVVVVVRRRRRGV",

            "VDDVVVVVVVVVDIIV",

            "VRRRRRIIIGGGDIIV",

            "VRRRRRIIIGGDDIIV",

            "VVVVVVVVVVVVVVVV"

        ]

        # Vérifie les dimensions de la grille.
        if len(layout) != GRID_ROWS:
            raise ValueError("Nombre de lignes incorrect")

        for row in layout:

            if len(row) != GRID_COLS:
                raise ValueError("Nombre de colonnes incorrect")

        # ==================================================
        # TYPES DE TERRAINS
        # ==================================================

        terrain_classes = {

            "R": RoadTerrain,
            "G": GrassTerrain,
            "D": DirtTerrain,
            "I": IceTerrain,
            "V": VoidTerrain

        }

        # ==================================================
        # BLOCS SPÉCIAUX
        # ==================================================

        start_p1 = StartBlock(1)

        start_p2 = StartBlock(2)

        checkpoint_1 = CheckpointBlock(1)

        checkpoint_2 = CheckpointBlock(2)

        finish = FinishBlock()

        boost_1 = BoostBlock(1)

        boost_2 = BoostBlock(2)

        # Coordonnées sous la forme (ligne, colonne).
        # Les cases adjacentes partagent le même objet bloc.

        blocks_by_cell = {

            # Positions de départ.
            (9, 1): start_p1,
            (10, 1): start_p2,

            # Boost 1.
            (9, 4): boost_1,
            (10, 4): boost_1,

            # Ligne d'arrivée.
            (8, 1): finish,
            (8, 2): finish,

            # Checkpoint 1.
            (6, 10): checkpoint_1,
            (7, 10): checkpoint_1,

            # Checkpoint 2.
            (3, 12): checkpoint_2,
            (4, 12): checkpoint_2,

            # Boost 2.
            (1, 11): boost_2,
            (2, 11): boost_2

        }

        # ==================================================
        # CONSTRUCTION DE LA GRILLE
        # ==================================================

        grid = []

        for row_index, row_text in enumerate(layout):

            tile_row = []

            for col_index, symbol in enumerate(row_text):

                terrain_class = terrain_classes[symbol]

                terrain = terrain_class()

                block = blocks_by_cell.get(
                    (row_index, col_index)
                )

                tile = RoadTile(
                    col=col_index,
                    row=row_index,
                    terrain=terrain,
                    block=block
                )

                tile_row.append(tile)

            grid.append(tile_row)

        # ==================================================
        # POSITIONS DE DÉPART
        # ==================================================

        start_positions = {

            1: (9, 1),

            2: (10, 1)

        }

        return cls(
            grid=grid,
            start_positions=start_positions,
            checkpoint_ids=(1, 2),
            laps_to_win=3
        )

    # ==================================================
    # MÉTHODES COMMUNES AUX CIRCUITS
    # ==================================================

    def get_tile(self, col, row):

        """Retourne la case correspondant aux coordonnées."""

        if 0 <= row < self.rows and 0 <= col < self.cols:

            return self.grid[row][col]

        return None

    def get_tile_at_pixel(self, px, py):

        """Retourne la case située sous une position en pixels."""

        col = int(px // TILE_SIZE)

        row = int(py // TILE_SIZE)

        return self.get_tile(col, row)

    def pixel_width(self):

        """Retourne la largeur totale du circuit en pixels."""

        return self.cols * TILE_SIZE

    def pixel_height(self):

        """Retourne la hauteur totale du circuit en pixels."""

        return self.rows * TILE_SIZE