import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Cliente {
    private static final String SERVER_ADDRESS = "127.0.0.1";
    private static final int SERVER_PORT = 12345;
    private static volatile boolean running = true;

    public static void main(String[] args) {
        try (
                Socket socket = new Socket(SERVER_ADDRESS, SERVER_PORT);
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                Scanner scanner = new Scanner(System.in)) {
            System.out.println("Conectado ao servidor " + SERVER_ADDRESS + ":" + SERVER_PORT);


            Thread receiver = new Thread(() -> {
                try {
                    String serverResponse;
                    while (running && (serverResponse = in.readLine()) != null) {
                        // Adiciona uma quebra de linha antes de respostas multi-linha
                        if (serverResponse.contains("\n")) {
                            System.out.println(serverResponse.replace("\n", "\n"));
                        } else {
                            System.out.println(serverResponse);
                        }
                        // System.out.print("Digite uma mensagem ou 'sair': ");
                    }
                } catch (IOException e) {
                    if (running) {
                        System.out.println("\nConexão com o servidor encerrada.");
                    }
                }
            });

            receiver.start();

            String userInput;
            while (running) {
                System.out.print("Digite uma mensagem ou 'sair': ");
                userInput = scanner.nextLine();
                if (userInput.equalsIgnoreCase("sair")) {
                    running = false;
                    out.println(userInput);
                    socket.close();
                    break;
                }
                out.println(userInput);
            }

        } catch (

        UnknownHostException e) {
            System.err.println("Host desconhecido: " + SERVER_ADDRESS);
        } catch (IOException e) {
            if (running) {
                System.err.println("Erro de I/O ao conectar com o servidor.");
                e.printStackTrace();
            }
        }

        System.out.println("Cliente encerrado.");
    }
}