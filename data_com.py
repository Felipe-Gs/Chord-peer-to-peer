class DataCom:
    SHOST = "localhost"
    SPORT = 3000
    FAIXA = 100
    
    def __init__(self, filename, numero_de_pares: int) -> None:
        if(numero_de_pares <= 0):
            numero_de_pares = 1
        self.SIZE = numero_de_pares
        self.MAP = []
        for a in range(self.SIZE):
            server_port, client_port = a, (a + 1)
            if(client_port < self.SIZE):
                self.MAP.append([server_port, client_port])
            else:
                self.MAP.append([server_port, 0])
        self.IdxMap = self.__config_ports(filename)
        
    def __config_ports(self, filename):
        _port = int(-1)
        try:
            with open(filename, 'r') as f: 
                _port = int(f.read())
            with open(filename, 'w') as f: 
                f.write(str(_port + 1))
        except IOError:
            print("Erro ao ler arquivo!")
            sys.exit()

        I = _port % self.SIZE
        self.HOST_SERVER = DataCom.SHOST
        self.PORT_SERVER = self.MAP[I][0] * DataCom.FAIXA + DataCom.SPORT
        self.SUCESSOR = self.MAP[I][1] * DataCom.FAIXA + DataCom.SPORT
        self.sucessor_name = "NO[{0}]".format(self.SUCESSOR)
        self.host_name = "NO[{0}]".format(self.PORT_SERVER)
        Ant_I = I - 1 if I - 1 >= 0 else self.SIZE - 1
        
        if Ant_I < len(self.MAP):
            self.antecessor_name = "NO[{0}]".format(self.MAP[Ant_I][0] * DataCom.FAIXA + DataCom.SPORT)
        else:
            self.antecessor_name = "NO[UNKNOWN]"
        
        self.setF(I)
        
        return I
    
    def __repr__(self) -> str:
        s = "Servidor({0}), PortServer({1}), SUCESSOR({2} -> FAIXA[{3}-{4}]) ....".format(
            self.HOST_SERVER, str(self.PORT_SERVER), str(self.SUCESSOR), self.Fi, self.Fj)
        return s + "\nCliente vai conectar assim: ESCUTA({0}), SUCESOR({1}), OK!!".format(
            self.HOST_SERVER, str(self.SUCESSOR))
    
    def setF(self, I: int):
        self.Fi = int(self.SUCESSOR - DataCom.FAIXA + 1)
        self.Fj = int(self.SUCESSOR - DataCom.SPORT)
        if(I + 1 == self.SIZE):
            self.Fi = int(self.PORT_SERVER - DataCom.SPORT + 1) 
    
    def calcular_finger_table(self):
        self.finger_table = []
        m = self.SIZE
        max_num = 2 ** m
        for i in range(m):
            finger = (self.PORT_SERVER + 2 ** i) % max_num
            sucessor = self.encontrar_sucessor(finger)
            self.finger_table.append(sucessor)

    def encontrar_sucessor(self, finger):
        for par in self.MAP:
            port = par[0] * DataCom.FAIXA + DataCom.SPORT
            if port >= finger:
                return port
        return self.MAP[0][0] * DataCom.FAIXA + DataCom.SPORT