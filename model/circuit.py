'''from model.road_tile import RoadTile
from constants import TILE_SIZE


class Circuit:

    def __init__(self,  grid: list[list[RoadTile]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE
'''

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

        # Positions: player -> (row, column).
        self.start_positions = start_positions

        self.checkpoint_ids = tuple(checkpoint_ids)

        self.laps_to_win = laps_to_win

    # ==================================================
    # CREATE EASY CIRCUIT
    # ==================================================

    @classmethod
    def create_easy(cls):

        # Each character represents one cell.
        #
        # R = Road
        # G = Grass
        # D = Dirt
        # I = Ice
        # V = Void

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

        # Check the grid dimensions.
        if len(layout) != GRID_ROWS:
            raise ValueError("Incorrect number of rows")

        for row in layout:

            if len(row) != GRID_COLS:
                raise ValueError("Incorrect number of columns")

        # ==================================================
        # TERRAIN TYPES
        # ==================================================

        terrain_classes = {

            "R": RoadTerrain,
            "G": GrassTerrain,
            "D": DirtTerrain,
            "I": IceTerrain,
            "V": VoidTerrain

        }

        # ==================================================
        # SPECIAL BLOCKS
        # ==================================================

        start_p1 = StartBlock(1)

        start_p2 = StartBlock(2)

        checkpoint_1 = CheckpointBlock(1)

        checkpoint_2 = CheckpointBlock(2)

        finish = FinishBlock()

        boost_1 = BoostBlock(1)

        boost_2 = BoostBlock(2)

        # Coordinates use (row, column).
        #
        # Adjacent cells share the same block object.
        # This means they represent ONE logical block.

        blocks_by_cell = {

            # Starting positions.
            (3, 3): start_p1,
            (2, 3): start_p2,

            # Boost 1.
            (2, 6): boost_1,
            (3, 6): boost_1,

            # Finish line.
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
        # CREATE THE GRID
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
        # PLAYER STARTING POSITIONS
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
    # CIRCUIT METHODS
    # ==================================================

    def get_tile(self, col, row):

        if 0 <= row < self.rows and 0 <= col < self.cols:

            return self.grid[row][col]

        return None

    def get_tile_at_pixel(self, px, py):

        col = int(px // TILE_SIZE)

        row = int(py // TILE_SIZE)

        return self.get_tile(col, row)

    def pixel_width(self):

        return self.cols * TILE_SIZE

    def pixel_height(self):

        return self.rows * TILE_SIZE