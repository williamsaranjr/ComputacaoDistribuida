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
        return fundos_imobiliarios[fii]["preco"]


class ObterProventos(Comando):
    def executar(self, fii: str):
        return fundos_imobiliarios[fii]["proventos"]


class ObterStatus(Comando):
    def executar(self, fii: str):
        preco = fundos_imobiliarios[fii]["preco"]
        proventos = fundos_imobiliarios[fii]["proventos"]

        return f"{fii.upper()} - Preço: R$ {preco:.02f} - Proventos: R$ {proventos:.02f}"


comandoExecutorMap = {
    "PRECO": ObterPreco(),
    "PROVENTO": ObterProventos(),
    "STATUS": ObterStatus()
}


if __name__ == "__main__":
    # Configurar o socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.b
        # Receber a requisição

        # Validar o comando
        if comando not in comandoExecutorMap.keys():
            

        # Executar o comando

        # Retornar o valor