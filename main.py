import threading  # Importa o módulo threading para criar e gerenciar threads
import readchar  # Importa o módulo readchar para ler caracteres do teclado
import sys  # Importa o módulo sys para acessar argumentos passados na linha de comando
from time import sleep  # Importa a função sleep do módulo time para pausar a execução
from data_com import DataCom  # Importa a classe DataCom do módulo data_com
from servidor import Servidor  # Importa a classe Servidor do módulo servidor
from cliente import Cliente  # Importa a classe Cliente do módulo cliente

class Node:
    def __init__(self, identifier, total_nodes):
        self.identifier = identifier
        self.total_nodes = total_nodes
        self.finger_table = []

    def calculate_finger_table(self):
        for i in range(1, self.total_nodes + 1):
            finger_id = (self.identifier + 2**(i-1)) % self.total_nodes
            self.finger_table.append(finger_id)

    def __str__(self):
        return f"Node {self.identifier} Finger Table: {self.finger_table}"

if __name__ == "__main__":
    numero_de_pares = 2  # Define o número padrão de pares como 2
    if len(sys.argv) > 2:
        numero_de_pares = int(sys.argv[1])  # Se houver mais de 2 argumentos, define o número de pares com o valor do argumento

    info = DataCom("portas.txt", numero_de_pares)  # Cria uma instância de DataCom com o arquivo de portas e o número de pares
    servidor = Servidor(info)  # Cria uma instância de Servidor com as informações de DataCom
    cliente = Cliente(info)  # Cria uma instância de Cliente com as informações de DataCom

    # Exemplo de uso da Finger Table
    for i in range(numero_de_pares):
        node = Node(i, numero_de_pares)
        node.calculate_finger_table()
        print(node)

    tserver = threading.Thread(target=servidor.run)  # Cria uma thread para executar o método run do servidor
    tserver.start()  # Inicia a thread do servidor
    sleep(1/10)  # Pausa a execução por 0.1 segundos

    print(info)  # Imprime as informações de DataCom
    print("********** [<<ENTER>>=CONECTAR] **********")  # Imprime uma mensagem para o usuário pressionar ENTER para conectar

    enter = readchar.readkey() == '\r'  # Lê uma tecla do teclado e verifica se é ENTER

    if enter:
        print("********** [<<EXIT>>=SAIR] **********")  # Imprime uma mensagem para o usuário pressionar EXIT para sair
        tclient = threading.Thread(target=cliente.run)  # Cria uma thread para executar o método run do cliente
        tclient.start()  # Inicia a thread do cliente
        tserver.join()  # Aguarda a thread do servidor terminar