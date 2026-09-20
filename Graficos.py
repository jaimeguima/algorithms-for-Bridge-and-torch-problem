import matplotlib.pyplot as plt

algoritmos = ['DFS', 'BFS', 'UCS', 'A*']
custos = [90, 19, 17, 17]
nos = [13, 26, 26, 17]

cores = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']

# --- Gráfico 1: Custo da Solução ---
plt.figure(figsize=(7, 4))
barras_custo = plt.bar(algoritmos, custos, color=cores, zorder=2)
plt.title('Custo da Solução (Tempo em Minutos)', fontsize=12, pad=15)
plt.ylabel('Tempo Total', fontsize=10)

plt.ylim(0, max(custos) * 1.15)

plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

for barra in barras_custo:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2., altura + 1.5,
             f'{altura}', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('grafico_custo.png', dpi=300)
plt.close()

# --- Gráfico 2: Nós Expandidos ---
plt.figure(figsize=(7, 4))
barras_nos = plt.bar(algoritmos, nos, color=cores, zorder=2)
plt.title('Número de Nós Expandidos', fontsize=12, pad=15)
plt.ylabel('Quantidade de Nós', fontsize=10)

plt.ylim(0, max(nos) * 1.15)

plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

for barra in barras_nos:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2., altura + 0.5,
             f'{altura}', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('grafico_nos.png', dpi=300)
plt.close()

print("Gráficos gerados com sucesso: grafico_custo.png e grafico_nos.png")