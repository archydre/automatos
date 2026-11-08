"""
Testes unitários para a Máquina de Turing de L = {aⁿ bⁿ cⁿ | n ≥ 1}.
"""

import unittest
from turing_machine.languages.an_bn_cn import create_an_bn_cn_machine


class TestAnBnCn(unittest.TestCase):

    def setUp(self):
        self.tm = create_an_bn_cn_machine()

    def test_accepted_strings(self):
        valid_cases = [
            "abc",
            "aabbcc",
            "aaabbbccc",
            "aaaabbbbcccc",
            "aaaaabbbbbccccc",
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
            "",                 # n >= 1 (vazia deve ser rejeitada)
            "a",
            "b",
            "c",
            "ab",
            "bc",
            "ac",
            "aabb",
            "bbcc",
            "aacc",
            "aabbc",            # Menos 'c's
            "aabcc",            # Menos 'b's
            "abbcc",            # Menos 'a's
            "aaabbcc",
            "aabbbccc",
            "cba",              # Ordem invertida
            "bac",
            "abcabc",
            "aaabbbcccc",       # 'c' a mais
            "aaabbbbccc",       # 'b' a mais
            "aaaabbbccc",       # 'a' a mais
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
            self.tm.load("abcd")
        with self.assertRaises(ValueError):
            self.tm.load("01")


if __name__ == "__main__":
    unittest.main()
