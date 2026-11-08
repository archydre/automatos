"""
Testes unitários para a Máquina de Turing de L = {ww | w ∈ {0, 1}*}.
"""

import unittest
from turing_machine.languages.ww import create_ww_machine


class TestWW(unittest.TestCase):

    def setUp(self):
        self.tm = create_ww_machine()

    def test_accepted_strings(self):
        valid_cases = [
            "",                 # w = epsilon -> ww = epsilon
            "00",               # w = 0
            "11",               # w = 1
            "0000",             # w = 00
            "1111",             # w = 11
            "0101",             # w = 01
            "1010",             # w = 10
            "00110011",         # w = 0011
            "11001100",         # w = 1100
            "110110",           # w = 110
            "011011",           # w = 011
            "10101010",         # w = 1010
        ]
        for word in valid_cases:
            with self.subTest(word=word):
                self.tm.load(word)
                result = self.tm.run()
                self.assertTrue(result, f"A palavra '{word}' deveria ser ACEITA.")
                self.assertTrue(self.tm.halted)
                self.assertTrue(self.tm.accepted)
                self.assertFalse(self.tm.rejected)

    def test_rejected_strings(self):
        invalid_cases = [
            # Comprimentos ímpares (impossível ser ww)
            "0",
            "1",
            "000",
            "111",
            "010",
            "101",
            "01010",
            "10101",
            # Comprimentos pares porém w1 != w2
            "01",
            "10",
            "0011",
            "1100",
            "0110",
            "1001",
            "110111",
            "011010",
            "000001",
        ]
        for word in invalid_cases:
            with self.subTest(word=word):
                self.tm.load(word)
                result = self.tm.run()
                self.assertFalse(result, f"A palavra '{word}' deveria ser REJEITADA.")
                self.assertTrue(self.tm.halted)
                self.assertFalse(self.tm.accepted)
                self.assertTrue(self.tm.rejected)

    def test_invalid_alphabet_symbols(self):
        with self.assertRaises(ValueError):
            self.tm.load("abc")
        with self.assertRaises(ValueError):
            self.tm.load("012")


if __name__ == "__main__":
    unittest.main()
