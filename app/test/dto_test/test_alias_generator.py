import unittest

from dto.base_dto import alias_generator


class TestAliasGenerator(unittest.TestCase):
    def test_alias_generator(self):
        self.assertEqual(alias_generator("created_at"), "createdAt")
        self.assertEqual(alias_generator("is_completed"), "isCompleted")
        self.assertEqual(alias_generator("_is_completed_true__"), "_isCompletedTrue")
        self.assertEqual(alias_generator("is_completed_No"), "isCompletedNo")
