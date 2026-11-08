"""
Máquina de Turing para a Linguagem L = {ww | w ∈ {0, 1}*}.
Linguagem clássica não livre de contexto sobre o alfabeto binário.
Inclui comentários didáticos a cada transição e fundamentação teórica.
"""

from turing_machine.machine import TuringMachine


def create_ww_machine() -> TuringMachine:
    """
    Constrói a Máquina de Turing determinística para reconhecer L = {ww | w ∈ {0, 1}*}.
    """
    states = {
        "q0",
        "q_seek_right",
        "q_mark_right",
        "q_seek_left",
        "q_mark_left",
        "q_stage2_rewind_start",
        "q_match_loop",
        "q_match_find_C",
        "q_match_find_D",
        "q_match_rewind",
        "q_verify_all_matched",
        "q_accept",
        "q_reject",
    }
    input_alphabet = {"0", "1"}
    tape_alphabet = {"0", "1", "A", "B", "C", "D", "*", "#", "_"}
    initial_state = "q0"
    blank_symbol = "_"
    accept_states = {"q_accept"}
    reject_states = {"q_reject"}

    transitions = {
        # --- ESTÁGIO 1: LOCALIZAÇÃO DO PONTO MÉDIO (PARIDADE) ---
        ("q0", "_"): ("q_accept", "_", "S"),
        ("q0", "0"): ("q_seek_right", "A", "R"),
        ("q0", "1"): ("q_seek_right", "B", "R"),

        ("q_seek_right", "0"): ("q_seek_right", "0", "R"),
        ("q_seek_right", "1"): ("q_seek_right", "1", "R"),
        ("q_seek_right", "_"): ("q_mark_right", "_", "L"),
        ("q_seek_right", "C"): ("q_mark_right", "C", "L"),
        ("q_seek_right", "D"): ("q_mark_right", "D", "L"),

        ("q_mark_right", "0"): ("q_seek_left", "C", "L"),
        ("q_mark_right", "1"): ("q_seek_left", "D", "L"),

        ("q_seek_left", "0"): ("q_seek_left", "0", "L"),
        ("q_seek_left", "1"): ("q_seek_left", "1", "L"),
        ("q_seek_left", "A"): ("q_mark_left", "A", "R"),
        ("q_seek_left", "B"): ("q_mark_left", "B", "R"),

        ("q_mark_left", "0"): ("q_seek_right", "A", "R"),
        ("q_mark_left", "1"): ("q_seek_right", "B", "R"),
        ("q_mark_left", "C"): ("q_stage2_rewind_start", "C", "L"),
        ("q_mark_left", "D"): ("q_stage2_rewind_start", "D", "L"),

        # --- ESTÁGIO 2: REBOBINAR AO INÍCIO DA FITA ---
        ("q_stage2_rewind_start", "A"): ("q_stage2_rewind_start", "A", "L"),
        ("q_stage2_rewind_start", "B"): ("q_stage2_rewind_start", "B", "L"),
        ("q_stage2_rewind_start", "_"): ("q_match_loop", "_", "R"),

        # --- ESTÁGIO 2: VERIFICAÇÃO DE CORRESPONDÊNCIA (w1 == w2) ---
        ("q_match_loop", "*"): ("q_match_loop", "*", "R"),
        ("q_match_loop", "A"): ("q_match_find_C", "*", "R"),
        ("q_match_loop", "B"): ("q_match_find_D", "*", "R"),
        ("q_match_loop", "#"): ("q_verify_all_matched", "#", "R"),

        ("q_match_find_C", "A"): ("q_match_find_C", "A", "R"),
        ("q_match_find_C", "B"): ("q_match_find_C", "B", "R"),
        ("q_match_find_C", "#"): ("q_match_find_C", "#", "R"),
        ("q_match_find_C", "C"): ("q_match_rewind", "#", "L"),

        ("q_match_find_D", "A"): ("q_match_find_D", "A", "R"),
        ("q_match_find_D", "B"): ("q_match_find_D", "B", "R"),
        ("q_match_find_D", "#"): ("q_match_find_D", "#", "R"),
        ("q_match_find_D", "D"): ("q_match_rewind", "#", "L"),

        ("q_match_rewind", "#"): ("q_match_rewind", "#", "L"),
        ("q_match_rewind", "C"): ("q_match_rewind", "C", "L"),
        ("q_match_rewind", "D"): ("q_match_rewind", "D", "L"),
        ("q_match_rewind", "A"): ("q_match_rewind", "A", "L"),
        ("q_match_rewind", "B"): ("q_match_rewind", "B", "L"),
        ("q_match_rewind", "*"): ("q_match_loop", "*", "R"),

        ("q_verify_all_matched", "#"): ("q_verify_all_matched", "#", "R"),
        ("q_verify_all_matched", "_"): ("q_accept", "_", "S"),
    }

    # Comentários didáticos da execução passo a passo
    explanations = {
        ("q0", "_"): "Palavra vazia (ε): Para w = ε, ww = ε. A cadeia vazia pertence formalmente à linguagem ww. PALAVRA ACEITA!",
        ("q0", "0"): "Leu '0' no início na pos {pos}: marcou como 'A' (lembrando que a 1ª metade começa com 0). Avança até o fim da fita para marcar o extremo oposto.",
        ("q0", "1"): "Leu '1' no início na pos {pos}: marcou como 'B' (lembrando que a 1ª metade começa com 1). Avança até o fim da fita para marcar o extremo oposto.",

        ("q_seek_right", "0"): "Leu '0' na pos {pos}: avançando à direita em busca do fim da cadeia...",
        ("q_seek_right", "1"): "Leu '1' na pos {pos}: avançando à direita em busca do fim da cadeia...",
        ("q_seek_right", "_"): "Leu '⊔' na pos {pos}: atingiu o final da cadeia! Dá 1 passo à esquerda para marcar o último símbolo.",
        ("q_seek_right", "C"): "Leu 'C' na pos {pos}: atingiu a fronteira de símbolos já marcados na direita. Dá 1 passo à esquerda para marcar.",
        ("q_seek_right", "D"): "Leu 'D' na pos {pos}: atingiu a fronteira de símbolos já marcados na direita. Dá 1 passo à esquerda para marcar.",

        ("q_mark_right", "0"): "Leu '0' na pos {pos} no extremo direito: gravou 'C' (lembrando que é 0 na 2ª metade). Pareamento concluído! Volta à esquerda.",
        ("q_mark_right", "1"): "Leu '1' na pos {pos} no extremo direito: gravou 'D' (lembrando que é 1 na 2ª metade). Pareamento concluído! Volta à esquerda.",

        ("q_seek_left", "0"): "Leu '0' na pos {pos}: voltando à esquerda sobre símbolos não marcados...",
        ("q_seek_left", "1"): "Leu '1' na pos {pos}: voltando à esquerda sobre símbolos não marcados...",
        ("q_seek_left", "A"): "Leu 'A' na pos {pos}: encontrou o último símbolo marcado na esquerda! Dá 1 passo à direita para marcar o próximo.",
        ("q_seek_left", "B"): "Leu 'B' na pos {pos}: encontrou o último símbolo marcado na esquerda! Dá 1 passo à direita para marcar o próximo.",

        ("q_mark_left", "0"): "Leu '0' na pos {pos}: gravou 'A'. Avança novamente à direita para encontrar o próximo símbolo correspondente do final.",
        ("q_mark_left", "1"): "Leu '1' na pos {pos}: gravou 'B'. Avança novamente à direita para encontrar o próximo símbolo correspondente do final.",
        ("q_mark_left", "C"): "Leu 'C' na pos {pos}: PONTO MÉDIO LOCALIZADO! Os marcadores da esquerda e da direita se encontraram. Comprimento é par! Iniciando Fase 2 de casamento.",
        ("q_mark_left", "D"): "Leu 'D' na pos {pos}: PONTO MÉDIO LOCALIZADO! Os marcadores da esquerda e da direita se encontraram. Comprimento é par! Iniciando Fase 2 de casamento.",

        ("q_stage2_rewind_start", "A"): "Leu 'A' na pos {pos}: rebobinando até o início da fita...",
        ("q_stage2_rewind_start", "B"): "Leu 'B' na pos {pos}: rebobinando até o início da fita...",
        ("q_stage2_rewind_start", "_"): "Leu '⊔' na pos {pos}: cabeçote no início! Dá 1 passo à direita e começa a validar se o primeiro bloco (w1) é idêntico ao segundo (w2).",

        ("q_match_loop", "A"): "Leu 'A' na pos {pos} (originalmente era '0'): gravou '*' (consumido). Agora varre à direita para achar o primeiro da 2ª metade, que DEVE ser 'C' (0).",
        ("q_match_loop", "B"): "Leu 'B' na pos {pos} (originalmente era '1'): gravou '*' (consumido). Agora varre à direita para achar o primeiro da 2ª metade, que DEVE ser 'D' (1).",
        ("q_match_loop", "*"): "Pulando símbolo '*' já verificado da primeira metade...",
        ("q_match_loop", "#"): "Leu '#' na pos {pos}: todos os símbolos da 1ª metade foram consumidos com sucesso! Mudo para q_verify para conferir o restante da 2ª metade.",

        ("q_match_find_C", "A"): "Pulando 'A' da 1ª metade em busca do símbolo da 2ª metade...",
        ("q_match_find_C", "B"): "Pulando 'B' da 1ª metade em busca do símbolo da 2ª metade...",
        ("q_match_find_C", "#"): "Pulando '#' (já verificado na 2ª metade) em busca do próximo livre...",
        ("q_match_find_C", "C"): "CASAMENTO CONFIRMADO! O símbolo da 2ª metade é 'C' ('0'), idêntico ao 'A' ('0') de w1! Gravou '#' (consumido). Rebobinando para pegar o próximo.",

        ("q_match_find_D", "A"): "Pulando 'A' da 1ª metade em busca do símbolo da 2ª metade...",
        ("q_match_find_D", "B"): "Pulando 'B' da 1ª metade em busca do símbolo da 2ª metade...",
        ("q_match_find_D", "#"): "Pulando '#' (já verificado na 2ª metade) em busca do próximo livre...",
        ("q_match_find_D", "D"): "CASAMENTO CONFIRMADO! O símbolo da 2ª metade é 'D' ('1'), idêntico ao 'B' ('1') de w1! Gravou '#' (consumido). Rebobinando para pegar o próximo.",

        ("q_match_rewind", "#"): "Rebobinando à esquerda sobre símbolos...",
        ("q_match_rewind", "C"): "Rebobinando à esquerda sobre símbolos...",
        ("q_match_rewind", "D"): "Rebobinando à esquerda sobre símbolos...",
        ("q_match_rewind", "A"): "Rebobinando à esquerda sobre símbolos...",
        ("q_match_rewind", "B"): "Rebobinando à esquerda sobre símbolos...",
        ("q_match_rewind", "*"): "Leu '*' na pos {pos}: retornou ao último símbolo consumido de w1. Dá 1 passo à direita para o próximo caractere a ser comparado.",

        ("q_verify_all_matched", "#"): "Conferindo que todos os símbolos da 2ª metade foram devidamente validados...",
        ("q_verify_all_matched", "_"): "Leu '⊔' (branco): final da fita alcançado! Toda a primeira metade coincidiu estritamente com a segunda metade (w1 == w2). PALAVRA ACEITA!",
    }

    intents = {
        "q0": "Fase 1: Início da detecção do ponto médio e paridade.",
        "q_seek_right": "Fase 1: Varrendo à direita até o extremo não marcado da cadeia.",
        "q_mark_right": "Fase 1: Marcando o símbolo da extremidade direita para parear com a esquerda.",
        "q_seek_left": "Fase 1: Rebobinando à esquerda em busca do próximo símbolo a marcar.",
        "q_mark_left": "Fase 1: Verificando se as duas frentes se encontraram no meio.",
        "q_stage2_rewind_start": "Fase 2: Rebobinando até a posição inicial da fita.",
        "q_match_loop": "Fase 2: Lendo o próximo símbolo de w1 para comparar com w2.",
        "q_match_find_C": "Fase 2: Procurando o '0' correspondente (marcador 'C') na segunda metade.",
        "q_match_find_D": "Fase 2: Procurando o '1' correspondente (marcador 'D') na segunda metade.",
        "q_match_rewind": "Fase 2: Rebobinando até a fronteira de símbolos já comparados de w1.",
        "q_verify_all_matched": "Fase 2: Verificando se toda a segunda metade foi consumida.",
        "q_accept": "Conclusão: Palavra aceita! w1 é estritamente idêntica a w2.",
        "q_reject": "Conclusão: Palavra rejeitada! Comprimento ímpar ou w1 != w2.",
    }

    rejection_reasons = {
        ("q_mark_right", "A"): "Sobrou um símbolo solitário no centro sem par na direita. A palavra tem comprimento ÍMPAR. Palavras ímpares nunca podem ser do formato ww. REJEITADA!",
        ("q_mark_right", "B"): "Sobrou um símbolo solitário no centro sem par na direita. A palavra tem comprimento ÍMPAR. Palavras ímpares nunca podem ser do formato ww. REJEITADA!",
        ("q_match_find_C", "D"): "DIVERGÊNCIA! A primeira metade tem '0', mas a segunda metade tem '1' ('D'). w1 != w2. REJEITADA!",
        ("q_match_find_D", "C"): "DIVERGÊNCIA! A primeira metade tem '1', mas a segunda metade tem '0' ('C'). w1 != w2. REJEITADA!",
        ("q_match_find_C", "_"): "Fim inesperado da fita durante o casamento de símbolos. REJEITADA!",
        ("q_match_find_D", "_"): "Fim inesperado da fita durante o casamento de símbolos. REJEITADA!",
    }

    theory_guide = {
        "title": "Linguagem L = {ww | w ∈ {0, 1}*}",
        "concept": "A linguagem de duplicação de palavras binárias consiste em cadeias formadas pela repetição idêntica de uma palavra w (como '0101' para w='01', ou '110110' para w='110'). Ela não é livre de contexto porque requer lembrar uma cadeia inteira e compará-la na mesma ordem (uma pilha LIFO inverte a ordem, só reconhecendo palíndromos w w^R).",
        "how_it_works": [
            "1. Fase de Ponto Médio: A máquina marca alternadamente o símbolo mais à esquerda e o mais à direita. Se sobrar 1 símbolo ímpar no meio, rejeita. Quando as duas frentes se encontram, achamos o meio exato!",
            "2. Preservação dos Bits: Os marcadores da 1ª metade (A=0, B=1) e da 2ª metade (C=0, D=1) guardam os valores originais.",
            "3. Fase de Casamento: A máquina lê o 1º de w1 (A ou B) e procura o 1º de w2 (C ou D). Se baterem, marca com '#' e volta para o próximo.",
            "4. Decisão: Se todos os símbolos baterem perfeitamente até o fim, a palavra é aceita! Se houver qualquer bit diferente, rejeita imediatamente."
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
        name="L = {ww | w ∈ {0, 1}*}",
        description="Reconhecedor da linguagem não livre de contexto de duplicação binária ww.",
        explanations=explanations,
        intents=intents,
        rejection_reasons=rejection_reasons,
        theory_guide=theory_guide
    )
