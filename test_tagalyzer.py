import tagalizer.daemon as td
import unittest
from collections import defaultdict

class MockDB(object):
    """Mock object to simulate a MongoDB database."""
    def find(*args, **kwargs):
        return None

class MongoMock(object):
    """Mock object to simulate a MonoClient instance."""
    def __init__(self, level=0):
        self.level = level
        self.children = defaultdict(
            lambda: MongoMock(self.level + 1) if self.level < 1 else MockDB())
    def __getattr__(self, name):
        return self.children[name]

class TestMongoMock(unittest.TestCase):
    """Tests the MongoDB mock class."""
    def test_mock_class_has_level_zero(self):
        self.assertEqual(MongoMock().level, 0)
    def test_mock_collection_has_level_one(self):
        self.assertEqual(MongoMock().foo.level, 1)
    def test_mock_collection_produces_mock_dbs(self):
        self.assertEqual(type(MongoMock().foo.bar), MockDB)
    def test_returns_None(self):
        self.assertEqual(MongoMock().foo.bar.find(), None)

class TestConfigManagement(unittest.TestCase):
    """Tests around retrieving and storing configuration."""
    def test_get_config_throws_if_no_config_found(self):
        with self.assertRaises(td.ConfigError):
            td.getConfig(MongoMock())

if __name__ == '__main__':
    unittest.main()
