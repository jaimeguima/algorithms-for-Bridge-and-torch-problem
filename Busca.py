from collections import deque
import heapq
import time


class Busca:

    def __init__(self, grafo):
        self.grafo = grafo

        inicial = [0, 0, 0, 0, 0]
        objetivo = [1, 1, 1, 1, 1]

        self.estado_inicial = grafo.estado_para_numero(inicial)
        self.estado_objetivo = grafo.estado_para_numero(objetivo)
        
        self.limite_nos = 10000  # Limite para evitar loops infinitos/muito longos

    def heuristica(self, estado_num):
        """Função heurística h(n) baseada na posição da tocha."""
        estado = self.grafo.numero_para_estado(estado_num)
        tempos = self.grafo.tempos
        
        origem = [tempos[i] for i in range(4) if estado[i] == 0]
        destino = [tempos[i] for i in range(4) if estado[i] == 1]
        
        if not origem:  # Estado objetivo alcançado
            return 0
            
        if estado[4] == 0:  # Tocha na origem
            return max(origem)
        else:               # Tocha no destino
            return max(origem) + min(destino) if destino else max(origem)

    def imprimir_metricas(self, nome_algoritmo, custo, nos_expandidos, tempo):
        print(f"[{nome_algoritmo}]")
        print(f" -> Custo da solução (Tempo total): {custo} minutos")
        print(f" -> Nós expandidos: {nos_expandidos}")
        print(f" -> Tempo de processamento: {tempo:.6f} segundos")

    def busca_profundidade(self):
        inicio_tempo = time.perf_counter()
        
        pilha = [self.estado_inicial]
        visitado = [False] * 32
        pai = [-1] * 32
        g_custo = [0] * 32  # Rastreia o custo acumulado
        
        nos_expandidos = 0

        while pilha:
            atual = pilha.pop()

            if visitado[atual]:
                continue

            visitado[atual] = True
            nos_expandidos += 1
            
            if nos_expandidos > self.limite_nos:
                print("Limite de nós atingido na DFS!")
                return False

            if atual == self.estado_objetivo:
                tempo_total = time.perf_counter() - inicio_tempo
                self.imprimir_metricas("Busca em Profundidade (DFS)", g_custo[atual], nos_expandidos, tempo_total)
                self.imprimir_caminho(pai, self.estado_objetivo)
                return True

            for aresta in self.grafo.get_adjacencias(atual):
                proximo = self.grafo.estado_para_numero(aresta.destino)
                if not visitado[proximo]:
                    pai[proximo] = atual
                    g_custo[proximo] = g_custo[atual] + aresta.custo
                    pilha.append(proximo)

        return False

    def busca_largura(self):
        inicio_tempo = time.perf_counter()
        
        fila = deque([self.estado_inicial])
        visitado = [False] * 32
        pai = [-1] * 32
        g_custo = [0] * 32
        
        visitado[self.estado_inicial] = True
        nos_expandidos = 0

        while fila:
            atual = fila.popleft()
            nos_expandidos += 1
            
            if nos_expandidos > self.limite_nos:
                print("Limite de nós atingido na BFS!")
                return False

            if atual == self.estado_objetivo:
                tempo_total = time.perf_counter() - inicio_tempo
                self.imprimir_metricas("Busca em Largura (BFS)", g_custo[atual], nos_expandidos, tempo_total)
                self.imprimir_caminho(pai, self.estado_objetivo)
                return True

            for aresta in self.grafo.get_adjacencias(atual):
                proximo = self.grafo.estado_para_numero(aresta.destino)
                if not visitado[proximo]:
                    visitado[proximo] = True
                    pai[proximo] = atual
                    g_custo[proximo] = g_custo[atual] + aresta.custo
                    fila.append(proximo)

        return False

    def busca_custo_uniforme(self):
        inicio_tempo = time.perf_counter()
        
        # Fila de prioridade armazena tuplas: (custo_acumulado, estado_atual)
        fila_prioridade = [(0, self.estado_inicial)]
        
        visitado = [False] * 32
        pai = [-1] * 32
        g_custo = [float('inf')] * 32
        g_custo[self.estado_inicial] = 0
        
        nos_expandidos = 0
        
        while fila_prioridade:
            custo_atual, atual = heapq.heappop(fila_prioridade)
            
            if visitado[atual]:
                continue
                
            visitado[atual] = True
            nos_expandidos += 1
            
            if nos_expandidos > self.limite_nos:
                print("Limite de nós atingido no UCS!")
                return False
                
            if atual == self.estado_objetivo:
                tempo_total = time.perf_counter() - inicio_tempo
                self.imprimir_metricas("Busca de Custo Uniforme (UCS)", custo_atual, nos_expandidos, tempo_total)
                self.imprimir_caminho(pai, self.estado_objetivo)
                return True
                
            for aresta in self.grafo.get_adjacencias(atual):
                proximo = self.grafo.estado_para_numero(aresta.destino)
                novo_custo = custo_atual + aresta.custo
                
                if novo_custo < g_custo[proximo]:
                    g_custo[proximo] = novo_custo
                    pai[proximo] = atual
                    heapq.heappush(fila_prioridade, (novo_custo, proximo))

        return False

    def busca_a_estrela(self):
        inicio_tempo = time.perf_counter()
        
        # Fila de prioridade armazena: (f(n), custo_acumulado, estado_atual)
        # f(n) = g(n) + h(n)
        fila_prioridade = [(self.heuristica(self.estado_inicial), 0, self.estado_inicial)]
        
        visitado = [False] * 32
        pai = [-1] * 32
        g_custo = [float('inf')] * 32
        g_custo[self.estado_inicial] = 0
        
        nos_expandidos = 0
        
        while fila_prioridade:
            f_n, custo_atual, atual = heapq.heappop(fila_prioridade)
            
            if visitado[atual]:
                continue
                
            visitado[atual] = True
            nos_expandidos += 1
            
            if nos_expandidos > self.limite_nos:
                print("Limite de nós atingido no A*!")
                return False
                
            if atual == self.estado_objetivo:
                tempo_total = time.perf_counter() - inicio_tempo
                self.imprimir_metricas("Busca A*", custo_atual, nos_expandidos, tempo_total)
                self.imprimir_caminho(pai, self.estado_objetivo)
                return True
                
            for aresta in self.grafo.get_adjacencias(atual):
                proximo = self.grafo.estado_para_numero(aresta.destino)
                novo_custo = custo_atual + aresta.custo
                
                if novo_custo < g_custo[proximo]:
                    g_custo[proximo] = novo_custo
                    pai[proximo] = atual
                    f_novo = novo_custo + self.heuristica(proximo)
                    heapq.heappush(fila_prioridade, (f_novo, novo_custo, proximo))

        return False

    def imprimir_caminho(self, pai, objetivo):
        caminho = []
        atual = objetivo

        while atual != -1:
            caminho.append(atual)
            atual = pai[atual]

        caminho.reverse()
        print("Caminho encontrado:")

        for i, estado in enumerate(caminho):
            self.grafo.imprimir_estado(self.grafo.numero_para_estado(estado))
            if i + 1 < len(caminho):
                print(" -> ", end="")
        print("\n" + "-"*50)