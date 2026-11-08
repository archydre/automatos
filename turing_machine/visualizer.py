"""
Visualizador de Fita e Rastreamento Minimalista para o Terminal (CLI).
Utiliza caracteres refinados de Box Drawing (Unicode) para um design limpo e elegante.
"""

from typing import Optional
from turing_machine.machine import TuringMachine, StepSnapshot


class Visualizer:
    """Formatador de visualização minimalista no terminal para a Máquina de Turing."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    INDIGO = "\033[38;5;99m"
    HEAD_STYLE = "\033[1m\033[97m\033[48;5;61m"

    @classmethod
    def render_tape_line(cls, tape_dict: dict) -> str:
        """
        Renderiza a fita no formato minimalista usando Box Drawing:
        ┌─────┬─────┬─────┐
        │  a  │  b  │  c  │
        └─────┴─────┴─────┘
                 ▲ [q]
        """
        head = tape_dict["head"]
        cells_map = {item["pos"]: item["symbol"] for item in tape_dict["cells"]}
        blank = tape_dict["blank_symbol"]

        min_pos = tape_dict["min_pos"]
        max_pos = tape_dict["max_pos"]
        count = max_pos - min_pos + 1

        # Linha de índices
        idx_line = "      "
        # Borda superior
        top_border = "    ┌" + "─────┬" * (count - 1) + "─────┐"
        # Linha das células
        cells_line = "    │"
        # Borda inferior
        bot_border = "    └" + "─────┴" * (count - 1) + "─────┘"
        # Apontador do cabeçote
        ptr_line = "     "

        for p in range(min_pos, max_pos + 1):
            sym = cells_map.get(p, blank)
            display_sym = "⊔" if sym == "_" else sym
            is_head = (p == head)

            idx_line += f"{cls.DIM}{p:^6}{cls.RESET}"

            if is_head:
                cells_line += f"{cls.HEAD_STYLE}  {display_sym}  {cls.RESET}│"
                ptr_line += f"{cls.CYAN}{cls.BOLD}  ▲   {cls.RESET}"
            else:
                cells_line += f"  {display_sym}  │"
                ptr_line += "      "

        return f"{idx_line}\n{top_border}\n{cells_line}\n{bot_border}\n{ptr_line}"

    @classmethod
    def render_step(cls, snapshot: StepSnapshot, show_tape: bool = True) -> str:
        """Renderiza um único snapshot da execução em formato minimalista."""
        step_str = f"{cls.DIM}#{snapshot.step_num:03d}{cls.RESET}"
        state_str = f"q: {cls.CYAN}{cls.BOLD}{snapshot.state}{cls.RESET}"
        head_str = f"pos: {cls.INDIGO}{snapshot.head_pos}{cls.RESET} ('{snapshot.read_symbol}')"

        header = f"{step_str}  •  {state_str}  •  {head_str}"
        msg = f"{cls.DIM}Regra:{cls.RESET} {snapshot.message}"
        explain = f"{cls.YELLOW}Comentário:{cls.RESET} {snapshot.explanation}" if snapshot.explanation else ""
        intent = f"{cls.DIM}Objetivo:{cls.RESET} {snapshot.intent}" if snapshot.intent else ""

        body_lines = [header, msg]
        if explain:
            body_lines.append(explain)
        if intent:
            body_lines.append(intent)

        info_block = "\n".join(body_lines)

        if snapshot.halted:
            if snapshot.accepted:
                status = f"\n{cls.GREEN}{cls.BOLD}✓ STATUS: PALAVRA ACEITA{cls.RESET}"
            else:
                status = f"\n{cls.RED}{cls.BOLD}✗ STATUS: PALAVRA REJEITADA{cls.RESET}"
        else:
            status = ""

        if show_tape:
            tape_view = cls.render_tape_line(snapshot.tape_dict)
            return f"\n{info_block}\n{tape_view}{status}"
        return f"{info_block}{status}"

    @classmethod
    def print_summary(cls, tm: TuringMachine, word: str) -> None:
        """Exibe o resumo consolidado em formato minimalista."""
        print("\n" + "─" * 55)
        print(f"{cls.BOLD}RESUMO DA EXECUÇÃO{cls.RESET}")
        print("─" * 55)
        print(f"Linguagem : {tm.name}")
        print(f"Entrada   : '{word}' (|w| = {len(word)})")
        print(f"Passos    : {tm.step_count}")
        print(f"Estado    : {tm.current_state}")
        
        if tm.accepted:
            print(f"Veredito  : {cls.GREEN}{cls.BOLD}ACEITA (Pertence a L){cls.RESET}")
        else:
            print(f"Veredito  : {cls.RED}{cls.BOLD}REJEITADA (Não pertence a L){cls.RESET}")
        print("─" * 55 + "\n")
