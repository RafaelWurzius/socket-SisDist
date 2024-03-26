import socket
import sys

def main():
    if len(sys.argv) != 2:
        print("Uso: python cliente.py <URL>")
        return

    url = sys.argv[1]
    parts = url.split("/")
    protocol = parts[0]
    address = parts[2].split(":")
    ip = address[0]
    port = int(address[1])
    filename = "/".join(parts[3:])

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        request = f"GET /{filename} HTTP/1.1\r\nHost: {ip}:{port}\r\n\r\n"
        client_socket.send(request.encode())

        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        print(response.decode())
        client_socket.close()
    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()
