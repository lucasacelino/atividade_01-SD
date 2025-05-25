import socket
import threading

class Cliente:
    def __init__(self, host='127.0.0.1', porta=12345):
        self.host = host
        self.porta = porta
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True


    def connect(self):
        try:
            self.client_socket.connect((self.host, self.porta))
            print(f"Conectado ao servidor {self.host}:{self.porta}")
            
            receive_thread = threading.Thread(target=self.receber_mensagens_servidor)
            receive_thread.daemon = True
            receive_thread.start()
            
            send_thread = threading.Thread(target=self.enviar_mensagens)
            send_thread.daemon = True
            send_thread.start()
            
            send_thread.join()
            
        except Exception as e:
            print(f"Erro na conexão: {e}")
            self.running = False
        finally:
            self.client_socket.close()
            print("Conexão encerrada.")


    def receber_mensagens_servidor(self):
        while self.running:
            try:
                dados = self.client_socket.recv(1024)
                if not dados:
                    self.running = False
                    break
                print(f"\nMensagem do servidor: {dados.decode('utf-8')}")
                # print("Digite uma mensagem ou 'sair': ", end='', flush=True)
            except ConnectionResetError:
                print("\nConexão com o servidor foi resetada")
                self.running = False
                break
            except Exception as e:
                print(f"\nErro ao receber mensagem: {e}")
                self.running = False
                break


    def enviar_mensagens(self):
        while self.running:
            try:
                mensagem = input("Digite uma mensagem ou 'sair': ")
                if mensagem.lower() == 'sair':
                    self.running = False
                    break
                self.client_socket.sendall(mensagem.encode('utf-8'))
            except Exception as e:
                print(f"\nErro ao enviar mensagem: {e}")
                self.running = False
                break


if __name__ == "__main__":
    cliente = Cliente()
    cliente.connect()