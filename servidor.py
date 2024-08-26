import socketserver  # Importa o módulo socketserver para criar servidores de rede
import sys  # Importa o módulo sys para manipulação de exceções e saída do programa
import ast
class Servidor:
    prompt = "HOST"  # Define um atributo de classe para o prompt do servidor
    
    def __init__(self, _info):
        self.info = _info  # Armazena as informações do servidor
        Servidor.prompt = self.info.host_name  # Atualiza o prompt do servidor com o nome do host
        
    def run(self):
        # Cria um servidor TCP usando as informações de host e porta fornecidas
        with socketserver.TCPServer((self.info.HOST_SERVER, self.info.PORT_SERVER), ComunicadorTCPHandler) as server:
            try:
                server.serve_forever()  # Inicia o servidor para aceitar conexões indefinidamente
            finally:
                server.shutdown()  # Garante que o servidor seja desligado corretamente

    def calcular_finger_table(self):
        # Calcula a Finger Table para o nó
        finger_table = []
        base_no = 3000
        intervalo = 100
        for i in range(1, 5):  # Exemplo: Finger Table com 4 entradas
            finger_no = base_no + (2 ** i) * intervalo
            finger_table.append(finger_no)
        return finger_table

# Codigo novo atualizado, faz a parte do detentor
#   COMO ENVIAR MENSAGEM 28 localhost 3000 detentor


class ComunicadorTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        run, msg = True, ""  # Inicializa variáveis de controle e mensagem
        while run:
            try:
                self.data = self.request.recv(1024).strip()  # Recebe dados do cliente (até 1024 bytes) e remove espaços em branco
                msg = self.data.decode('utf-8')  # Decodifica os dados recebidos para string
                print("PEER : {0}, Menssagem: {1}\n{2}:>> ".format(self.client_address[0], msg, Servidor.prompt), end="")
                
                # Adiciona a lógica para o comando "detentor"
                if "detentor" in msg.lower():
                    # Parsing da mensagem no formato esperado
                    try:
                        parsed_msg = ast.literal_eval(msg)
                        chave = parsed_msg[0]  # Extrai a chave do formato [K, IP, PORTA, COMANDO]
                        
                        # Verifica se a chave é um número
                        if isinstance(chave, int):
                            chave_int = chave
                        else:
                            # Se a chave é uma string com aspas, remova as aspas e converta para inteiro
                            if isinstance(chave, str):
                                chave = chave.strip('\"')
                                try:
                                    chave_int = int(chave)
                                except ValueError:
                                    chave_int = -1  # Valor padrão para chave inválida
                            else:
                                chave_int = -1  # Valor padrão para chave inválida
                            
                        no = self.determinar_no(chave_int)  # Determina o nó correto com base na chave
                        # Envia a mensagem de resposta ao cliente
                        self.request.sendall(f"O detentor da chave {chave} é o {no}".encode('utf-8'))
                    except Exception as e:
                        print(f"Erro ao processar a mensagem: {e}")
                        self.request.sendall(f"Erro ao processar a mensagem".encode('utf-8'))
                else:
                    # Se não for o comando "detentor", envia a mensagem em maiúsculas de volta
                    self.request.sendall(self.data.upper())

            except Exception as e:
                print(f"********* CONNECTION DOWN: {e} *********")  # Imprime uma mensagem de erro se a conexão cair
                sys.exit()  # Encerra o programa
            
            if str(msg).strip().lower() == "exit":  # Verifica se a mensagem é "exit"
                print("Antecessor({0}) saiu (e informou)!!!".format(Servidor.prompt))  # Imprime uma mensagem de saída
                sys.exit()  # Encerra o programa

# parte para verificar se a chave é um número e determinar o nó correto
    def determinar_no(self, chave):
        # Lógica para determinar o nó correto com base na chave
        try:
            if chave == -1:
                return "NÓ_INVÁLIDO"
            base_no = 3000
            intervalo = 100
            no = base_no + (chave // intervalo) * 100
            return no
        except ValueError:
            # Se a chave não for um número, retorna um nó padrão ou uma mensagem de erro
            return "NÓ_INVÁLIDO"