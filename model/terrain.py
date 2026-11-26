from abc import ABC, abstractmethod

from constants import (
    DEFAULT_TRACTION,
    DEFAULT_SEUIL_DERAPAGE,
    DEFAULT_FROTTEMENT_DERAPAGE
)


class Terrain(ABC):
    """Classe mère représentant les propriétés physiques d'un terrain."""

    def __init__(
        self,
        name,
        color,
        traction,
        drift_threshold,
        drift_friction
    ):
        self.name = name
        self.color = color
        self.traction = traction
        self.drift_threshold = drift_threshold
        self.drift_friction = drift_friction

    @abstractmethod
    def get_symbol(self):
        pass


class RoadTerrain(Terrain):

    def __init__(self):
        super().__init__(
            "Road",
            (125, 140, 155),
            DEFAULT_TRACTION,
            DEFAULT_SEUIL_DERAPAGE,
            DEFAULT_FROTTEMENT_DERAPAGE
        )

    def get_symbol(self):
        return "R"


class GrassTerrain(Terrain):

    def __init__(self):
        super().__init__(
            "Grass",
            (74, 137, 12),
            0.65,
            110.0,
            0.04
        )

    def get_symbol(self):
        return "G"


class DirtTerrain(Terrain):

    def __init__(self):
        super().__init__(
            "Dirt",
            (115, 70, 25),
            0.55,
            85.0,
            0.025
        )

    def get_symbol(self):
        return "D"


class IceTerrain(Terrain):

    def __init__(self):
        super().__init__(
            "Ice",
            (109, 178, 255),
            0.25,
            20.0,
            0.002
        )

    def get_symbol(self):
        return "I"


class VoidTerrain(Terrain):

    def __init__(self):
        super().__init__(
            "Void",
            (18, 18, 18),
            0.0,
            0.0,
            0.0
        )

    def get_symbol(self):
        return "V"