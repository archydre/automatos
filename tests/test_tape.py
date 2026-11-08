"""
Testes unitários para a Fita Infinita (Tape).
"""

import unittest
from turing_machine.tape import Tape


class TestTape(unittest.TestCase):

    def test_initialization(self):
        tape = Tape("abc", blank_symbol="_")
        self.assertEqual(tape.head, 0)
        self.assertEqual(tape.read(), "a")
        self.assertEqual(tape.blank_symbol, "_")

    def test_empty_tape(self):
        tape = Tape("", blank_symbol="_")
        self.assertEqual(tape.head, 0)
        self.assertEqual(tape.read(), "_")

    def test_move_right(self):
        tape = Tape("abc", blank_symbol="_")
        self.assertEqual(tape.read(), "a")
        tape.move("R")
        self.assertEqual(tape.head, 1)
        self.assertEqual(tape.read(), "b")
        tape.move("r")  # Case insensitive
        self.assertEqual(tape.head, 2)
        self.assertEqual(tape.read(), "c")
        tape.move("R")
        self.assertEqual(tape.head, 3)
        self.assertEqual(tape.read(), "_")  # Célula não inicializada é branco

    def test_move_left_into_negatives(self):
        tape = Tape("abc", blank_symbol="_")
        tape.move("L")
        self.assertEqual(tape.head, -1)
        self.assertEqual(tape.read(), "_")
        tape.write("Z")
        self.assertEqual(tape.read(), "Z")
        tape.move("l")
        self.assertEqual(tape.head, -2)
        self.assertEqual(tape.read(), "_")
        tape.move("R")
        self.assertEqual(tape.head, -1)
        self.assertEqual(tape.read(), "Z")

    def test_move_stay(self):
        tape = Tape("abc", blank_symbol="_")
        pos_before = tape.head
        tape.move("S")
        self.assertEqual(tape.head, pos_before)
        self.assertEqual(tape.read(), "a")
        tape.move("s")
        self.assertEqual(tape.head, pos_before)

    def test_invalid_direction(self):
        tape = Tape("abc")
        with self.assertRaises(ValueError):
            tape.move("X")

    def test_write_and_read(self):
        tape = Tape("hello")
        tape.write("H")
        self.assertEqual(tape.read(), "H")
        tape.move("R")
        tape.write("E")
        self.assertEqual(tape.read(), "E")

    def test_bounds(self):
        tape = Tape("abc", blank_symbol="_")
        min_p, max_p = tape.bounds(padding=0)
        self.assertEqual(min_p, 0)
        self.assertEqual(max_p, 2)

        tape.move("L")
        tape.move("L")  # head at -2
        min_p, max_p = tape.bounds(padding=0)
        self.assertEqual(min_p, -2)
        self.assertEqual(max_p, 2)

    def test_to_dict_and_copy(self):
        tape = Tape("ab", blank_symbol="_")
        tape_dict = tape.to_dict()
        self.assertIn("cells", tape_dict)
        self.assertIn("head", tape_dict)
        self.assertEqual(tape_dict["head"], 0)

        copy_tape = tape.copy()
        self.assertEqual(copy_tape.read(), "a")
        copy_tape.write("X")
        self.assertEqual(copy_tape.read(), "X")
        self.assertEqual(tape.read(), "a")  # Original não alterada


if __name__ == "__main__":
    unittest.main()
