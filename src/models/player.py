import random
from typing import List

from src.models.ownership import Ownership

IMPULSIVE = 'impulsivo'
DEMANDING = 'exigente'
CAUTIOUS = 'cauteloso'
RANDOM = 'aleatório'

class Player:
    def __init__(self, id: int, player_profile: str):
        self.id = id
        self.status: bool = True
        self.player_profile = player_profile
        self.cash = 300
        self.position = 0
        self.ownerships: List = []

    @staticmethod
    def demanding_player(rent_value: int) -> bool:
        if rent_value > 50:
            return True
        return False

    def cautious_player(self, property_price: int) -> bool:
        return (self.cash - property_price) > 80

    @staticmethod
    def random_player() -> bool:
        return random.choice([True, False])

    def buy_property(self, ownership: Ownership) -> None:
        buy_property = {
            IMPULSIVE: True,
            DEMANDING: self.demanding_player(ownership.rent_value) if self.player_profile == DEMANDING else None,
            CAUTIOUS: self.cautious_player(ownership.value) if self.player_profile == CAUTIOUS else None,
            RANDOM: self.random_player() if self.player_profile == RANDOM else None
        }

        if buy_property[self.player_profile]:
            if self.cash >= ownership.value:
                self.cash -= ownership.value
                ownership.owner = self.id
                self.ownerships.append(ownership)

    def complete_lap(self) -> None:
        self.cash += 100

    def player_position(self, value: int) -> None:
        self.position = value

    def lost(self) -> None:
        for ownership in self.ownerships:
            ownership.owner = None
        self.ownerships = []
        self.status = False
