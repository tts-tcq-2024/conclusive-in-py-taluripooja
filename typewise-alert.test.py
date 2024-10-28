import unittest
from unittest.mock import patch
import typewise_alert


class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')

    def test_infer_breach_low(self):
        self.assertEqual(typewise_alert.infer_breach(20, 50, 100), 'TOO_LOW')

    def test_infer_breach_high(self):
        self.assertEqual(typewise_alert.infer_breach(110, 50, 100), 'TOO_HIGH')

    def test_infer_breach_normal(self):
        self.assertEqual(typewise_alert.infer_breach(75, 50, 100), 'NORMAL')

    def test_get_temperature_limits(self):
        self.assertEqual(typewise_alert.get_temperature_limits('PASSIVE_COOLING'), (0, 35))
        self.assertEqual(typewise_alert.get_temperature_limits('HI_ACTIVE_COOLING'), (0, 45))
        self.assertEqual(typewise_alert.get_temperature_limits('MED_ACTIVE_COOLING'), (0, 40))
        self.assertEqual(typewise_alert.get_temperature_limits('UNKNOWN_COOLING'), (0, 0))

    def test_classify_temperature_breach_passive_cooling(self):
        self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 20), 'NORMAL')
        self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 36), 'TOO_HIGH')

    def test_classify_temperature_breach_active_cooling(self):
        self.assertEqual(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 46), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 39), 'NORMAL')

    @patch('typewise_alert.send_to_controller')
    def test_check_and_alert_controller(self, mock_send):
        typewise_alert.check_and_alert('TO_CONTROLLER', {'coolingType': 'PASSIVE_COOLING'}, 20)
        mock_send.assert_called_once_with('NORMAL')

    @patch('typewise_alert.send_to_email')
    def test_check_and_alert_email(self, mock_send):
        typewise_alert.check_and_alert('TO_EMAIL', {'coolingType': 'PASSIVE_COOLING'}, 36)
        mock_send.assert_called_once_with('TOO_HIGH')


if __name__ == '__main__':
    unittest.main()
