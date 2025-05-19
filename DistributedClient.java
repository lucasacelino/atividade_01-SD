import java.io.*;
import java.net.*;
import java.util.Scanner;

public class DistributedClient {
    private static final String SERVER_ADDRESS = "127.0.0.1";
    private static final int SERVER_PORT = 12345;
    
    public static void main(String[] args) {
        try (
            Socket socket = new Socket(SERVER_ADDRESS, SERVER_PORT);
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            Scanner scanner = new Scanner(System.in);
        ) {
            System.out.println("Conectado ao servidor " + SERVER_ADDRESS + ":" + SERVER_PORT);
            
            // Thread para receber mensagens do servidor
            new Thread(() -> {
                try {
                    String serverResponse;
                    while ((serverResponse = in.readLine()) != null) {
                        System.out.println("Resposta do servidor: " + serverResponse);
                    }
                } catch (IOException e) {
                    System.out.println("Conexão com o servidor foi encerrada.");
                }
            }).start();
            
            // Loop principal para enviar mensagens
            String userInput;
            while (true) {
                userInput = scanner.nextLine();
                if (userInput.equalsIgnoreCase("sair")) {
                    break;
                }
                out.println(userInput);
            }
        } catch (UnknownHostException e) {
            System.err.println("Host desconhecido: " + SERVER_ADDRESS);
        } catch (IOException e) {
            System.err.println("Erro de I/O para a conexão com " + SERVER_ADDRESS);
            e.printStackTrace();
        }
        System.out.println("Cliente encerrado.");
    }
}