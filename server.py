"""
Servidor HTTP Leve e API REST para a Interface Gráfica da Máquina de Turing.
Utiliza apenas a biblioteca padrão do Python (sem dependências externas).
"""

import json
import os
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from turing_machine.languages.an_bn_cn import create_an_bn_cn_machine
from turing_machine.languages.ww import create_ww_machine


WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


def get_machine(lang_id: str):
    if lang_id == "anbncn":
        return create_an_bn_cn_machine()
    elif lang_id == "ww":
        return create_ww_machine()
    raise ValueError(f"Linguagem desconhecida: {lang_id}")


class TuringMachineHandler(SimpleHTTPRequestHandler):
    """Manipulador de requisições HTTP e API REST."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/info":
            self.send_json(self.handle_api_info())
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/simulate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body) if body else {}
                response_data = self.handle_api_simulate(data)
                self.send_json(response_data)
            except Exception as e:
                self.send_json({"error": str(e)}, status=400)
        else:
            self.send_error(404, "Endpoint não encontrado")

    def handle_api_info(self) -> dict:
        m1 = create_an_bn_cn_machine()
        m2 = create_ww_machine()
        return {
            "languages": [
                {
                    "id": "anbncn",
                    "name": m1.name,
                    "description": m1.description,
                    "input_alphabet": sorted(list(m1.input_alphabet)),
                    "tape_alphabet": sorted(list(m1.tape_alphabet)),
                    "blank_symbol": m1.blank_symbol,
                    "initial_state": m1.initial_state,
                    "accept_states": sorted(list(m1.accept_states)),
                    "reject_states": sorted(list(m1.reject_states)),
                    "transitions": m1.get_transitions_table(),
                    "theory_guide": m1.theory_guide,
                    "presets": [
                        {"word": "abc", "label": "abc (n=1, Válida)", "expected": True},
                        {"word": "aabbcc", "label": "aabbcc (n=2, Válida)", "expected": True},
                        {"word": "aaabbbccc", "label": "aaabbbccc (n=3, Válida)", "expected": True},
                        {"word": "aabbc", "label": "aabbc (menos c, Inválida)", "expected": False},
                        {"word": "aabcc", "label": "aabcc (menos b, Inválida)", "expected": False},
                        {"word": "abbc", "label": "abbc (menos a, Inválida)", "expected": False},
                        {"word": "cba", "label": "cba (ordem invertida, Inválida)", "expected": False},
                    ]
                },
                {
                    "id": "ww",
                    "name": m2.name,
                    "description": m2.description,
                    "input_alphabet": sorted(list(m2.input_alphabet)),
                    "tape_alphabet": sorted(list(m2.tape_alphabet)),
                    "blank_symbol": m2.blank_symbol,
                    "initial_state": m2.initial_state,
                    "accept_states": sorted(list(m2.accept_states)),
                    "reject_states": sorted(list(m2.reject_states)),
                    "transitions": m2.get_transitions_table(),
                    "theory_guide": m2.theory_guide,
                    "presets": [
                        {"word": "", "label": "ε (palavra vazia, Válida)", "expected": True},
                        {"word": "00", "label": "00 (w=0, Válida)", "expected": True},
                        {"word": "11", "label": "11 (w=1, Válida)", "expected": True},
                        {"word": "0101", "label": "0101 (w=01, Válida)", "expected": True},
                        {"word": "110110", "label": "110110 (w=110, Válida)", "expected": True},
                        {"word": "0110", "label": "0110 (w1 != w2, Inválida)", "expected": False},
                        {"word": "010", "label": "010 (ímpar, Inválida)", "expected": False},
                        {"word": "1001", "label": "1001 (espelho, Inválida)", "expected": False},
                    ]
                }
            ]
        }

    def handle_api_simulate(self, data: dict) -> dict:
        lang_id = data.get("lang", "anbncn")
        word = data.get("word", "")
        max_steps = int(data.get("max_steps", 10000))

        tm = get_machine(lang_id)
        tm.load(word)
        tm.run(max_steps=max_steps)

        snapshots = [s.to_dict() for s in tm.trace]

        return {
            "lang": lang_id,
            "word": word,
            "machine_name": tm.name,
            "accepted": tm.accepted,
            "rejected": tm.rejected,
            "halted": tm.halted,
            "total_steps": tm.step_count,
            "final_state": tm.current_state,
            "trace": snapshots
        }

    def send_json(self, data: dict, status: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Silencia logs redundantes de requisição no terminal para manter a tela limpa
        pass


def start_server(port: int = 8080, host: str = "0.0.0.0"):
    """Inicia o servidor Web na porta indicada, com busca automática de porta livre se ocupada."""
    ThreadingHTTPServer.allow_reuse_address = True
    
    current_port = port
    max_attempts = 25
    httpd = None

    for attempt in range(max_attempts):
        try:
            server_address = (host, current_port)
            httpd = ThreadingHTTPServer(server_address, TuringMachineHandler)
            break
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"\033[93mAviso: Porta {current_port} já está em uso. Tentando próxima porta...\033[0m")
                current_port += 1
            else:
                raise e

    if not httpd:
        raise RuntimeError(f"Não foi possível encontrar uma porta livre após {max_attempts} tentativas.")

    url_local = f"http://localhost:{current_port}"
    url_ip = f"http://127.0.0.1:{current_port}"
    print("\n" + "=" * 65)
    print(f" Servidor da Interface Gráfica iniciado com sucesso!")
    print(f" Abra no seu navegador qualquer um dos links abaixo:")
    print(f" 👉 \033[96m\033[1m{url_local}\033[0m")
    print(f" 👉 \033[96m\033[1m{url_ip}\033[0m")
    print(f" Pressione Ctrl+C para encerrar o servidor.")
    print("=" * 65 + "\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado pelo usuário.")
        httpd.server_close()


if __name__ == "__main__":
    start_server()
