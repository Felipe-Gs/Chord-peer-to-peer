import socket  # Importa o módulo socket para comunicação de rede

class Cliente:
    def __init__(self, _info):
        self.sc = socket.socket()  # Cria um socket TCP/IP
        self.info = _info  # Armazena as informações do cliente
        self.connected = False  # Inicializa o estado de conexão como desconectado
        self.prompt = self.info.host_name + ":>> "  # Define o prompt do cliente
    
    def run(self):
        self.open()  # Abre a conexão com o servidor
        # codigo novo
        while True:
            msg = input(str(self.prompt))  # Lê a mensagem do usuário
            if msg.strip() != "":  # Verifica se a mensagem não está vazia
                # Aqui vamos enviar o protocolo específico para o comando "detentor"
                if msg.lower().startswith("detentor"):
                    chave = msg.split()[1]  # Extrai a chave da mensagem
                    self.send_protocol(chave, self.info.HOST_SERVER, self.info.PORT_SERVER, "detentor")
                else:
                    self.send(msg)  # Envia a mensagem para o servidor
                self.recive()  # Recebe a resposta do servidor
                if msg.strip().lower() == 'exit':  # Verifica se a mensagem é 'exit'
                    break  # Sai do loop e encerra a execução
    
    def send(self, msg):
        if(self.connected):  # Verifica se está conectado
            self.sc.sendall(msg.encode('utf-8'))  # Envia a mensagem codificada em UTF-8
    
    def recive(self):
        try:
            if self.connected:  # Verifica se está conectado
                rec_msg = self.sc.recv(1024).strip()  # Recebe a mensagem do servidor (até 1024 bytes) e remove espaços em branco
                rec_msg = rec_msg.decode('utf-8')  # Decodifica a mensagem recebida
                print("SUCESSOR({0}):>> {1}".format(self.info.sucessor_name, rec_msg))  # Imprime a mensagem do sucessor
        except ConnectionAbortedError as e:
            print(f"Conexão abortada: {e}")
            self.connected = False  # Define o estado de conexão como desconectado
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            self.connected = False  # Define o estado de conexão como desconectado
            
    def close(self):
        self.open()  # Abre a conexão com o servidor
        self.send("exit")  # Envia a mensagem 'exit' para o servidor
        self.recive()  # Recebe a resposta do servidor
    
    def open(self):
        if(self.connected == False):  # Verifica se não está conectado
            try:
                self.sc.connect((self.info.HOST_SERVER, self.info.SUCESSOR))  # Tenta conectar ao servidor
                self.connected = True  # Define o estado de conexão como conectado
            except IOError:
                # Imprime uma mensagem de erro se a conexão falhar
                print("SUCESSOR({0}), Host({1}), PORTA({2}) Falhou!!".format(self.info.sucessor_name, self.info.HOST_SERVER, str(self.info.SUCESSOR)))
                self.connected = False  # Define o estado de conexão como desconectado
    
    # codigo novo
    def send_protocol(self, k, ip, porta, comando):
        protocolo = f"[{k}, \"{ip}\", {porta}, \"{comando}\"]"
        print(f"Enviando protocolo: {protocolo}")
        self.send(protocolo)  # Usa o método send para enviar a mensagem
        self.recive()  # Recebe a resposta do sucessor

    
    # enviar finger table
    def enviar_com_finger_table(self, k, ip, porta, comando):
        # Lógica para encontrar a melhor entrada na Finger Table para a chave k
        for finger in reversed(self.info.finger_table):
            if finger.start <= k:
                try:
                    self.sc.connect((finger.node.HOST_SERVER, finger.node.PORT_SERVER))
                    self.send_protocol(k, ip, porta, comando)
                    return
                except Exception as e:
                    print(f"Falha ao conectar com o nó da Finger Table: {e}")
                    continue
        # Se não encontrar um nó adequado na Finger Table, envia para o sucessor
        try:
            self.sc.connect((self.info.sucessor_name, self.info.SUCESSOR))
            self.send_protocol(k, ip, porta, comando)
        except Exception as e:
            print(f"Falha ao conectar com o sucessor: {e}")