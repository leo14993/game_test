import random
from typing import List

from src.models.ownership import Ownership
from src.models.player import Player


class GameTasks:

    _min_ownership_value: int = 40
    _max_ownership_value: int = 200
    _steps_ownership_value: int = 20
    _board_size: int = 20
    _dice_faces: int = 6
    _dice_values = [n for n in range(1, _dice_faces + 1)]

    def make_board(self) -> List[Ownership]:
        board = []
        values = [random.randrange(
            self._min_ownership_value,
            self._max_ownership_value,
            self._steps_ownership_value
        ) for i in range(self._board_size)]

        for i, value in enumerate(values):
            rent_value = round(value / 4)
            board.append(Ownership(id=i, value=value, rent_value=rent_value))

        return board

    @staticmethod
    def make_players() -> List[Player]:
        profiles = [
            'impulsivo',
            'exigente',
            'cauteloso',
            'aleatório'
        ]
        return [Player(id, profile) for id, profile in enumerate(profiles)]

    def roll_the_dice(self) -> int:
        return random.choice(self._dice_values)

    @staticmethod
    def pay_rent(player: Player, ownership: Ownership) -> bool:
        return ownership.owner and ownership.owner != player.id

    def run(self):

        ownerships = self.make_board()
        board_size = len(ownerships)
        players = self.make_players()
        random.shuffle(players)

        timeout = []
        simulation_rolls = []

        for simulation in range(301):

            rolls = 0

            for roll in range(1001):
                rolls += 1

                for player in players:
                    dice_value = (self.roll_the_dice())

                    player.position += dice_value

                    if player.position >= board_size:
                        player.complete_lap()
                        player.position -= board_size

                    ownership = ownerships[player.position]

                    must_buy_rent = self.pay_rent(player, ownership)
                    if self.pay_rent(player, ownership):
                        owner = list(filter(lambda player: player.id == ownership.owner, players))[0]
                        rent = ownership.rent_value
                        player.cash -= rent
                        if player.cash < 0:
                            player.lost()
                            rent = rent + player.cash

                        owner.cash += rent

                    player.buy_property(ownerships[player.position])

                    # buy_rent(player, owner)
            simulation_rolls.append(rolls)