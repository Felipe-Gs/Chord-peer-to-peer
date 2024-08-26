import threading  # Importa o módulo threading para criar e gerenciar threads
import readchar  # Importa o módulo readchar para ler caracteres do teclado
import sys  # Importa o módulo sys para acessar argumentos passados na linha de comando
from time import sleep  # Importa a função sleep do módulo time para pausar a execução
from data_com import DataCom  # Importa a classe DataCom do módulo data_com
from servidor import Servidor  # Importa a classe Servidor do módulo servidor
from cliente import Cliente  # Importa a classe Cliente do módulo cliente

if __name__ == "__main__":
    numero_de_pares = 2  # Define o número padrão de pares como 2
    if len(sys.argv) > 2:
        numero_de_pares = int(sys.argv[1])  # Se houver mais de 2 argumentos, define o número de pares com o valor do argumento

    info = DataCom("portas.txt", numero_de_pares)  # Cria uma instância de DataCom com o arquivo de portas e o número de pares
    servidor = Servidor(info)  # Cria uma instância de Servidor com as informações de DataCom
    cliente = Cliente(info)  # Cria uma instância de Cliente com as informações de DataCom

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
        tclient.join()  # Aguarda a thread do cliente terminar
        print("********** FIM CONECTADO **********")  # Imprime uma mensagem indicando que a conexão terminou
        print(repr(readchar.readkey()))  # Lê e imprime a próxima tecla pressionada
    else:
        print("********** ABORT ANTES DE CONECTAR **********")  # Imprime uma mensagem indicando que a conexão foi abortada
        cliente.close()  # Fecha a conexão do cliente
        print(repr(readchar.readkey()))  # Lê e imprime a próxima tecla pressionada