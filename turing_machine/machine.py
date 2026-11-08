"""
Mecanismo de Execução Formal da Máquina de Turing Determinística de Decisão.
"""

from typing import Dict, Tuple, Set, Optional, List, Any
from dataclasses import dataclass, asdict
from turing_machine.tape import Tape


@dataclass
class Transition:
    next_state: str
    write_symbol: str
    direction: str  # 'L', 'R', ou 'S'

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class StepSnapshot:
    step_num: int
    state: str
    head_pos: int
    read_symbol: str
    transition: Optional[Transition]
    halted: bool
    accepted: bool
    rejected: bool
    tape_dict: dict
    message: str
    explanation: str = ""
    intent: str = ""
    formal_rule: str = ""

    def to_dict(self) -> dict:
        res = asdict(self)
        if self.transition:
            res["transition"] = self.transition.to_dict()
        return res


class TuringMachine:
    """
    Máquina de Turing Determinística (Decisora).
    Formalizada pela 7-tupla: (Q, Sigma, Gamma, delta, q0, B, F_accept, [F_reject])
    """

    def __init__(
        self,
        states: Set[str],
        input_alphabet: Set[str],
        tape_alphabet: Set[str],
        transitions: Dict[Tuple[str, str], Tuple[str, str, str]],
        initial_state: str,
        blank_symbol: str = "_",
        accept_states: Optional[Set[str]] = None,
        reject_states: Optional[Set[str]] = None,
        name: str = "Turing Machine",
        description: str = "",
        explanations: Optional[Dict[Tuple[str, str], str]] = None,
        intents: Optional[Dict[str, str]] = None,
        rejection_reasons: Optional[Dict[Tuple[str, str], str]] = None,
        theory_guide: Optional[dict] = None
    ):
        self.name = name
        self.description = description
        self.states = set(states)
        self.input_alphabet = set(input_alphabet)
        self.tape_alphabet = set(tape_alphabet)
        self.blank_symbol = blank_symbol
        self.initial_state = initial_state
        self.accept_states = set(accept_states or {"q_accept", "qa"})
        self.reject_states = set(reject_states or {"q_reject", "qr"})
        self.explanations = explanations or {}
        self.intents = intents or {}
        self.rejection_reasons = rejection_reasons or {}
        self.theory_guide = theory_guide or {}

        # Normaliza transições para Transition dataclass
        self.transitions: Dict[Tuple[str, str], Transition] = {}
        for (st, sym), (nxt_st, wr_sym, direct) in transitions.items():
            direct_upper = direct.upper()
            if direct_upper not in {"L", "R", "S"}:
                raise ValueError(f"Direção inválida '{direct}' na transição ({st}, {sym}).")
            self.transitions[(st, sym)] = Transition(
                next_state=nxt_st,
                write_symbol=wr_sym,
                direction=direct_upper
            )

        # Estado de execução
        self.tape: Tape = Tape("", blank_symbol=self.blank_symbol)
        self.current_state: str = self.initial_state
        self.step_count: int = 0
        self.halted: bool = False
        self.accepted: bool = False
        self.rejected: bool = False
        self.trace: List[StepSnapshot] = []

    def load(self, input_string: str) -> None:
        """Carrega uma nova palavra de entrada na fita e reinicia o estado."""
        for ch in input_string:
            if ch not in self.input_alphabet:
                raise ValueError(
                    f"Símbolo '{ch}' da entrada não pertence ao alfabeto de entrada {self.input_alphabet}."
                )

        self.tape = Tape(input_string, blank_symbol=self.blank_symbol)
        self.current_state = self.initial_state
        self.step_count = 0
        self.halted = False
        self.accepted = False
        self.rejected = False
        self.trace = []

        initial_explanation = f"Entrada '{input_string}' carregada na fita a partir da posição 0. Cabeçote no início." if input_string else "Entrada vazia (ε) carregada na fita."
        initial_intent = self.intents.get(self.initial_state, "Pronto para iniciar.")

        if self.current_state in self.accept_states:
            self.halted = True
            self.accepted = True
        elif self.current_state in self.reject_states:
            self.halted = True
            self.rejected = True

        self.trace.append(self._create_snapshot(
            transition=None,
            message="Estado inicial carregado.",
            explanation=initial_explanation,
            intent=initial_intent,
            formal_rule=f"Estado inicial: {self.initial_state}"
        ))

    def step(self) -> StepSnapshot:
        """
        Executa exatamente uma transição da Máquina de Turing.
        Retorna o snapshot resultante da transição com comentário didático.
        """
        if self.halted:
            return self.trace[-1] if self.trace else self._create_snapshot(None, "Máquina já parada.")

        read_sym = self.tape.read()
        rule_key = (self.current_state, read_sym)

        if rule_key not in self.transitions:
            self.halted = True
            self.rejected = True
            reason = self.rejection_reasons.get(
                rule_key,
                f"Nenhuma regra definida para o estado {self.current_state} lendo '{read_sym}'. Parada por travamento."
            )
            snapshot = self._create_snapshot(
                transition=None,
                message=f"Travamento: sem transição para ({self.current_state}, '{read_sym}'). Rejeitada.",
                explanation=reason,
                intent="Parada da máquina (Palavra Rejeitada).",
                formal_rule=f"δ({self.current_state}, '{read_sym}') = Indefinida"
            )
            self.trace.append(snapshot)
            return snapshot

        trans = self.transitions[rule_key]
        prev_state = self.current_state
        head_pos = self.tape.head

        # Aplica a escrita na fita
        self.tape.write(trans.write_symbol)

        # Aplica o movimento do cabeçote (L, R, S)
        self.tape.move(trans.direction)

        # Atualiza o estado
        self.current_state = trans.next_state
        self.step_count += 1

        # Resolução comentada da transição
        template = self.explanations.get(
            rule_key,
            f"Leu '{read_sym}' no estado {prev_state}: escreveu '{trans.write_symbol}', moveu para {trans.direction} e entrou em {trans.next_state}."
        )
        explanation = template.format(pos=head_pos)

        intent = self.intents.get(self.current_state, f"Estado {self.current_state}")
        formal_rule = f"δ({prev_state}, '{read_sym}') = ({trans.next_state}, '{trans.write_symbol}', {trans.direction})"

        # Avalia estado de parada
        if self.current_state in self.accept_states:
            self.halted = True
            self.accepted = True
            msg = f"Palavra ACEITA no passo {self.step_count} (estado {self.current_state})."
            intent = "Conclusão: Palavra Válida! Reconhecida pela Máquina de Turing."
        elif self.current_state in self.reject_states:
            self.halted = True
            self.rejected = True
            msg = f"Palavra REJEITADA no passo {self.step_count} (estado {self.current_state})."
            intent = "Conclusão: Palavra Inválida! Rejeitada pela Máquina de Turing."
        else:
            msg = formal_rule

        snapshot = self._create_snapshot(
            transition=trans,
            message=msg,
            explanation=explanation,
            intent=intent,
            formal_rule=formal_rule
        )
        self.trace.append(snapshot)
        return snapshot

    def run(self, max_steps: int = 10000) -> bool:
        """Executa a máquina até parada."""
        while not self.halted and self.step_count < max_steps:
            self.step()

        if self.step_count >= max_steps and not self.halted:
            self.halted = True
            self.rejected = True
            msg = f"Limite de {max_steps} passos atingido sem parada."
            self.trace.append(self._create_snapshot(
                None,
                msg,
                explanation=f"A máquina excedeu o limite máximo de {max_steps} passos.",
                intent="Parada forçada por limite de passos."
            ))

        return self.accepted

    def _create_snapshot(
        self,
        transition: Optional[Transition],
        message: str,
        explanation: str = "",
        intent: str = "",
        formal_rule: str = ""
    ) -> StepSnapshot:
        return StepSnapshot(
            step_num=self.step_count,
            state=self.current_state,
            head_pos=self.tape.head,
            read_symbol=self.tape.read(),
            transition=transition,
            halted=self.halted,
            accepted=self.accepted,
            rejected=self.rejected,
            tape_dict=self.tape.to_dict(),
            message=message,
            explanation=explanation,
            intent=intent,
            formal_rule=formal_rule
        )

    def get_transitions_table(self) -> List[dict]:
        """Exporta a tabela de transição em formato amigável para exibição."""
        rows = []
        for (st, sym), tr in sorted(self.transitions.items()):
            rows.append({
                "from_state": st,
                "read_symbol": sym,
                "to_state": tr.next_state,
                "write_symbol": tr.write_symbol,
                "direction": tr.direction
            })
        return rows
