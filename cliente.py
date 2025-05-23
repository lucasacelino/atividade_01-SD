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
            
            # Thread para receber mensagens
            threading.Thread(target=self.receive_messages, daemon=True).start()
            
            while True:
                message = input("Digite uma mensagem ou 'sair': ")
                if message.lower() == 'sair':
                    break
                self.client_socket.sendall(message.encode('utf-8'))

        except Exception as e:
            print(f"Erro na conexão: {e}")
        finally:
            self.client_socket.close()
            print("Conexão encerrada.")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f"Resposta do servidor: {data.decode('utf-8')}")
            except:
                break

if __name__ == "__main__":
    client = Client()
    client.connect()
