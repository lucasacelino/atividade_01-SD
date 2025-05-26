import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
    private String host;
    private int porta;
    private Socket socket;
    private volatile boolean running;
    private BufferedReader entrada;
    private PrintWriter saida;

    public Client(String host, int porta) {
        this.host = host;
        this.porta = porta;
        this.running = true;
    }

    public void connect() {
        try {
            socket = new Socket(host, porta);
            entrada = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            saida = new PrintWriter(socket.getOutputStream(), true);
            
            System.out.println("Conectado ao servidor " + host + ":" + porta);

            Thread recebimentoThread = new Thread(this::receberMensagens);
            recebimentoThread.setDaemon(true);
            recebimentoThread.start();

            this.enviarMensagem();

            recebimentoThread.join();

        } catch (Exception e) {
            System.err.println("Erro na conexão: " + e.getMessage());
            running = false;
        } finally {
            fecharConexao();
            System.out.println("Conexão encerrada.");
        }
    }

    private void receberMensagens() {
        try {
            while (running) {
                String mensagem = entrada.readLine();
                if (mensagem == null) { 
                    running = false;
                    break;
                }
                System.out.println("\nMensagem do servidor: " + mensagem);
            }
        } catch (SocketException e) {
            if (running) {
                System.out.println("\nConexão com o servidor foi resetada");
                running = false;
            }
        } catch (IOException e) {
            if (running) {
                System.out.println("\nErro ao receber mensagem: " + e.getMessage());
                running = false;
            }
        }
    }

    private void enviarMensagem() {
        Scanner scanner = new Scanner(System.in);
        try {
            while (running) {
                System.out.print("Digite uma mensagem ou 'sair': ");
                String mensagem = scanner.nextLine();
                
                if ("sair".equalsIgnoreCase(mensagem)) {
                    running = false;
                    saida.println(mensagem);
                    break;
                }
                
                saida.println(mensagem);
            }
        } finally {
            scanner.close();
        }
    }

    private void fecharConexao() {
        try {
            if (saida != null) {
                saida.close();
            }
            if (entrada != null) {
                entrada.close();
            }
            if (socket != null && !socket.isClosed()) {
                socket.close();
            }
        } catch (IOException e) {
            System.err.println("Erro ao fechar conexão: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        Client client = new Client("127.0.0.1", 12345);
        client.connect();
    }
}
