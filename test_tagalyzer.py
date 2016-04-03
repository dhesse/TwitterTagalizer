import tagalizer.daemon as td
import unittest
from collections import defaultdict

class MockDB(object):
    """Mongo database that can store stuff..."""
    def __init__(self):
        self.objects = []
    def find(self):
        if self.objects == []:
            return None
        return self.objects
    def insert_one(self, what):
        self.objects.append(what)

class MongoMock(object):
    """Mock object to simulate a MonoClient instance."""
    def __init__(self, db=None, level=0):
        self.children = defaultdict(
            lambda: MongoMock(db, level + 1) if level < 1 else db or MockDB())
    def __getattr__(self, name):
        return self.children[name]

class TestMongoMock(unittest.TestCase):
    """Tests the MongoDB mock class."""
    def test_mock_collection_is_mongo_mock(self):
        self.assertEqual(type(MongoMock().foo), MongoMock)
    def test_mock_collection_produces_mock_dbs(self):
        self.assertEqual(type(MongoMock().foo.bar), MockDB)
    def test_returns_None(self):
        self.assertEqual(MongoMock().foo.bar.find(), None)

class TestConfigManagement(unittest.TestCase):
    """Tests around retrieving and storing configuration."""
    def test_get_config_throws_if_no_config_found(self):
        with self.assertRaises(td.ConfigError):
            td.getConfig(MongoMock())
    def test_get_config_collects_options(self):
        db = MockDB()
        db.insert_one({'option_name': 'foo', 'value': 2})
        db.insert_one({'option_name': 'bar', 'value': 3})
        self.assertEqual(td.getConfig(MongoMock(db)),
                         {'foo': 2, 'bar': 3})
    def test_get_config_throws_if_options_exists_twice(self):
        db = MockDB()
        db.insert_one({'option_name': 'foo', 'value': 2})
        db.insert_one({'option_name': 'foo', 'value': 3})
        with self.assertRaises(td.ConfigError):
            td.getConfig(MongoMock(db))
    def test_store_config(self):
        db = MockDB()
        td.storeConfig(MongoMock(db), {'foo': 1, 'bar': 2})
        self.assertEqual(db.objects, [{'option_name': 'foo', 'value': 1},
                                      {'option_name': 'bar', 'value': 2}])

if __name__ == '__main__':
    unittest.main()
