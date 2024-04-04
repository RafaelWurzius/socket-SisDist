import socket
import time
def main():
    matricula = input("Matrícula: ")
    senha = input("Senha: ")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(("localhost", 8080))

    server_socket.sendall(matricula.encode())
    time.sleep(0.1)
    server_socket.sendall(senha.encode())

    response = server_socket.recv(1024).decode()
    print(response)

    
    while True:
        data = server_socket.recv(1024).decode()

        if not data:
            break

        print(data)
 
        resposta = input("Sua resposta: ").strip().lower()
        server_socket.sendall(resposta.encode())

        correcao = server_socket.recv(1024).decode()
        print(correcao)

    server_socket.close()

if __name__ == "__main__":
    main()
