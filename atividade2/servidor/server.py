import socket

# lista de questões
QUESTOES = [
    {
        "enunciado": "Qual é a capital do Brasil?",
        "alternativas": "a) São Paulo \nb) Brasília \nc) Rio de Janeiro \nd) Belo Horizonte",
        "resposta_correta": "b"
    },
    # {
    #     "enunciado": "Qual é a capital do Brasil?",
    #     "alternativas": ["a) São Paulo", "b) Brasília", "c) Rio de Janeiro", "d) Belo Horizonte"],
    #     "resposta_correta": "b"
    # },
    {
        "enunciado": "Qual é o maior planeta do sistema solar?",
        "alternativas": "a) Terra \nb) Júpiter \nc) Saturno \nd) Marte",
        "resposta_correta": "b"
    },
   
    {
        "enunciado": "Qual a melhor linguagem de programação?",
        "alternativas": "a) Java \nb) Python \nc) Assembly \nd) Aquela que resolve melhor o probema",
        "resposta_correta": "d"
    },
    {
        "enunciado": "Qual tipo de critografia possui eficácia de segurança devido ao probelma do logaritmo discreto?",
        "alternativas": "a) ECC \nb) RSA \nc) AES \nd) PGP",
        "resposta_correta": "a"
    },
    {
        "enunciado": "Quanto é 2 + 2?",
        "alternativas": "a) 1 \nb) 2 \nc) 3 \nd) 4",
        "resposta_correta": "d"
    },
]

# Lista de alunos e senhas
ALUNOS = {
    "aluno1": "senha1",
}


def verificar_credential(matricula, senha):
    return ALUNOS.get(matricula) == senha

def enviar_questao(client_socket, questao):
    client_socket.sendall(questao["enunciado"].encode())
    client_socket.sendall("\n".encode())
    # for alternativa in questao["alternativas"]:
    #     client_socket.sendall(alternativa.encode())
    #     client_socket.sendall("\n".encode())

    client_socket.sendall(questao["alternativas"].encode())
    client_socket.sendall("\n".encode())

def main():
    acertos = 0

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8080))
    server_socket.listen(1)

    print("Servidor aguardando conexões...")

    client_socket, address = server_socket.accept()
    print(f"Conexão estabelecida com {address}")

    matricula = client_socket.recv(1024).decode()
    senha = client_socket.recv(1024).decode()

    if verificar_credential(matricula, senha):
        print(f"Aluno {matricula} autenticado")
        client_socket.sendall("Autenticado\n".encode())

        for questao in QUESTOES:
            enviar_questao(client_socket, questao)
            resposta = client_socket.recv(1024).decode().strip().lower()
            if resposta == questao["resposta_correta"]:
                client_socket.sendall("Resposta correta!\n".encode())
                acertos+=1
            else:
                client_socket.sendall("Resposta incorreta!\n".encode())
    else:
        print(f"Tentativa de login com credenciais inválidas: {matricula}, {senha}")
        client_socket.sendall("Credenciais inválidas\n".encode())

    client_socket.close()

if __name__ == "__main__":
    main()
