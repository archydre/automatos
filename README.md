# Tema 5: Máquina de Turing de Decisão (Reconhecedora de Linguagens)

Este projeto implementa uma **Máquina de Turing (MT) Determinística de Decisão** em Python, atendendo a todos os requisitos do **Tema 5**:

1. **Fita infinita bidirecional** com suporte a movimentações **L** (*Left*), **R** (*Right*) e **S** (*Stay* / Parado), com símbolo de branco configurável ($\sqcup$ ou `_`).
2. **Tabelas de transição formais** para reconhecimento de linguagens não livres de contexto clássicas:
   - $L_1 = \{a^n b^n c^n \mid n \ge 1\}$
   - $L_2 = \{ww \mid w \in \{0, 1\}^*\}$
3. **Exibição do passo a passo da fita** com duas interfaces completas:
   - **Interface Gráfica Web interativa** no navegador com animação da fita, controles de reprodução (*play/pause*, passo a passo, slider de velocidade) e rastreamento da regra ativa na tabela de transições.
   - **Interface CLI no Terminal** com modos interativo, animado e direto com visualização detalhada em cores ANSI.
4. **Bateria de testes automatizados** cobrindo todos os componentes e casos de borda.
5. **Manual Didático Completo em PDF**: Documento técnico e pedagógico sem lacunas conceituais, com analogias intuitivas, tabelas completas de transição e traçados passo a passo ([Manual_Didatico_Maquina_de_Turing.pdf](Manual_Didatico_Maquina_de_Turing.pdf)).

---

## 🏛️ Fundamentação Teórica

Formalmente, a Máquina de Turing é definida pela 7-tupla:
$$M = (Q, \Sigma, \Gamma, \delta, q_0, B, F)$$

Onde:
- $Q$: Conjunto finito de estados.
- $\Sigma$: Alfabeto de entrada ($B \notin \Sigma$).
- $\Gamma$: Alfabeto da fita ($\Sigma \subset \Gamma$ e $B \in \Gamma$).
- $\delta$: Função de transição $\delta: Q \times \Gamma \to Q \times \Gamma \times \{L, R, S\}$.
- $q_0 \in Q$: Estado inicial.
- $B \in \Gamma$: Símbolo de branco (representado por `_` internamente e `⊔` visualmente).
- $F$: Conjunto de estados de aceitação ($F_{accept}$), com estado explícito de rejeição ($F_{reject}$) e parada por travamento caso não haja transição definida.

Como se trata de uma **Máquina de Decisão (Decider)**, o autômato **sempre para** para qualquer cadeia de entrada $w \in \Sigma^*$, decidindo formalmente se $w \in L$ ou $w \notin L$.

---

## 📁 Estrutura do Repositório

```text
automatos/
├── Manual_Didatico_Maquina_de_Turing.pdf # Manual didático completo em PDF
├── generate_pdf.py                       # Script gerador do manual em PDF
├── docs/
│   ├── manual_didatico_maquina_turing.html # Código fonte estruturado do manual
│   └── Manual_Didatico_Maquina_de_Turing.pdf
├── turing_machine/
│   ├── __init__.py
│   ├── tape.py              # Fita infinita bidirecional indexada em Z (L, R, S)
│   ├── machine.py           # Controlador formal da MT e histórico de execução
│   ├── visualizer.py        # Formatador e renderizador do passo a passo no terminal
│   └── languages/
│       ├── __init__.py
│       ├── an_bn_cn.py      # MT para L = {aⁿ bⁿ cⁿ | n ≥ 1}
│       └── ww.py            # MT para L = {ww | w ∈ {0, 1}*}
├── web/
│   ├── index.html           # Interface Gráfica Web moderna
│   ├── style.css            # Estilização visual (células da fita, cabeçote animado)
│   ├── app.js               # Lógica visual e controles da fita
│   └── diagram.js           # Renderizador interativo de grafos vetoriais SVG
├── tests/
│   ├── __init__.py
│   ├── test_tape.py         # Testes da fita infinita e movimentações L/R/S
│   ├── test_an_bn_cn.py     # Testes da linguagem aⁿbⁿcⁿ
│   └── test_ww.py           # Testes da linguagem ww
├── server.py                # Servidor HTTP leve integrado com API REST
├── main.py                  # Ponto de entrada CLI interativo e executável
└── README.md                # Este documento
```

---

## 🚀 Como Executar

