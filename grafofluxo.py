import grafop as grafo

class GrafoFluxo:
    def __init__ (self,mat_adj = None,mat_adj_init = None,mat_cap = None,cap = 0,demand = 0,list = None,vert = 0,num_vert = 0,lastt = 0):
        if mat_adj == None:
            self.mat_adj = []
        else:
            self.mat_adj = mat_adj
        if mat_adj_init == None:
            self.mat_adj_init = []
        else:
            self.mat_adj_init = mat_adj_init
        if mat_cap == None:
            self.mat_cap = []
        else:
            self.mat_cap = mat_cap
        self.cap = cap
        self.demand = demand
        if list == None:
            self.list = {}
        else :
            self.list = list
        self.vert = vert
        self.num_vert = num_vert
        self.lastt = lastt

    def read_file(self,file1,file2):
        list_lesson = {}
        try:
            '''Criando dicionario de turmas e ligando as a superdemanda t'''
            file = open(file2)
            str = file.readlines()
            aux = len(str)
            file = open(file1)
            str = file.readlines()
            self.vert = aux-1
            aux = len(str)-1
            file = open(file1)
            t = self.vert + len(str)
            self.num_vert = t+1
            self.mat_adj = [[float("inf") for i in range(self.num_vert)] for j in range(self.num_vert)]
            self.mat_adj_init = [[float("inf") for i in range(self.num_vert)] for j in range(self.num_vert)]
            self.mat_cap = [[0 for i in range(self.num_vert)] for j in range(self.num_vert)]
            file.readline()
            for i in range(aux):
                '''lendo os vertices dentro do arquivo de disciplinas'''
                str = file.readline()
                str = str.split(";")
                self.vert +=1
                list_lesson[str[0]] = self.vert
                self.list[self.vert] = str[0],str[1]
                self.add_cap(list_lesson[str[0]],t,int(str[2]))
                self.add_edge(list_lesson[str[0]],t,0)
                self.demand = self.demand + int(str[2])
        except IOError:
            print("Not was possible to read the file1!")

        try:
            '''criando dicionario de professores e ligando ao vertice origem'''
            file = open(file2)
            str = file.readlines()
            file = open(file2)
            self.vert = 0
            aux = len(str)-1
            file.readline()
            for i in range(aux):
                str = file.readline()
                str = str.split(";")
                self.vert = self.vert+1
                self.list[self.vert] = str[0]
                self.lastt = self.vert
                self.add_cap(0,self.vert,int(str[1]))
                self.add_edge(0,self.vert,0)
                for i in range(5):
                    '''ligando professores as suas disciplinas com seus devidos pesos'''
                    straux = str[i+2].strip()
                    if straux != '':
                        prefer = 0
                        if i == 1:
                            prefer = 3
                        elif i == 2:
                            prefer = 5
                        elif i == 3:
                            prefer = 8
                        elif i == 4:
                            prefer = 10
                        self.add_edge(self.vert,list_lesson[straux],prefer)
                        if str[i+2] == 'CSI000':
                            self.add_cap(self.vert,list_lesson[straux],1)
                        else :
                            self.add_cap(self.vert, list_lesson[straux],2)
                    else:
                        break;
        except IOError:
            print("Not was possible to read the file2!")

    def add_edge(self,u,v,w):
        if  u < self.num_vert and v < self.num_vert:
            self.mat_adj[u][v] = w
            self.mat_adj_init[u][v] = w
        else:
            print("Invalid Edge!")

    def add_cap(self,u,v,w):
        if u < self.num_vert and v < self.num_vert:
            self.mat_cap[u][v] = w
        else:
            print("Invalid Edge!")

    def print_capmat(self):
        for elem in self.mat_cap:
            print(elem)

    def print_adjmat(self):
        for elem in self.mat_adj:
            print(elem)

    def bellman_ford(self,s):
        dist = [float("inf") for i in range(self.num_vert)]
        pred = [None for i in range(self.num_vert)]
        dist[s] = 0
        for u in range(len(self.mat_adj)):
            for v in range(len(self.mat_adj)):
                if self.mat_adj[u][v] != float("inf"):
                    if dist[v] > dist[u] + self.mat_adj[u][v]:
                        dist[v] = dist[u] + self.mat_adj[u][v]
                        pred[v] = u
        return pred

    def SMP(self):
        '''Sucessive Minimal Paths'''
        F = [[0 for elem in self.mat_adj]for elem in self.mat_adj]
        while self.demand != 0:
            C = self.bellman_ford(0)
            mincap = float("inf")
            aux = len(C) - 1
            if C[aux] == None:
                return F
            while aux != 0:
                if self.mat_cap[C[aux]][aux] < mincap:
                    mincap = self.mat_cap[C[aux]][aux]
                aux = C[aux]
            f = mincap
            aux1 = len(C) - 1
            while aux1 != 0:
                F[C[aux1]][aux1] = F[C[aux1]][aux1] + f
                self.mat_cap[C[aux1]][aux1] = self.mat_cap[C[aux1]][aux1] - f
                if self.mat_adj[aux1][C[aux1]] == float("inf"):
                    self.mat_adj[aux1][C[aux1]] = self.mat_adj[C[aux1]][aux1]*(-1)
                if self.mat_cap[C[aux1]][aux1] == 0:
                    self.mat_adj[C[aux1]][aux1] = float("inf")
                self.mat_cap[aux1][C[aux1]] = self.mat_cap[aux1][C[aux1]] + f
                if F[aux1][C[aux1]] != 0:
                    F[aux1][C[aux1]] = F[aux1][C[aux1]] - f
                aux1 = C[aux1]
            self.demand = self.demand - f
        return F

    def print_concl(self,matrix):
        print("{:<19} {:<13} {:<39} {:<8} {:<8}".format('Professor', 'Discipllina', 'Nome', '#Turmas', 'Custo'))
        for i in range(1,self.lastt):
            count = 0
            contador = 0
            control = []
            for j in range((self.lastt)+1,len(matrix[i])):
                if i > 0 and i < (self.lastt)+1 and j > self.lastt and j < len(matrix)-1 and matrix[i][j] != 0:
                    print("{:<19} {:<13} {:<39} {:<8} {:<8}".format(self.list[i],self.list[j][0],self.list[j][1],matrix[i][j],self.mat_adj_init[i][j]))
                    count += 1
            if count == 0:
                control.append(self.list[i])
        if len(control) == 0:
            print("\n\n\n")
            print("Todos os professores estão com pelo menos uma turma")
        else:
            print("\n\n\n")
            print("os professores, ",control,"não se encaixaram em nenhuma turma" )
