import random
from typing import List

from src.models.ownership import Ownership
from src.models.player import Player


def make_board() -> List[Ownership]:
    board = []
    values = [random.randrange(40, 200, 20) for i in range(10)]

    for i, value in enumerate(values):
        rent_value = round(value / 4)
        board.append(Ownership(i, value, rent_value))

    return board


def make_players() -> List[Player]:
    profiles = [
        'impulsivo',
        'exigente',
        'cauteloso',
        'aleatório'
    ]
    return [Player(id, profile) for id, profile in enumerate(profiles)]


def roll_the_dice() -> int:
    return random.choice([n for n in range(1, 7)])


def pay_rent(player: Player, ownership: Ownership) -> bool:
    return ownership.owner and ownership.owner != player.id


def start():
    pass

    
if __name__ == '__main__':
    start()
