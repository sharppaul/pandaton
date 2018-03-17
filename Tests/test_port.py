from unittest import TestCase
import port

class test_port(TestCase):
    def test_custom_weather(self):
        testportNone = port.Port(None, None, None, None, None, None)
        testportCity = port.Port(None, "Dordrecht", None, None, None, None)

        self.assertFalse(testportNone.check_custom_weather(500, 2))
        self.assertFalse(testportNone.check_custom_weather(5000, 10))
        self.assertFalse(testportNone.check_custom_weather(500, 10))
        self.assertIsNone(testportNone.check_custom_weather(None, None))
        self.assertIsNone(testportNone.check_custom_weather(None, 10))
        self.assertIsNone(testportNone.check_custom_weather(5000, None))
        self.assertIsNone(testportNone.check_custom_weather(5000, 2))
        self.assertTrue(testportCity.check_custom_weather(5000, 2))
