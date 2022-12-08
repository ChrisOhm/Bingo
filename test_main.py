# @author Christoffer Öhman

from unittest import TestCase
import data
import main


class Test(TestCase):
    def test_get_loosing_score(self):
        loosing_score = main.get_loosing_score(data.testDrawNumbers, main.get_bingo_boards(data.testBoardString))
        self.assertEqual(loosing_score, 1924)
