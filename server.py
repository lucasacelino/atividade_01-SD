import socket
import threading
from datetime import datetime

class Servidor:
    def __init__(self, host='0.0.0.0', porta=12345):
        self.host = host
        self.porta = porta
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes_conectados = {}
        self.lock = threading.Lock()

    def iniciar_servidor(self):
        self.server_socket.bind((self.host, self.porta))
        self.server_socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.porta}. Aguardando conexões...")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                ip, port = client_address

                with self.lock:
                    
                    #Múltiplos clientes com o mesmo IP, mas com porta diferentes
                    client_id = f"{ip}:{port}"
                    
                    #Atendendo a restrição de IPs duplicados
                    # client_id = ip

                    if client_id in self.clientes_conectados:
                        client_socket.send("Erro: IP já conectado.".encode('utf-8'))
                        client_socket.close()
                        continue

                    if len(self.clientes_conectados) >= 5:
                        client_socket.send("Erro: Limite de 5 conexões atingido.".encode('utf-8'))
                        client_socket.close()
                        continue

                    self.clientes_conectados[client_id] = client_socket
                    print(self.clientes_conectados)
                    print(f"Conexão estabelecida com {ip}:{port}. Total: {len(self.clientes_conectados)}")

                threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()

        except KeyboardInterrupt:
            print("\nServidor encerrando...")
        finally:
            self.server_socket.close()
    
    
    def handle_client(self, client_socket, client_address):
        ip, port = client_address
        client_id = f"{ip}:{port}"

        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break

                print(f"[{ip}:{port}] Mensagem: {message}")

                if message.startswith("comando:"):
                    response = self.comandos_especiais(message, ip, port)
                else:
                    response = f"Echo: {message}"

                client_socket.send(response.encode('utf-8'))

        except ConnectionResetError:
            print(f"Conexão com {ip}:{port} perdida")
        finally:
            with self.lock:
                if client_id in self.clientes_conectados:
                    del self.clientes_conectados[client_id]
                    print(f"Conexão com {ip}:{port} encerrada. Total: {len(self.clientes_conectados)}")
            client_socket.close()


    def comandos_especiais(self, comando, client_ip, client_port):
        cmd = comando.strip()
        if cmd == "comando:1":
            return datetime.now().strftime("Data: %Y-%m-%d\n")
        elif cmd == "comando:2":
            return datetime.now().strftime("Hora: %H:%M:%S\n")
        elif cmd == "comando:3":
            return (
                f"\nServidor: {self.host}:{self.porta}\n"
                f"Cliente: {client_ip}:{client_port}\n"
                f"Status: Conexão ativa com o servidor.\n"
            )
        elif cmd == "comando:4":
            with self.lock:
                return f"Clientes conectados ({len(self.clientes_conectados)}):\n" + "\n".join(self.clientes_conectados.keys()) + "\n"
        else:
            return "Comando inválido"


if __name__ == "__main__":
    server = Servidor()
    server.iniciar_servidor()