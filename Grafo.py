class Aresta:
    """Representa uma aresta do grafo (uma travessia possível)."""

    def __init__(self, destino, custo, pessoas):
        self.destino = destino      # Estado (lista de 5 ints) de destino
        self.custo = custo          # Custo (tempo) da travessia
        self.pessoas = pessoas      # Lista com os índices das pessoas que atravessaram


class Grafo:

    tempos = [1, 2, 5, 10]

    def __init__(self):
        self.adjacencias = [[] for _ in range(32)]
        self.gerar_grafo()

    # ---------------------------------------------------------
    # Converte um número entre 0 e 31 para um estado.
    #
    # Exemplo:
    # 0  -> [0,0,0,0,0]
    # 31 -> [1,1,1,1,1]
    # ---------------------------------------------------------
    def numero_para_estado(self, numero):
        estado = [0] * 5

        for i in range(4, -1, -1):
            estado[i] = numero % 2
            numero //= 2

        return estado

    # ---------------------------------------------------------
    # Converte um estado para seu número correspondente.
    #
    # Exemplo:
    # [0,0,0,0,0] -> 0
    # [1,1,1,1,1] -> 31
    # ---------------------------------------------------------
    def estado_para_numero(self, estado):
        numero = 0

        for i in range(5):
            numero = numero * 2 + estado[i]

        return numero

    # ---------------------------------------------------------
    # Gera todos os sucessores válidos de um estado.
    # ---------------------------------------------------------
    def gerar_sucessores(self, estado):
        sucessores = []
        disponiveis = []

        # A posição 4 representa a tocha
        lado_tocha = estado[4]

        # -----------------------------------------------------
        # Identifica quais pessoas estão no mesmo lado
        # que a tocha.
        # -----------------------------------------------------
        for i in range(4):
            if estado[i] == lado_tocha:
                disponiveis.append(i)

        # -----------------------------------------------------
        # Travessias com UMA pessoa
        # -----------------------------------------------------
        for pessoa in disponiveis:
            novo_estado = estado.copy()

            # Pessoa troca de lado
            novo_estado[pessoa] = 1 - novo_estado[pessoa]

            # Tocha troca de lado
            novo_estado[4] = 1 - novo_estado[4]

            aresta = Aresta(
                destino=novo_estado,
                custo=self.tempos[pessoa],
                pessoas=[pessoa],
            )

            sucessores.append(aresta)

        # -----------------------------------------------------
        # Travessias com DUAS pessoas
        # -----------------------------------------------------
        for i in range(len(disponiveis)):
            for j in range(i + 1, len(disponiveis)):

                pessoa1 = disponiveis[i]
                pessoa2 = disponiveis[j]

                novo_estado = estado.copy()

                # As duas pessoas trocam de lado
                novo_estado[pessoa1] = 1 - novo_estado[pessoa1]
                novo_estado[pessoa2] = 1 - novo_estado[pessoa2]

                # Tocha troca de lado
                novo_estado[4] = 1 - novo_estado[4]

                # O custo é determinado pela pessoa mais lenta
                custo = max(self.tempos[pessoa1], self.tempos[pessoa2])

                aresta = Aresta(
                    destino=novo_estado,
                    custo=custo,
                    pessoas=[pessoa1, pessoa2],
                )

                sucessores.append(aresta)

        return sucessores

    # ---------------------------------------------------------
    # Gera o grafo completo.
    # ---------------------------------------------------------
    def gerar_grafo(self):
        for i in range(32):
            estado = self.numero_para_estado(i)
            self.adjacencias[i] = self.gerar_sucessores(estado)

    # ---------------------------------------------------------
    # Retorna as arestas que saem de determinado estado.
    # ---------------------------------------------------------
    def get_adjacencias(self, estado):
        return self.adjacencias[estado]

    # ---------------------------------------------------------
    # Retorna o nome da pessoa a partir do índice.
    # ---------------------------------------------------------
    def nome_pessoa(self, indice):
        nomes = {0: "A", 1: "B", 2: "C", 3: "D"}
        return nomes.get(indice, "?")

    # ---------------------------------------------------------
    # Imprime um estado.
    # ---------------------------------------------------------
    def imprimir_estado(self, estado):
        print("(" + ",".join(str(e) for e in estado) + ")", end="")

    # ---------------------------------------------------------
    # Imprime todo o grafo.
    # ---------------------------------------------------------
    def imprimir_grafo(self):
        for i in range(32):
            origem = self.numero_para_estado(i)

            print(f"\nEstado {i} ", end="")
            self.imprimir_estado(origem)
            print(":")

            for aresta in self.adjacencias[i]:
                print("  ", end="")

                # Imprime as pessoas que atravessaram
                nomes = [self.nome_pessoa(p) for p in aresta.pessoas]
                print(" e ".join(nomes), end="")

                print(" -> ", end="")
                self.imprimir_estado(aresta.destino)

                print(f" | custo: {aresta.custo} min")