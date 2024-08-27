import socketserver
import sys
import ast
from pprint import pprint

class Servidor:
    prompt = "HOST"

    def __init__(self, _info):
        self.info = _info
        self.finger_table = self.calcular_finger_table()

    def run(self):
        with socketserver.TCPServer((self.info.HOST_SERVER, self.info.PORT_SERVER), ComunicadorTCPHandler) as server:
            try:
                server.finger_table = self.finger_table  # Passa a Finger Table para o servidor
                server.serve_forever()
            finally:
                server.shutdown()

    def calcular_finger_table(self):
        finger_table = []
        base_no = 3000
        intervalo = 100
        for i in range(1, 5):
            finger_no = base_no + (2 ** i) * intervalo
            finger_table.append(finger_no)
        return finger_table

    def get_fingers(self, nodes, m):
        nodes_augment = nodes.copy()
        nodes_augment = sorted(nodes_augment)
        maxnum = pow(2, m)
        nodes_augment.append(nodes_augment[0] + maxnum)

        finger_table = {}
        for node in nodes:
            fingers = [None] * m
            for i in range(m):
                j = (node + pow(2, i)) % maxnum
                fingers[i] = self.successor(nodes_augment, j) % maxnum
            finger_table[node] = fingers.copy()

        return finger_table

    def successor(self, L, n):
        found, midpoint = self.binarySearch(L, n)
        if L[midpoint] >= n:
            return L[midpoint]
        if L[midpoint] < n:
            if midpoint == len(L) - 1:
                return None
            return L[midpoint + 1]

    def binarySearch(self, alist, item):
        first = 0
        last = len(alist) - 1
        found = False

        while first <= last and not found:
            midpoint = (first + last) // 2
            if alist[midpoint] == item:
                found = True
            else:
                if item < alist[midpoint]:
                    last = midpoint - 1
                else:
                    first = midpoint + 1

        return found, midpoint

    def get_key_loc(self, nodes, key, m):
        finger_table = self.get_fingers(nodes, m)
        for node, fingers in finger_table.items():
            if key in fingers:
                return node
        return None

    def get_query_path(self, nodes, key, query_node, m):
        path = [query_node]
        finger_table = self.get_fingers(nodes, m)
        while query_node != self.get_key_loc(nodes, key, m):
            next_node = finger_table[query_node][0]
            path.append(next_node)
            query_node = next_node
        return path

class ComunicadorTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        run, msg = True, ""
        while run:
            try:
                self.data = self.request.recv(1024).strip()
                msg = self.data.decode('utf-8')
                print(f"PEER: {self.client_address[0]}, Mensagem: {msg}\n{Servidor.prompt}:>> ", end="")

                if "detentor" in msg.lower():
                    try:
                        parsed_msg = ast.literal_eval(msg)
                        chave = parsed_msg[0]
                        chave_int = int(chave) if isinstance(chave, (int, str)) else -1
                        no = self.determinar_no(chave_int)
                        self.request.sendall(f"O detentor da chave {chave} é o {no}".encode('utf-8'))
                    except Exception as e:
                        print(f"Erro ao processar a mensagem: {e}")
                        self.request.sendall("Erro ao processar a mensagem".encode('utf-8'))
                elif "finger_table" in msg.lower():
                    finger_table_str = ', '.join(map(str, self.server.finger_table))
                    print(f"Finger Table: {finger_table_str}")
                    self.request.sendall(f"Finger Table: {finger_table_str}".encode('utf-8'))
                else:
                    self.request.sendall(self.data.upper())

            except Exception as e:
                print(f"********* CONNECTION DOWN: {e} *********")
                sys.exit()

            if str(msg).strip().lower() == "exit":
                print(f"Antecessor({Servidor.prompt}) saiu (e informou)!!!")
                sys.exit()

    def determinar_no(self, chave):
        try:
            if chave == -1:
                return "NÓ_INVÁLIDO"

            # Ordenar a finger table
            sorted_finger_table = sorted(self.server.finger_table)

            # Determinar o nó responsável pela chave
            for i in range(len(sorted_finger_table)):
                no_atual = sorted_finger_table[i]
                no_proximo = sorted_finger_table[(i + 1) % len(sorted_finger_table)]

                # Verifica se a chave está no intervalo entre no_atual e no_proximo - 1
                if no_atual <= chave < no_proximo:
                    return no_atual

                # Casos onde a chave está no intervalo que "dá a volta" no anel
                if i == len(sorted_finger_table) - 1 and (chave >= no_atual or chave < sorted_finger_table[0]):
                    return no_atual

            return "NÓ_NÃO_ENCONTRADO"
        except ValueError:
            return "NÓ_INVÁLIDO"