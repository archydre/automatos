"""
Implementação da Fita Infinita Bidirecional para a Máquina de Turing.
Suporta movimentações L (Left), R (Right) e S (Stay), indexação em Z e símbolos em branco.
"""

from collections import defaultdict
from typing import Dict, Tuple, List, Optional


class Tape:
    """
    Fita infinita bidirecional da Máquina de Turing.
    
    A fita é indexada por inteiros relativos (Z), permitindo avanço e recuo ilimitados.
    Posições não gravadas contêm o símbolo de branco configurado.
    """

    def __init__(self, initial_content: str = "", blank_symbol: str = "_"):
        self.blank_symbol = blank_symbol
        self.cells: Dict[int, str] = defaultdict(lambda: self.blank_symbol)
        self.head: int = 0
        
        # Inicializa o conteúdo da fita a partir da posição 0
        for i, char in enumerate(initial_content):
            self.cells[i] = char

    def read(self) -> str:
        """Lê o símbolo na posição atual do cabeçote."""
        return self.cells[self.head]

    def write(self, symbol: str) -> None:
        """Escreve um símbolo na posição atual do cabeçote."""
        self.cells[self.head] = symbol

    def move(self, direction: str) -> None:
        """
        Move o cabeçote da fita:
        - 'R' ou 'r': Direita (+1)
        - 'L' ou 'l': Esquerda (-1)
        - 'S' ou 's': Parado / Sem movimento (+0)
        """
        dir_upper = direction.upper()
        if dir_upper == "R":
            self.head += 1
        elif dir_upper == "L":
            self.head -= 1
        elif dir_upper == "S":
            pass
        else:
            raise ValueError(f"Direção inválida: '{direction}'. Esperado 'L', 'R' ou 'S'.")

    def bounds(self, padding: int = 2) -> Tuple[int, int]:
        """
        Calcula o intervalo [min_pos, max_pos] que engloba todas as células não-brancas
        e a posição atual do cabeçote, com uma margem (padding) adicional.
        """
        non_blank_positions = [
            pos for pos, char in self.cells.items() if char != self.blank_symbol
        ]
        all_positions = non_blank_positions + [self.head]
        min_pos = min(all_positions) - padding
        max_pos = max(all_positions) + padding
        return min_pos, max_pos

    def get_slice(self, start: int, end: int) -> List[Tuple[int, str, bool]]:
        """
        Retorna uma lista de tuplas (posição, símbolo, é_cabeçote) para o intervalo [start, end].
        """
        result = []
        for pos in range(start, end + 1):
            symbol = self.cells[pos]
            is_head = (pos == self.head)
            result.append((pos, symbol, is_head))
        return result

    def copy(self) -> "Tape":
        """Cria um clone do estado atual da fita."""
        new_tape = Tape("", blank_symbol=self.blank_symbol)
        new_tape.cells = defaultdict(lambda: self.blank_symbol, dict(self.cells))
        new_tape.head = self.head
        return new_tape

    def to_dict(self) -> dict:
        """Serializa o estado da fita para representação JSON / Web."""
        min_pos, max_pos = self.bounds(padding=3)
        cells_list = [
            {"pos": pos, "symbol": self.cells[pos], "is_head": pos == self.head}
            for pos in range(min_pos, max_pos + 1)
        ]
        return {
            "head": self.head,
            "blank_symbol": self.blank_symbol,
            "min_pos": min_pos,
            "max_pos": max_pos,
            "cells": cells_list
        }

    def __repr__(self) -> str:
        min_pos, max_pos = self.bounds(padding=1)
        tape_str = "".join(self.cells[i] for i in range(min_pos, max_pos + 1))
        return f"Tape(head={self.head}, view='{tape_str}' [{min_pos}..{max_pos}])"
