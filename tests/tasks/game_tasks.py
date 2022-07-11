from unittest import TestCase

from unittest.mock import patch

from src.models.ownership import Ownership
from src.models.player import Player
from src.tasks.game_tasks import GameTasks


class MainTestCase(TestCase):
    # _player_impulsivo = Player(1, 'impulsivo')
    # _player_exigente = Player(2, 'exigente')
    # _player_cauteloso = Player(3, 'cauteloso')
    # _player_aleatorio = Player(4, 'aleatório')

    _game_tasks = GameTasks()

    @patch('src.tasks.game_tasks.Ownership')
    @patch('src.tasks.game_tasks.random')
    def test_make_board(self, random_mock, ownership_mock):
        # arrange
        ownership_value = 100
        random_mock.randrange.return_value = ownership_value
        ownership_mock().value = ownership_value

        # act
        current_board = self._game_tasks.make_board()

        # assert
        random_mock.randrange.assert_called_with(40, 200, 20)
        for ownership in current_board:
            self.assertEqual(ownership.value, ownership_value)

    @patch('src.tasks.game_tasks.Player')
    def test_make_players(self, player_mock):
        # arrange
        player_mock().player_profile = 'aleatório'
        profiles = [
            'impulsivo',
            'exigente',
            'cauteloso',
            'aleatório'
        ]

        # act
        current_players = self._game_tasks.make_players()

        # assert
        for player in current_players:
            self.assertTrue(player.player_profile in profiles)

    @patch('src.tasks.game_tasks.random')
    def test_roll_the_dice(self, random_mock):
        # arrange
        expected_dice_value = 3
        dice_values = [1, 2, 3, 4, 5, 6]
        random_mock.choice.return_value = expected_dice_value

        # act
        current_dice_value = self._game_tasks.roll_the_dice()

        # arrange
        self.assertEqual(expected_dice_value, current_dice_value)
        random_mock.choice.assert_called_once_with(dice_values)

    @patch('src.tasks.game_tasks.Ownership')
    @patch('src.tasks.game_tasks.Player')
    def test_pay_rent_when_player_must_pay_rent(self, player_mock, ownership_mock):
        # arrange
        ownership_mock().owner = 1
        player_mock().id = 2

        # act
        pay_rent = self._game_tasks.pay_rent(player_mock, ownership_mock)

        # arrange

        self.assertTrue(pay_rent)

    @patch('src.tasks.game_tasks.Ownership')
    @patch('src.tasks.game_tasks.Player')
    def test_pay_rent_when_player_must_not_pay_rent(self, player_mock, ownership_mock):
        # arrange
        ownership_mock().owner = 1
        player_mock().id = 1

        # act
        pay_rent = self._game_tasks.pay_rent(player_mock, ownership_mock)

        # arrange

        self.assertFalse(pay_rent)

    @patch('src.tasks.game_tasks.Ownership')
    @patch('src.tasks.game_tasks.Player')
    def test_pay_rent_when_player_must_not_pay_rent(self, player_mock, ownership_mock):
        # arrange
        ownership_mock.owner = None
        player_mock.id = 1

        # act
        pay_rent = self._game_tasks.pay_rent(player_mock, ownership_mock)

        # arrange
        self.assertFalse(pay_rent)
