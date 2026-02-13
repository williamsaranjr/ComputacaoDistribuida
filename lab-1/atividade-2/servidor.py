import socket
from threading import Thread, Lock

HOST = '0.0.0.0'
PORT = 1337

MAIOR_LANCE = 0.0
CLIENTES_CONECTADOS = []
LOCK = Lock()


class ServerHandler:
    def __init__(self):
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Socket inicializado com sucesso")

    def inicializar(self):
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)

        print("Servidor aguardando conexões...")

        try:
            while self.running:
                conn, addr = self.socket.accept()

                with LOCK:
                    CLIENTES_CONECTADOS.append(conn)

                thread = Thread(
                    target=self.lidar_com_conexao,
                    args=(conn, addr),
                    daemon=True
                )
                thread.start()

                print(f"Cliente conectado: {addr}")

        except KeyboardInterrupt:
            print("\nEncerrando servidor...")

        finally:
            self.socket.close()
            print("Socket fechado.")

    @staticmethod
    def broadcast(mensagem: str):
        with LOCK:
            for cliente in CLIENTES_CONECTADOS:
                try:
                    cliente.sendall(mensagem.encode("utf-8"))
                except:
                    pass

    @staticmethod
    def lidar_com_conexao(conexao: socket.socket, addr):
        global MAIOR_LANCE

        print(f"Conexão aceita de {addr}")

        try:
            while True:
                dados = conexao.recv(1024)
                if not dados:
                    break

                try:
                    lance = float(dados.decode("utf-8").strip())
                except ValueError:
                    conexao.sendall("Formato inválido\n".encode("utf-8"))
                    continue

                mensagem = None

                with LOCK:
                    if lance > MAIOR_LANCE:
                        MAIOR_LANCE = lance
                        mensagem = f"NOVO LANCE: {lance:.2f} por {addr}\n"
                        print(mensagem.strip())

                if mensagem:
                    ServerHandler.broadcast(mensagem)
                else:
                    conexao.sendall(
                        "LANCE RECUSADO: Valor baixo\n".encode("utf-8")
                    )

        finally:
            with LOCK:
                if conexao in CLIENTES_CONECTADOS:
                    CLIENTES_CONECTADOS.remove(conexao)

            conexao.close()
            print(f"Cliente desconectado: {addr}")


if __name__ == "__main__":
    server = ServerHandler()
    server.inicializar()
