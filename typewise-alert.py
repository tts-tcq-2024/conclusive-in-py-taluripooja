import unittest
from unittest.mock import patch
import typewise_alert

class TypewiseAlertTest(unittest.TestCase):
    
    def test_infer_breach(self):
        cases = [
            (20, 50, 100, 'TOO_LOW'),
            (110, 50, 100, 'TOO_HIGH'),
            (75, 50, 100, 'NORMAL')
        ]
        for value, lower_limit, upper_limit, expected in cases:
            with self.subTest(value=value, lower_limit=lower_limit, upper_limit=upper_limit):
                self.assertEqual(typewise_alert.infer_breach(value, lower_limit, upper_limit), expected)

    def test_get_temperature_limits(self):
        cases = [
            ('PASSIVE_COOLING', (0, 35)),
            ('HI_ACTIVE_COOLING', (0, 45)),
            ('MED_ACTIVE_COOLING', (0, 40)),
            ('UNKNOWN_COOLING', (0, 0))
        ]
        for cooling_type, expected_limits in cases:
            with self.subTest(cooling_type=cooling_type):
                self.assertEqual(typewise_alert.get_temperature_limits(cooling_type), expected_limits)

    def test_classify_temperature_breach(self):
        cases = [
            ('PASSIVE_COOLING', 20, 'NORMAL'),
            ('PASSIVE_COOLING', 36, 'TOO_HIGH'),
            ('HI_ACTIVE_COOLING', 46, 'TOO_HIGH'),
            ('MED_ACTIVE_COOLING', 39, 'NORMAL')
        ]
        for cooling_type, temperature, expected_breach in cases:
            with self.subTest(cooling_type=cooling_type, temperature=temperature):
                self.assertEqual(typewise_alert.classify_temperature_breach(cooling_type, temperature), expected_breach)

    @patch('typewise_alert.send_to_controller')
    def test_alert_to_controller(self, mock_send):
        typewise_alert.check_and_alert('TO_CONTROLLER', {'coolingType': 'PASSIVE_COOLING'}, 20)
        mock_send.assert_called_once_with('NORMAL')

    @patch('typewise_alert.send_to_email')
    def test_alert_to_email(self, mock_send):
        typewise_alert.check_and_alert('TO_EMAIL', {'coolingType': 'PASSIVE_COOLING'}, 36)
        mock_send.assert_called_once_with('TOO_HIGH')

if __name__ == '__main__':
    unittest.main()
