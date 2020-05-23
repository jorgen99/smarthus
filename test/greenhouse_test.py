import unittest
import sys
sys.path.append("../events")
from greenhouse import apa


class GreenhouseTestCase(unittest.TestCase):
    def test_setup(self):
        hi = apa("Jugge")
        self.assertEqual(hi, "Hej Jugge")


if __name__ == '__main__':
    unittest.main()
