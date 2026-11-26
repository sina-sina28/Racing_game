class Block:
    """Classe mère représentant un bloc spécial."""

    def __init__(self, label, block_id):

        self.label = label
        self.block_id = block_id


class StartBlock(Block):

    def __init__(self, player_id):

        super().__init__(
            f"P{player_id}",
            f"start_{player_id}"
        )

        self.player_id = player_id


class CheckpointBlock(Block):

    def __init__(self, order):

        super().__init__(
            f"C{order}",
            f"checkpoint_{order}"
        )

        self.order = order


class FinishBlock(Block):

    def __init__(self):

        super().__init__("F", "finish")


class BoostBlock(Block):

    def __init__(self, number):

        super().__init__(
            f"B{number}",
            f"boost_{number}"
        )

        self.number = number