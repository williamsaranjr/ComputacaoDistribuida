from abc import ABC
import socket

fundos_imobiliarios = {
    "HGLG11": {"preco": 165.30, "provento": 1.10},
    "MXRF11": {"preco": 10.45, "provento": 0.10},
    "KNRI11": {"preco": 140.20, "provento": 0.95},
    "VISC11": {"preco": 108.90, "provento": 0.85},
    "XPML11": {"preco": 112.50, "provento": 0.90},
    "BCFF11": {"preco": 62.30, "provento": 0.55},
    "HSML11": {"preco": 86.40, "provento": 0.70},
    "CPTS11": {"preco": 98.10, "provento": 1.05},
    "RBRF11": {"preco": 76.80, "provento": 0.65},
    "GGRC11": {"preco": 103.60, "provento": 0.78}
}


class Comando(ABC):
    def executar(self, fii: str):
        pass


class ObterPreco(Comando):
    def executar(self, fii: str):
        return f"R$ {fundos_imobiliarios[fii].get("preco"):.02f}"


class ObterProventos(Comando):
    def executar(self, fii: str):
        return f"R$ {fundos_imobiliarios[fii].get("provento"):.02f}"


class ObterStatus(Comando):
    def executar(self, fii: str):
        preco = fundos_imobiliarios[fii].get("preco")
        proventos = fundos_imobiliarios[fii].get("provento")

        return f"{fii.upper()} - Preço: R$ {preco:.02f} - Proventos: R$ {proventos:.02f}"


comandoExecutorMap = {
    "PRECO": ObterPreco(),
    "PROVENTO": ObterProventos(),
    "STATUS": ObterStatus()
}

HOST = "0.0.0.0"
PORT = 1337

if __name__ == "__main__":
    print(f"[INFO] Informações do host:\n\tHost: {HOST}\n\tPorta: {PORT}")

    # Configurar o socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            print(f"[INFO] Socket inicializado com sucesso")

            s.listen(1)
            print(f"[INFO] Socket aguardando conexões")

            print(f"[INFO] Pressione CTRL + C para finalizar o processo")

            while True:
                # Receber a requisição
                conn, addr = s.accept()
                print(f"[INFO] Conexão com '{addr}' aceita")

                data = conn.recv(1024).decode("utf-8")
                print(f"[INFO] Dados recebidos: '{data}'")

                # Validar o comando
                try:
                    comando, ticker = data.split(";")

                    # Comandos inválidos
                    if comando not in comandoExecutorMap.keys():
                        print(f"[ERROR] Comando informado não é válido")
                        conn.sendall("ERRO: Comando inválido".encode("utf-8"))
                        continue

                    executor: Comando = comandoExecutorMap.get(comando)

                except Exception:
                    print(f"[ERROR] Ocorreu um erro ao validar a mensagem")
                    conn.sendall("ERRO: Mensagem inválida".encode("utf-8"))
                    continue

                # Executar o comando
                try:
                    response = executor.executar(ticker)
                    print(f"[INFO] Retornando '{response}' ao cliente")

                    # Retornar o valor
                    conn.sendall(response.encode("utf-8"))
                    print(f"[INFO] Resposta enviada com sucesso")

                except KeyError:
                    print(f"[ERROR] Cliente informou um ticker inválido")
                    conn.sendall("ERRO: Ticker inválido".encode("utf-8"))
                    continue

                except Exception:
                    print(f"[ERROR] Houve um erro ao executar o comando")
                    conn.sendall("ERRO_AO_EXECUTAR_COMANDO".encode("utf-8"))
                    continue

            # Finalizar a conexão
            conn.close()
            print(f"[INFO] Conexão finalizada com sucesso")

        except KeyboardInterrupt:
                print(f"[INFO] Encerrando programa graciosamente")

        finally:
                s.close()
                print(f"[INFO] Socket finalizado com sucesso")