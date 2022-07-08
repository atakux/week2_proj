import unittest
from main import places_api,suggested_places_api,filter_categories,coordinates,get_weather

class TestFileName(unittest.TestCase):

    def setUp(self):
        pass

    def test_places_api(self):
        self.assertEqual(places_api("Denver",5,3),200)
    def test_test(self):
        self.assertEqual(0,0)

if __name__ == '__main__':
    unittest.main()
