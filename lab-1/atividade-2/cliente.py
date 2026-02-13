import socket
from threading import Thread

HOST = "127.0.0.1"  # ou IP do servidor
PORT = 1337


def escutar_servidor(sock: socket.socket):
    try:
        while True:
            dados = sock.recv(1024)
            if not dados:
                print("Conexão encerrada pelo servidor.")
                break

            print("\n" + dados.decode("utf-8").strip())
    except:
        pass


def iniciar_cliente():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        print("Conectado ao servidor.")
    except:
        print("Não foi possível conectar.")
        return

    # Thread para escutar mensagens do servidor
    thread = Thread(target=escutar_servidor, args=(sock,), daemon=True)
    thread.start()

    try:
        while True:
            lance = input("Digite seu lance: ")

            if lance.lower() == "sair":
                break

            sock.sendall(lance.encode("utf-8"))

    except KeyboardInterrupt:
        print("\nEncerrando cliente...")

    finally:
        sock.close()


if __name__ == "__main__":
    iniciar_cliente()
