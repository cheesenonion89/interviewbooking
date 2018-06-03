import unittest
from unittest import TestCase

from model import Interviewer
from service import db_service


class TestDBService(TestCase):
    def setUp(self):
        db_service.init_db()
        db_service.mockup()

    def test_get_next_id(self):
        next_id = db_service.get_next_id(Interviewer)
        self.assertEqual(next_id, 6)

    def tearDown(self):
        db_service.teardown_db()


if __name__ == "__main__":
    unittest.main()
