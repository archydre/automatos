"""
Ponto de Entrada Principal (CLI) para a Máquina de Turing de Decisão.
Oferece menu interativo no terminal, execução passo a passo, animação e inicialização do servidor Web.
"""

import sys
import time
import argparse
import unittest
from turing_machine.languages.an_bn_cn import create_an_bn_cn_machine
from turing_machine.languages.ww import create_ww_machine
from turing_machine.visualizer import Visualizer


def run_interactive_simulation(tm, word: str, mode: str = "interactive", delay: float = 0.25):
    """Executa a simulação com a visualização selecionada."""
    try:
        tm.load(word)
    except ValueError as e:
        print(f"\n{Visualizer.RED}Erro na entrada:{Visualizer.RESET} {e}\n")
        return

    print("\n" + "=" * 65)
    print(f"{Visualizer.BOLD}Iniciando Máquina de Turing: {tm.name}{Visualizer.RESET}")
    print(f"Palavra de entrada: '{word}' | Branco: '{tm.blank_symbol}'")
    print("=" * 65)

    # Exibe snapshot inicial
    initial_snap = tm.trace[0]
    print(Visualizer.render_step(initial_snap, show_tape=True))

    if mode == "interactive":
        input(f"\n{Visualizer.CYAN}Pressione [Enter] para executar o primeiro passo...{Visualizer.RESET}")

    while not tm.halted:
        snap = tm.step()
        print(Visualizer.render_step(snap, show_tape=True))

        if mode == "interactive" and not tm.halted:
            cmd = input(f"\n{Visualizer.CYAN}[Enter]: próximo passo | [c]: continuar direto | [q]: abortar > {Visualizer.RESET}").strip().lower()
            if cmd == "q":
                print("\nExecução abortada pelo usuário.")
                break
            elif cmd == "c":
                mode = "fast"
        elif mode == "animated" and not tm.halted:
            time.sleep(delay)

    Visualizer.print_summary(tm, word)


def run_tests():
    """Executa os testes automatizados da suíte unittest."""
    print("\n" + "=" * 65)
    print(f"{Visualizer.BOLD}Executando Bateria de Testes Automatizados...{Visualizer.RESET}")
    print("=" * 65 + "\n")
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def menu_choose_word(lang_id: int):
    """Menu para seleção de palavra de exemplo ou personalizada."""
    if lang_id == 1:
        presets = [
            ("abc", "Válida (n=1)"),
            ("aabbcc", "Válida (n=2)"),
            ("aaabbbccc", "Válida (n=3)"),
            ("aabbc", "Inválida (menos 'c's)"),
            ("aabcc", "Inválida (menos 'b's)"),
            ("abbc", "Inválida (menos 'a's)"),
            ("cba", "Inválida (ordem invertida)"),
        ]
    else:
        presets = [
            ("00", "Válida (w=0)"),
            ("11", "Válida (w=1)"),
            ("0101", "Válida (w=01)"),
            ("110110", "Válida (w=110)"),
            ("0110", "Inválida (w1 != w2)"),
            ("010", "Inválida (comprimento ímpar)"),
            ("1001", "Inválida (palíndromo, não duplicação)"),
        ]

    print("\nEscolha uma palavra de teste:")
    for idx, (ex_word, desc) in enumerate(presets, 1):
        print(f"  [{idx}] '{ex_word}' ({desc})")
    print(f"  [{len(presets) + 1}] Digitar palavra personalizada")

    choice = input(f"\nSelecione uma opção (1-{len(presets) + 1}): ").strip()
    if choice.isdigit():
        c_int = int(choice)
        if 1 <= c_int <= len(presets):
            return presets[c_int - 1][0]
        elif c_int == len(presets) + 1:
            return input("Digite a palavra desejada: ").strip()

    print("Opção inválida, usando o primeiro exemplo.")
    return presets[0][0]


def menu_choose_mode():
    """Menu para escolha do modo de visualização."""
    print("\nEscolha o modo de execução:")
    print("  [1] Passo a passo interativo (Pressione Enter a cada passo)")
    print("  [2] Animação no terminal (delay entre transições)")
    print("  [3] Execução direta com exibição de todos os passos")
    print("  [4] Execução instantânea (apenas resumo final)")
    
    choice = input("\nModo (1-4, padrão=1): ").strip()
    if choice == "2":
        return "animated"
    elif choice == "3":
        return "fast"
    elif choice == "4":
        return "silent"
    return "interactive"


def interactive_cli():
    """Menu principal no terminal."""
    while True:
        print("\n" + "=" * 65)
        print(f"{Visualizer.BOLD}TEMA 5: MÁQUINA DE TURING DE DECISÃO (SIMULADOR){Visualizer.RESET}")
        print("=" * 65)
        print("Linguagens Não Livres de Contexto Disponíveis:")
        print("  [1] L = {aⁿ bⁿ cⁿ | n ≥ 1}  (Alfabeto: {a, b, c})")
        print("  [2] L = {ww | w ∈ {0,1}*}   (Alfabeto: {0, 1})")
        print("\nFerramentas:")
        print("  [3] Iniciar Interface Gráfica Web (Visual no Navegador)")
        print("  [4] Executar Testes Automatizados (unittest)")
        print("  [0] Sair")
        print("=" * 65)

        op = input("\nEscolha uma opção: ").strip()
        if op == "0":
            print("\nEncerrando o simulador. Até logo!")
            break
        elif op == "1":
            tm = create_an_bn_cn_machine()
            word = menu_choose_word(1)
            mode = menu_choose_mode()
            if mode == "silent":
                tm.load(word)
                tm.run()
                Visualizer.print_summary(tm, word)
            else:
                run_interactive_simulation(tm, word, mode=mode)
        elif op == "2":
            tm = create_ww_machine()
            word = menu_choose_word(2)
            mode = menu_choose_mode()
            if mode == "silent":
                tm.load(word)
                tm.run()
                Visualizer.print_summary(tm, word)
            else:
                run_interactive_simulation(tm, word, mode=mode)
        elif op == "3":
            from server import start_server
            print("\nIniciando servidor da Interface Gráfica Web...")
            start_server(port=8080)
        elif op == "4":
            run_tests()
        else:
            print(f"{Visualizer.RED}Opção inválida! Tente novamente.{Visualizer.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Simulador de Máquina de Turing de Decisão")
    parser.add_argument("--lang", choices=["anbncn", "ww"], help="Linguagem a ser executada")
    parser.add_argument("--word", type=str, help="Palavra de entrada")
    parser.add_argument("--mode", choices=["interactive", "animated", "fast", "silent"], default="interactive")
    parser.add_argument("--web", action="store_true", help="Iniciar diretamente a Interface Gráfica Web")
    parser.add_argument("--test", action="store_true", help="Executar testes unitários")
    parser.add_argument("--port", type=int, default=8080, help="Porta para o servidor Web (padrão 8080)")

    args = parser.parse_args()

    if args.test:
        run_tests()
        return

    if args.web:
        from server import start_server
        start_server(port=args.port)
        return

    if args.lang and args.word is not None:
        if args.lang == "anbncn":
            tm = create_an_bn_cn_machine()
        else:
            tm = create_ww_machine()
        run_interactive_simulation(tm, args.word, mode=args.mode)
        return

    interactive_cli()


if __name__ == "__main__":
    main()
