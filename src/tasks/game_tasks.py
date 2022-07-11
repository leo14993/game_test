import random
from statistics import mean
from typing import List, Dict

from src.models.ownership import Ownership
from src.models.player import Player, IMPULSIVE, DEMANDING, CAUTIOUS, RANDOM


class GameTasks:

    _min_ownership_value: int = 80
    _max_ownership_value: int = 300
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
    def reset_board(ownerships: List[Ownership]) -> List[Ownership]:
        reseted_list = []
        for ownership in ownerships:
            ownership.owner = None
            reseted_list.append(ownership)

        return reseted_list

    def remove_player_from_ownerships(self, ownerships: List[Ownership], player_id) -> List[Ownership]:
        reseted_list = []
        for ownership in ownerships:
            if ownership.owner == player_id:
                ownership.owner = None
            reseted_list.append(ownership)

        return reseted_list

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

    @staticmethod
    def get_best_player(players_victories: Dict) -> str:
        new_dict = {}
        for key, value in players_victories.items():
            new_dict[value] = key

        return new_dict[max(new_dict.keys())]

    def run(self):

        players_victories = {
            IMPULSIVE: 0,
            DEMANDING: 0,
            CAUTIOUS: 0,
            RANDOM: 0
        }

        timeout = 0
        simulation_rolls = []
        ownerships = self.make_board()
        board_size = len(ownerships)

        for simulation in range(300):

            players = self.make_players()
            random.shuffle(players)

            game = True
            rolls = 0
            while game:
                rolls += 1

                for player in players:
                    dice_value = (self.roll_the_dice())

                    player.position += dice_value

                    if player.position >= board_size:
                        player.complete_lap()
                        player.position -= board_size

                    ownership = ownerships[player.position]

                    must_buy_rent = self.pay_rent(player, ownership)

                    if must_buy_rent:
                        owner = list(filter(lambda player: player.id == ownership.owner, players))[0]
                        rent = ownership.rent_value
                        player.cash -= rent
                        if player.cash < 0:
                            player.lost()
                            rent = rent + player.cash
                            ownerships = self.remove_player_from_ownerships(ownerships, player.id)

                        owner.cash += rent

                        if not player.status:
                            players.remove(player)

                    player.buy_property(ownerships[player.position])

                if len(players) == 1:
                    ownerships = self.reset_board(ownerships)
                    game = False
                    players_victories[players[0].player_profile] += 1
                elif rolls == 100:
                    ownerships = self.reset_board(ownerships)
                    game = False
                    timeout += 1

            simulation_rolls.append(rolls)

        best_player = self.get_best_player(players_victories)

        print(f'Partidas terminadas por Timeout: {timeout}')
        print(f'Média de turnos de uma partida: {round(mean(simulation_rolls))}')
        print(f'Taxa de vitórias por jogador')
        partidas = 300 - timeout
        for player, vicory in players_victories.items():
            print(f' {player}: {round(vicory/partidas * 100,2)}%')
        print(f'Melhor comportamento: {best_player}')

        #Todo: Ficou faltando organizar isso em métodos,
        # fazer os testes unitários e aumentar o coverage para pelo menos 80%
        # :Todo