import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1337

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[INFO] Socket inicializado com sucesso")

        request = input("Insira o comando: ")

        try:
            s.connect((HOST, PORT))
            print(f"[INFO] Conexão com '' estabelecida com sucesso")

            s.sendall(request.encode("utf-8"))
            print(f"[INFO] Comando enviado com sucesso. Aguardando resposta do servidor")

            data = s.recv(1024).decode("utf-8")
            print(f"[INFO] Resposta recebida: {data}")
    
        except Exception:
            print(f"[ERROR] Houve um erro ao executar o programa")

    s.close()
    print(f"[INFO] Socket finalizado com sucesso")