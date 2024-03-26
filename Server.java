package socket;

import java.io.*;
import java.net.*;

public class Server {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Uso: java Server <porta> <diretorio>");
            System.exit(1);
        }

        int porta = Integer.parseInt(args[0]);
        String diretorio = args[1];

        try {
            ServerSocket serverSocket = new ServerSocket(porta);
            System.out.println("Servidor escutando na porta " + porta + "...");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Conexao estabelecida com " + clientSocket.getInetAddress() + ":" + clientSocket.getPort());
                Thread t = new Thread(new ClientHandler(clientSocket, diretorio));
                t.start();
            }
        } catch (IOException e) {
            System.err.println("Erro ao iniciar o servidor: " + e.getMessage());
        }
    }
}

class ClientHandler implements Runnable {
    private Socket clientSocket;
    private String diretorio;

    public ClientHandler(Socket socket, String dir) {
        this.clientSocket = socket;
        this.diretorio = dir;
    }

    @Override
    public void run() {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            DataOutputStream out = new DataOutputStream(clientSocket.getOutputStream());

            String request = in.readLine();
            System.out.println("Requisicao recebida: " + request);
            System.out.println("Diretorio: " + diretorio);

            String[] parts = request.split(" ");
            String filename = parts[1];

            File file = new File(diretorio + filename);
            System.out.println("File path: " + diretorio + filename);
            System.out.println("Absolute file path: " + file.getAbsolutePath());
            
            if (file.exists()) {
                out.writeBytes("HTTP/1.1 200 OK\r\n\r\n");
                FileInputStream fis = new FileInputStream(file);
                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = fis.read(buffer)) != -1) {
                    out.write(buffer, 0, bytesRead);
                }
                fis.close();
            } else {
                out.writeBytes("HTTP/1.1 404 Not Found\r\n\r\n");
                out.writeBytes("<html><body><h1>404 Not Found</h1></body></html>");
            }

            out.close();
            in.close();
            clientSocket.close();
        } catch (IOException e) {
            System.err.println("Erro ao lidar com o cliente: " + e.getMessage());
        }
    }
}