### 1. Interface Gráfica Web Interativa (Recomendada)
Inicie o servidor Web leve (utiliza apenas a biblioteca padrão do Python):
```bash
python3 main.py --web
# ou
python3 server.py
```
Abra seu navegador em: **`http://localhost:8080`** (ou `http://127.0.0.1:8080`)

**Recursos da Interface Web:**
- **Fita Infinita Dinâmica**: As células se movem suavemente para a esquerda ou direita à medida que o cabeçote avança, mantendo a célula atual sempre centralizada sob o indicador do cabeçote.
- **Controles de Reprodução**: Botões de `Início (⏮)`, `Anterior (◀)`, `Reproduzir/Pausar (▶/⏸)`, `Próximo (▶)` e `Fim (⏭)`.
- **Slider de Velocidade**: Ajuste em tempo real entre 50ms e 1200ms por transição.
- **Destaque na Tabela de Transições**: A linha exata da transição formal $\delta(q, \sigma)$ executada no momento fica iluminada em tempo real.
- **Histórico Completo (Trace)**: Lista de todos os passos com navegação por clique direto.
- **Exemplos Rápidos**: Botões pré-configurados com palavras válidas e inválidas clássicas.

---

### 2. Interface de Linha de Comando (CLI no Terminal)
Para usar o menu interativo no terminal:
```bash
python3 main.py
```

Você pode também executar simulações diretas via linha de comando:

```bash
# Executa aⁿbⁿcⁿ no modo rápido exibindo todos os passos:
python3 main.py --lang anbncn --word aabbcc --mode fast

# Executa ww no modo animado no terminal:
python3 main.py --lang ww --word 0101 --mode animated

# Executa modo passo a passo interativo (pressionando Enter a cada transição):
python3 main.py --lang anbncn --word abc --mode interactive
```

---

### 3. Bateria de Testes Automatizados
Para executar todos os testes unitários via `unittest`:
```bash
python3 -m unittest discover tests
# ou
python3 main.py --test
```

---

## 🧠 Detalhamento das Linguagens Implementadas

### 1. Linguagem $L_1 = \{a^n b^n c^n \mid n \ge 1\}$
- **Alfabetos**: $\Sigma = \{a, b, c\}$, $\Gamma = \{a, b, c, X, Y, Z, \_\}$.
- **Algoritmo**:
  1. $q_0$: Marca o primeiro `a` não marcado com `X`, move para a direita e entra em $q_1$. Se ler `Y`, todos os `a`s foram consumidos; vai para verificação final em $q_5$.
  2. $q_1$: Varre à direita pulando `a`s e `Y`s até achar o primeiro `b` não marcado; marca com `Y` e avança para $q_2$.
  3. $q_2$: Varre à direita pulando `b`s e `Z`s até achar o primeiro `c` não marcado; marca com `Z` e inicia o recuo para $q_3$.
  4. $q_3$: Rebobina à esquerda pulando todos os símbolos até atingir o marcador `X` mais recente; move $R$ e volta a $q_0$.
  5. $q_5$ e $q_6$: Verificação de encerramento; garante que não restaram `b`s ou `c`s soltos. Ao ler o branco `_`, para em $q_{accept}$ com movimento `S` (*Stay*).

---

### 2. Linguagem $L_2 = \{ww \mid w \in \{0, 1\}^*\}$
- **Alfabetos**: $\Sigma = \{0, 1\}$, $\Gamma = \{0, 1, A, B, C, D, *, \#, \_\}$.
- **Algoritmo em 2 Estágios**:
  1. **Estágio 1 (Detecção de Ponto Médio e Paridade)**:
     - Marca alternadamente o símbolo mais à esquerda (`0 → A`, `1 → B`) e o mais à direita (`0 → C`, `1 → D`).
     - Se sobrar um símbolo ímpar no meio, para e rejeita imediatamente.
     - Quando os marcadores da esquerda e da direita se encontram, o ponto médio exato da palavra foi delimitado.
  2. **Estágio 2 (Comparação Símbolo a Símbolo)**:
     - Rebobina a fita até a primeira posição.
     - Para cada símbolo marcado na primeira metade (`A` para 0, `B` para 1), marca como consumido (`*`) e varre à direita para encontrar o próximo símbolo da segunda metade (`C` para 0, `D` para 1).
     - Se forem correspondentes (`A` com `C`, ou `B` com `D`), marca com `#` e repete. Se houver divergência, para e rejeita.
     - Ao final, garante que todos os símbolos foram conferidos e termina em $q_{accept}$ com movimento `S`.
