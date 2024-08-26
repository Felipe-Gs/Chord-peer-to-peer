import sys  # Importa o módulo sys para manipulação de exceções e saída do programa

class DataCom:
    SHOST = "localhost"  # Define o host padrão como localhost
    SPORT = 3000  # Define a porta padrão do servidor como 3000
    FAIXA = 100  # Define a faixa de portas como 100
    
    def __init__(self, filename, numero_de_pares: int) -> None:
        if(numero_de_pares <= 0):
            numero_de_pares = 1  # Garante que o número de pares seja pelo menos 1
        self.SIZE = numero_de_pares  # Define o tamanho como o número de pares
        self.MAP = []  # Inicializa a lista MAP para armazenar pares de portas
        for a in range(self.SIZE):
            server_port, client_port = a, (a + 1)  # Define portas do servidor e cliente de forma circular
            if(client_port < self.SIZE):
                self.MAP.append([server_port, client_port])  # Adiciona o par de portas ao MAP
            else:
                self.MAP.append([server_port, 0])  # Se o cliente_port exceder o tamanho, volta para 0
        self.IdxMap = self.__config_ports(filename)  # Configura as portas usando o arquivo fornecido
        
    def __config_ports(self, filename):
        _port = int(-1)  # Inicializa a variável _port com -1
        try:
            with open(filename, 'r') as f: 
                _port = int(f.read())  # Lê a porta do arquivo
            with open(filename, 'w') as f: 
                f.write(str(_port + 1))  # Incrementa a porta e escreve de volta no arquivo
        except IOError:
            print("Erro ao ler arquivo!")  # Imprime mensagem de erro se não conseguir ler o arquivo
            sys.exit()  # Sai do programa

        I = _port % self.SIZE  # Calcula o índice circular
        self.HOST_SERVER = DataCom.SHOST  # Define o host do servidor
        self.PORT_SERVER = self.MAP[I][0] * DataCom.FAIXA + DataCom.SPORT  # Calcula a porta do servidor
        self.SUCESSOR = self.MAP[I][1] * DataCom.FAIXA + DataCom.SPORT  # Calcula a porta do sucessor
        self.sucessor_name = "NO[{0}]".format(self.SUCESSOR)  # Define o nome do sucessor
        self.host_name = "NO[{0}]".format(self.PORT_SERVER)  # Define o nome do host
        Ant_I = I - 1 if I - 1 >= 0 else self.SIZE - 1  # Calcula o índice do antecessor
        

        # CODIGO NOVO 
        # Verifica se o índice Ant_I está dentro dos limites da lista
        if Ant_I < len(self.MAP):
            self.antecessor_name = "NO[{0}]".format(self.MAP[Ant_I][0] * DataCom.FAIXA + DataCom.SPORT)  # Define o nome do antecessor
        else:
            self.antecessor_name = "NO[UNKNOWN]"  # Define um valor padrão se o índice estiver fora dos limites
        
        self.setF(I)  # Configura os valores Fi e Fj
        
        return I  # Retorna o índice
    
    def __repr__(self) -> str:
        # Retorna uma string representando o estado do objeto DataCom
        s = "Servidor({0}), PortServer({1}), SUCESSOR({2} -> FAIXA[{3}-{4}]) ....".format(
            self.HOST_SERVER, str(self.PORT_SERVER), str(self.SUCESSOR), self.Fi, self.Fj)
        return s + "\nCliente vai conectar assim: ESCUTA({0}), SUCESOR({1}), OK!!".format(
            self.HOST_SERVER, str(self.SUCESSOR))
    
    def setF(self, I: int):
        # Configura os valores Fi e Fj baseados no índice I
        self.Fi = int(self.SUCESSOR - DataCom.FAIXA + 1)
        self.Fj = int(self.SUCESSOR - DataCom.SPORT)
        if(I + 1 == self.SIZE):
            self.Fi = int(self.PORT_SERVER - DataCom.SPORT + 1) 
    

    # calcular o finger table
    def calcular_finger_table(self):
        self.finger_table = []
        m = self.SIZE  # Número de pares na rede
        for i in range(m):
            finger = (self.PORT_SERVER + 2**i) % (2**m)
            sucessor = self.encontrar_sucessor(finger)
            self.finger_table.append(sucessor)

    def encontrar_sucessor(self, finger):
        # Lógica para encontrar o sucessor de uma posição finger
        for par in self.MAP:
            if par[0] >= finger:
                return par[0] * DataCom.FAIXA + DataCom.SPORT
        return self.MAP[0][0] * DataCom.FAIXA + DataCom.SPORT