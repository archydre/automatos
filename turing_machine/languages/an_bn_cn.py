"""
Máquina de Turing para a Linguagem L = {aⁿ bⁿ cⁿ | n ≥ 1}.
Linguagem clássica sensível ao contexto (não livre de contexto).
Inclui comentários didáticos a cada transição e fundamentação teórica.
"""

from turing_machine.machine import TuringMachine


def create_an_bn_cn_machine() -> TuringMachine:
    """
    Constrói a Máquina de Turing determinística para reconhecer L = {aⁿ bⁿ cⁿ | n ≥ 1}.
    """
    states = {"q0", "q1", "q2", "q3", "q5", "q6", "q_accept", "q_reject"}
    input_alphabet = {"a", "b", "c"}
    tape_alphabet = {"a", "b", "c", "X", "Y", "Z", "_"}
    initial_state = "q0"
    blank_symbol = "_"
    accept_states = {"q_accept"}
    reject_states = {"q_reject"}

    transitions = {
        # Estado q0: Marca o próximo 'a' com 'X' ou inicia verificação se encontrar 'Y'
        ("q0", "a"): ("q1", "X", "R"),
        ("q0", "Y"): ("q5", "Y", "R"),

        # Estado q1: Procura o 'b' correspondente
        ("q1", "a"): ("q1", "a", "R"),
        ("q1", "Y"): ("q1", "Y", "R"),
        ("q1", "b"): ("q2", "Y", "R"),

        # Estado q2: Procura o 'c' correspondente
        ("q2", "b"): ("q2", "b", "R"),
        ("q2", "Z"): ("q2", "Z", "R"),
        ("q2", "c"): ("q3", "Z", "L"),

        # Estado q3: Retorna à esquerda até o último 'X' marcado
        ("q3", "Z"): ("q3", "Z", "L"),
        ("q3", "b"): ("q3", "b", "L"),
        ("q3", "Y"): ("q3", "Y", "L"),
        ("q3", "a"): ("q3", "a", "L"),
        ("q3", "X"): ("q0", "X", "R"),

        # Estado q5: Verificação dos 'Y's restantes após todos os 'a's terem sido consumidos
        ("q5", "Y"): ("q5", "Y", "R"),
        ("q5", "Z"): ("q6", "Z", "R"),

        # Estado q6: Verificação dos 'Z's restantes até o final da fita
        ("q6", "Z"): ("q6", "Z", "R"),
        ("q6", "_"): ("q_accept", "_", "S"),
    }

    # Comentários didáticos detalhados para cada transição (resolução comentada)
    explanations = {
        ("q0", "a"): "Leu 'a' na pos {pos}: gravou 'X' (1º membro do trio registrado). Mudo para q1 e avanço à direita para encontrar o 'b' equivalente.",
        ("q0", "Y"): "Leu 'Y' na pos {pos}: todos os 'a's da palavra já foram marcados como 'X'! Mudo para q5 para verificar se todos os 'b' e 'c' também foram emparelhados.",
        
        ("q1", "a"): "Leu 'a' na pos {pos}: pulando símbolos 'a' ainda não processados em direção ao bloco de 'b's.",
        ("q1", "Y"): "Leu 'Y' na pos {pos}: pulando 'Y' (já marcado em rodadas anteriores) para alcançar o próximo 'b' livre.",
        ("q1", "b"): "Leu 'b' na pos {pos}: ENCONTROU O 'b'! Gravou 'Y' (2º membro do trio registrado). Mudo para q2 e avanço à direita em busca do 'c'.",

        ("q2", "b"): "Leu 'b' na pos {pos}: pulando símbolos 'b' ainda não processados em direção ao bloco de 'c's.",
        ("q2", "Z"): "Leu 'Z' na pos {pos}: pulando 'Z' (já marcado em rodadas anteriores) para alcançar o próximo 'c' livre.",
        ("q2", "c"): "Leu 'c' na pos {pos}: ENCONTROU O 'c'! Gravou 'Z'. TRIO COMPLETO (X, Y, Z)! Mudo para q3 e rebobino para a esquerda até o último 'X'.",

        ("q3", "Z"): "Leu 'Z' na pos {pos}: rebobinando a fita para a esquerda...",
        ("q3", "b"): "Leu 'b' na pos {pos}: rebobinando a fita para a esquerda...",
        ("q3", "Y"): "Leu 'Y' na pos {pos}: rebobinando a fita para a esquerda...",
        ("q3", "a"): "Leu 'a' na pos {pos}: rebobinando a fita para a esquerda...",
        ("q3", "X"): "Leu 'X' na pos {pos}: chegou de volta ao último 'X' marcado! Dou 1 passo à direita e volto ao estado q0 para processar o próximo 'a'.",

        ("q5", "Y"): "Leu 'Y' na pos {pos}: validando que todos os 'b's foram devidamente marcados como 'Y'...",
        ("q5", "Z"): "Leu 'Z' na pos {pos}: passou pelos 'b's marcados e alcançou o bloco de 'c's marcados ('Z'). Mudo para q6 para validar até o fim da fita.",

        ("q6", "Z"): "Leu 'Z' na pos {pos}: validando que todos os 'c's foram devidamente marcados como 'Z'...",
        ("q6", "_"): "Leu '⊔' (branco): final da fita alcançado sem sobras nem símbolos fora de ordem! Todos os trios (a, b, c) têm cardinalidades idênticas. PALAVRA ACEITA!",
    }

    # Intenção / objetivo de cada estado
    intents = {
        "q0": "Objetivo: Encontrar o próximo 'a' para formar um novo trio (a, b, c) ou iniciar a checagem final.",
        "q1": "Objetivo: Varrendo a fita à direita em busca do 'b' correspondente ao 'a' marcado.",
        "q2": "Objetivo: Varrendo a fita à direita em busca do 'c' correspondente ao trio.",
        "q3": "Objetivo: Trio completo! Rebobinando o cabeçote para a esquerda até a última marcação 'X'.",
        "q5": "Objetivo: Checagem final: garantindo que não restam 'b's desmarcados.",
        "q6": "Objetivo: Checagem final: garantindo que não restam 'c's desmarcados até o branco.",
        "q_accept": "Conclusão: Palavra formalmente aceita! A cadeia pertence à linguagem L = {aⁿ bⁿ cⁿ}.",
        "q_reject": "Conclusão: Palavra rejeitada! A cadeia não respeita a proporção ou ordem n de a, b e c.",
    }

    # Motivos de rejeição (quando a máquina trava por falta de transição)
    rejection_reasons = {
        ("q0", "_"): "A fita começou vazia. Como a linguagem exige n ≥ 1, a palavra vazia (ε) é rejeitada.",
        ("q0", "b"): "Encontrou 'b' sem 'a' anterior correspondente (ordem errada ou excesso de b's). Rejeitada.",
        ("q0", "c"): "Encontrou 'c' antes de ter 'a' ou 'b' (ordem errada). Rejeitada.",
        ("q1", "_"): "A fita acabou enquanto procurava um 'b'. Existem menos 'b's do que 'a's na palavra. Rejeitada.",
        ("q1", "Z"): "Encontrou 'Z' antes de encontrar um 'b' desmarcado. Faltam 'b's para emparelhar com os 'a's. Rejeitada.",
        ("q2", "_"): "A fita acabou enquanto procurava um 'c'. Existem menos 'c's do que 'a's e 'b's na palavra. Rejeitada.",
        ("q5", "b"): "Encontrou um 'b' não marcado após o término dos 'a's. A quantidade de 'b's excede a de 'a's. Rejeitada.",
        ("q5", "_"): "A fita terminou sem nenhum 'c' marcado (não há blocos de 'c'). Rejeitada.",
        ("q6", "a"): "Encontrou 'a' fora de ordem no final da palavra. Rejeitada.",
        ("q6", "b"): "Encontrou 'b' fora de ordem no final da palavra. Rejeitada.",
        ("q6", "Y"): "Encontrou 'Y' fora de ordem na zona dos 'c's. Rejeitada.",
    }

    theory_guide = {
        "title": "Linguagem L = {aⁿ bⁿ cⁿ | n ≥ 1}",
        "concept": "Esta é a linguagem não livre de contexto mais famosa da Teoria da Computação. Ela exige que o número de 'a's, 'b's e 'c's seja rigorosamente o mesmo e na ordem correta (ex: 'aabbcc' com n=2). Autômatos com Pilha (AP) não conseguem reconhecê-la porque uma única pilha só consegue comparar dois contadores (como aⁿ bⁿ).",
        "how_it_works": [
            "1. Memória de Trabalho: A Máquina de Turing usa a fita infinita para marcar símbolos consumidos sem perder a posição.",
            "2. Ciclo de Pareamento: A cada ciclo, ela marca um 'a' como 'X', procura o primeiro 'b' e marca como 'Y', procura o primeiro 'c' e marca como 'Z'.",
            "3. Rebobinamento: Ao fechar o trio (X, Y, Z), o cabeçote volta para trás até o último 'X' para repetir o ciclo no próximo 'a'.",
            "4. Validação: Quando acabam os 'a's, ela confere se sobrou algum 'b' ou 'c' desmarcado. Se a fita terminar em branco, a palavra é aceita!"
        ]
    }

    return TuringMachine(
        states=states,
        input_alphabet=input_alphabet,
        tape_alphabet=tape_alphabet,
        transitions=transitions,
        initial_state=initial_state,
        blank_symbol=blank_symbol,
        accept_states=accept_states,
        reject_states=reject_states,
        name="L = {aⁿ bⁿ cⁿ | n ≥ 1}",
        description="Reconhecedor da linguagem não livre de contexto clássica aⁿbⁿcⁿ.",
        explanations=explanations,
        intents=intents,
        rejection_reasons=rejection_reasons,
        theory_guide=theory_guide
    )
