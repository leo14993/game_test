from unittest import TestCase

from unittest.mock import patch

from src.models.ownership import Ownership
from src.models.player import Player


class MyTestCase(TestCase):
    _player_impulsivo = Player(1, 'impulsivo')
    _player_exigente = Player(2, 'exigente')
    _player_cauteloso = Player(3, 'cauteloso')
    _player_aleatorio = Player(4, 'aleatório')

    def setUp(self):
        pass
        # self.player_id = 1
        # self.player_profiles = ['impulsivo', 'exigente', 'cauteloso', 'aleatório']

    @patch('src.models.ownership.Ownership')
    def test_player_lost_then_lost_ownerships_and_status_is_false(self, ownership_mock):
        # arrange
        ownership_mock.owner = self._player_aleatorio.id
        ownerships_mock = [ownership_mock for i in range(5)]
        self._player_aleatorio.ownerships = ownerships_mock

        expected_ownerships = []

        # act
        self._player_aleatorio.lost()

        # assert
        self.assertEqual(self._player_aleatorio.ownerships, expected_ownerships)
        self.assertFalse(self._player_aleatorio.status)



    def test_complete_lap(self):

        # arrange
        self._player_aleatorio.cash = 0
        expected_player_cash = 100

        # act
        self._player_aleatorio.complete_lap()

        # assert
        self.assertEqual(self._player_aleatorio.cash, expected_player_cash)

    def test_player_position(self):
        # arrange
        position = 5
        self._player_aleatorio.position = 0
        expected_position = position

        # act
        self._player_aleatorio.player_position(position)

        # assert
        self.assertEqual(self._player_aleatorio.position, expected_position)

    def test_demanding_player_when_insert_value_then_return_expected_answer(self):
        # arrange
        rent_value_ok = 51
        rent_value_not_ok = 50
        rent_value_not_ok = 49

        # act
        expected_answer_1 = self._player_exigente.demanding_player(rent_value_ok)
        expected_answer_2 = self._player_exigente.demanding_player(rent_value_not_ok)
        expected_answer_3 = self._player_exigente.demanding_player(rent_value_not_ok)

        # assert
        self.assertTrue(expected_answer_1)
        self.assertFalse(expected_answer_2)
        self.assertFalse(expected_answer_3)

    def test_cautious_player_when_insert_value_then_return_expected_answer(self):
        # arrange
        self._player_cauteloso.cash = 200
        property_price1 = 119
        property_price2 = 120
        property_price3 = 121

        # act
        expected_answer_1 = self._player_cauteloso.cautious_player(property_price1)
        expected_answer_2 = self._player_cauteloso.cautious_player(property_price2)
        expected_answer_3 = self._player_cauteloso.cautious_player(property_price3)

        # assert
        self.assertTrue(expected_answer_1)
        self.assertFalse(expected_answer_2)
        self.assertFalse(expected_answer_3)

    @patch('src.models.ownership.Ownership')
    @patch('src.models.player.Player.demanding_player')
    @patch('src.models.player.Player.cautious_player')
    @patch('src.models.player.Player.random_player')
    def test_buy_property_when_impulsive_player_has_cash(self,
                                                         random_player_mock,
                                                         cautious_player_mock,
                                                         demanding_player_mock,
                                                         ownership_mock):
        # arrange
        ownership_mock.value = 200
        ownership_mock.rent_value = 80
        self._player_impulsivo.cash = 200
        random_player_mock.return_value = False
        cautious_player_mock.return_value = False
        demanding_player_mock.return_value = False
        expected_cash_after_buy = 0

        # act
        self._player_impulsivo.buy_property(ownership_mock)
        self.assertEqual(self._player_impulsivo.cash, expected_cash_after_buy)

        # assert
        random_player_mock.assert_not_called()
        cautious_player_mock.assert_not_called()
        demanding_player_mock.assert_not_called()

    @patch('src.models.ownership.Ownership')
    @patch('src.models.player.Player.demanding_player')
    @patch('src.models.player.Player.cautious_player')
    @patch('src.models.player.Player.random_player')
    def test_buy_property_when_impulsive_player_has_not_sufficient_cash(self,
                                                                        random_player_mock,
                                                                        cautious_player_mock,
                                                                        demanding_player_mock,
                                                                        ownership_mock):
        # arrange
        ownership_mock.value = 201
        ownership_mock.rent_value = 80
        self._player_impulsivo.cash = 200
        random_player_mock.return_value = False
        cautious_player_mock.return_value = False
        demanding_player_mock.return_value = False
        expected_cash_after_buy = 200

        # act
        self._player_impulsivo.buy_property(ownership_mock)

        # assert
        random_player_mock.assert_not_called()
        cautious_player_mock.assert_not_called()
        demanding_player_mock.assert_not_called()
        self.assertEqual(self._player_impulsivo.cash, expected_cash_after_buy)

    @patch('src.models.ownership.Ownership')
    @patch('src.models.player.Player.demanding_player')
    @patch('src.models.player.Player.cautious_player')
    @patch('src.models.player.Player.random_player')
    def test_buy_property_when_demanding_player_buy_property(self,
                                                             random_player_mock,
                                                             cautious_player_mock,
                                                             demanding_player_mock,
                                                             ownership_mock):
        # arrange
        ownership_mock.value = 200
        rent_value = 51
        ownership_mock.rent_value = rent_value
        self._player_exigente.cash = 200
        random_player_mock.return_value = False
        cautious_player_mock.return_value = False
        demanding_player_mock.return_value = True
        expected_cash_after_buy = 0

        # act
        self._player_exigente.buy_property(ownership_mock)

        # assert
        random_player_mock.assert_not_called()
        cautious_player_mock.assert_not_called()
        demanding_player_mock.assert_called_once_with(rent_value)
        self.assertEqual(self._player_exigente.cash, expected_cash_after_buy)

    @patch('src.models.ownership.Ownership')
    @patch('src.models.player.Player.demanding_player')
    @patch('src.models.player.Player.cautious_player')
    @patch('src.models.player.Player.random_player')
    def test_buy_property_when_demanding_player_want_buy_property_but_has_not_sufficient_cash(self,
                                                                                              random_player_mock,
                                                                                              cautious_player_mock,
                                                                                              demanding_player_mock,
                                                                                              ownership_mock):
        # arrange
        ownership_mock.value = 201
        rent_value = 51
        ownership_mock.rent_value = rent_value
        self._player_exigente.cash = 200
        random_player_mock.return_value = False
        cautious_player_mock.return_value = False
        demanding_player_mock.return_value = True
        expected_cash_after_buy = 200

        # act
        self._player_exigente.buy_property(ownership_mock)

        # assert
        random_player_mock.assert_not_called()
        cautious_player_mock.assert_not_called()
        demanding_player_mock.assert_called_once_with(rent_value)
        self.assertEqual(self._player_exigente.cash, expected_cash_after_buy)

    @patch('src.models.ownership.Ownership')
    @patch('src.models.player.Player.demanding_player')
    @patch('src.models.player.Player.cautious_player')
    @patch('src.models.player.Player.random_player')
    def test_buy_property_when_demanding_player_dont_buy_property(self,
                                                                  random_player_mock,
                                                                  cautious_player_mock,
                                                                  demanding_player_mock,
                                                                  ownership_mock):
        # arrange
        ownership_mock.value = 201
        rent_value = 50
        ownership_mock.rent_value = rent_value
        self._player_exigente.cash = 200
        random_player_mock.return_value = False
        cautious_player_mock.return_value = False
        demanding_player_mock.return_value = True
        expected_cash_after_buy = 200

        # act
        self._player_exigente.buy_property(ownership_mock)

        # assert
        random_player_mock.assert_not_called()
        cautious_player_mock.assert_not_called()
        demanding_player_mock.assert_called_once_with(rent_value)
        self.assertEqual(self._player_exigente.cash, expected_cash_after_buy)




    #: Todo: Faltou os testes para os players cautelosos e aleatorios

# arrange
# act
# assert
