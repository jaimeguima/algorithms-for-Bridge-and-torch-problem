from Grafo import Grafo
from Busca import Busca

def main():
    print("Iniciando análises do Problema da Ponte e Tocha...\n")
    grafo = Grafo()
    busca = Busca(grafo)

    print("=== 1. Busca em Profundidade (DFS) ===")
    busca.busca_profundidade()

    print("=== 2. Busca em Largura (BFS) ===")
    busca.busca_largura()

    print("=== 3. Busca de Custo Uniforme (UCS) ===")
    busca.busca_custo_uniforme()

    print("=== 4. Busca A* ===")
    busca.busca_a_estrela()

if __name__ == "__main__":
    main()