from friendzone.nwx2qcengine.pt2driver import pt2driver
from simde import Energy
import unittest

class NotAPT:
    pass

class Testpt2driver(unittest.TestCase):
    def test_pts_that_map_to_energy(self):
        for pt in [Energy()]:
            self.assertEqual(pt2driver(pt), 'energy')

    def test_bad_pt(self):
        self.assertRaises(Exception, pt2driver, NotAPT())
