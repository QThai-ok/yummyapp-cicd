import unittest
from unittest.mock import patch

from yummy_app import YummyApp


class TestYummyApp(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_returns_restaurants(self, mock_location):
        mock_location.return_value = (10.0, 105.0)

        result = self.app.get_nearby_restaurants()

        self.assertEqual(
            result,
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        mock_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_returns_empty_list(self, mock_location):
        mock_location.return_value = (20.0, 110.0)

        result = self.app.get_nearby_restaurants()

        self.assertEqual(result, [])
        mock_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_signal_lost(self, mock_location):
        from gps_service import GPSSignalLostError

        mock_location.side_effect = GPSSignalLostError("GPS lost")

        result = self.app.get_nearby_restaurants()

        self.assertEqual(result, "Khong the xac dinh vi tri.")

    def test_promo_valid_online(self):
        self.app.network_status = "online"

        result = self.app.apply_promo_code(100000, "GIAM10")

        self.assertEqual(result, 90000)

    def test_promo_network_error(self):
        self.app.network_status = "offline"

        with self.assertRaises(ConnectionError):
            self.app.apply_promo_code(100000, "GIAM10")

    def test_promo_new_os_supported(self):
        self.app.os_version = 15

        result = self.app.apply_promo_code(100000, "NEW_OS_ONLY")

        self.assertEqual(result, 80000)

    def test_promo_new_os_not_supported(self):
        self.app.os_version = 14

        with self.assertRaises(ValueError):
            self.app.apply_promo_code(100000, "NEW_OS_ONLY")


if __name__ == "__main__":
    unittest.main()
