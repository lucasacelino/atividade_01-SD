import socket
import threading

class Cliente:
    def __init__(self, host='127.0.0.1', porta=12345):
        self.host = host
        self.porta = porta
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.executando_cliente = True


    def iniciar_conexao(self):
        try:
            self.client_socket.connect((self.host, self.porta))
            print(f"Conectado ao servidor {self.host}:{self.porta}")
            
            thread_recebimento = threading.Thread(target=self.receber_mensagens_servidor)
            thread_recebimento.daemon = True
            thread_recebimento.start()
            
            thread_envio = threading.Thread(target=self.enviar_mensagens)
            thread_envio.daemon = True
            thread_envio.start()
            
            thread_envio.join()
            
        except Exception as e:
            print(f"Erro na conexão: {e}")
            self.executando_cliente = False
        finally:
            self.client_socket.close()
            print("Conexão encerrada.")


    def receber_mensagens_servidor(self):
        while self.executando_cliente:
            try:
                dados = self.client_socket.recv(1024)
                if not dados:
                    self.executando_cliente = False
                    break
                print(f"\nMensagem do servidor: {dados.decode('utf-8')}")
                # print("Digite uma mensagem ou 'sair': ", end='', flush=True)
            except ConnectionResetError:
                print("\nConexão com o servidor foi resetada")
                self.executando_cliente = False
                break
            except Exception as e:
                print(f"\nErro ao receber mensagem: {e}")
                self.executando_cliente = False
                break


    def enviar_mensagens(self):
        while self.executando_cliente:
            try:
                mensagem = input("Digite uma mensagem ou 'sair': ")
                if mensagem.lower() == 'sair':
                    self.executando_cliente = False
                    break
                self.client_socket.sendall(mensagem.encode('utf-8'))
            except Exception as e:
                print(f"\nErro ao enviar mensagem: {e}")
                self.executando_cliente = False
                break


if __name__ == "__main__":
    cliente = Cliente()
    cliente.iniciar_conexao()