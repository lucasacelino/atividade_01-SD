import socket
import threading
from datetime import datetime

class Server:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_clients = {}  # Armazena IP: socket (ou ID único para localhost)
        self.lock = threading.Lock()
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}. Aguardando conexões...")
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                ip, port = client_address  # IP e porta de origem
                
                with self.lock:
                    # Permite múltiplas conexões locais, mas bloqueia IPs externos duplicados
                    client_id = f"{ip}:{port}" if ip == '127.0.0.1' else ip
                    
                    if client_id in self.connected_clients:
                        client_socket.send("Erro: Conexão duplicada.".encode('utf-8'))
                        client_socket.close()
                        continue
                    
                    if len(self.connected_clients) >= 5:
                        client_socket.send("Erro: Limite de 5 conexões atingido.".encode('utf-8'))
                        client_socket.close()
                        continue
                    
                    self.connected_clients[client_id] = client_socket
                    print(f"Conexão estabelecida com {ip}:{port}. Total: {len(self.connected_clients)}")
                
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        
        except KeyboardInterrupt:
            print("\nServidor encerrando...")
        finally:
            self.server_socket.close()
    
    def handle_client(self, client_socket, client_address):
        ip, port = client_address
        client_id = f"{ip}:{port}" if ip == '127.0.0.1' else ip
        
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                print(f"[{ip}:{port}] Mensagem: {message}")
                
                if message.startswith("comando:"):
                    response = self.process_command(message, ip)
                else:
                    response = f"Echo: {message}"
                
                client_socket.send(response.encode('utf-8'))
        
        except ConnectionResetError:
            print(f"Conexão com {ip}:{port} perdida")
        finally:
            with self.lock:
                if client_id in self.connected_clients:
                    del self.connected_clients[client_id]
                    print(f"Conexão com {ip}:{port} encerrada. Total: {len(self.connected_clients)}")
            client_socket.close()
    
    def process_command(self, command, client_ip):
        try:
            cmd = command.strip()
            if cmd == "comando:1":
                return datetime.now().strftime("Data: %Y-%m-%d")
            elif cmd == "comando:2":
                return datetime.now().strftime("Hora: %H:%M:%S")
            elif cmd == "comando:3":
                return f"Servidor: {self.host}:{self.port}\nCliente: {client_ip}\nStatus: Ativo"
            elif cmd == "comando:4":
                with self.lock:
                    ips = "\n".join([k.split(':')[0] for k in self.connected_clients.keys()])
                    return f"Clientes conectados ({len(self.connected_clients)}):\n{ips}"
            else:
                return "Comando inválido"
        except Exception as e:
            return f"Erro: {str(e)}"

if __name__ == "__main__":
    server = Server()
    server.start()