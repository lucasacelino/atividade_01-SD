import socket
import threading

class Client:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Conectado ao servidor {self.host}:{self.port}")
            
            # Thread para receber mensagens do servidor
            threading.Thread(target=self.receive_messages, daemon=True).start()
            
            # Loop principal para enviar mensagens
            while True:
                message = input()
                if message.lower() == 'sair':
                    break
                self.client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            self.client_socket.close()
            print("Conexão encerrada.")
    
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Resposta do servidor: {message}")
            except:
                break

if __name__ == "__main__":
    client = Client()
    client.connect()