# ==========================================================
# PROJETO DE VISUALIZAÇÃO DE INFORMAÇÕES - NETFLIX
# ==========================================================
# Autor: Rafael Mocellin Leszczynski
# RGM: 28599535
# Disciplina: Visualização de Informações
# Instituição: Universidade Cruzeiro do Sul
# Data: 08/05/2026
# Tema: Análise do catálogo da Netflix
# ==========================================================

# =========================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =========================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import networkx as nx
import os

# =========================
# CONFIGURAÇÕES
# =========================

sns.set(style="whitegrid")

# Criar pasta para salvar gráficos
if not os.path.exists("graficos"):
    os.makedirs("graficos")

# =========================
# CARREGAMENTO DO DATASET
# =========================

print("Carregando dataset...")

df = pd.read_csv("netflix_titles.csv")

print("\nDataset carregado com sucesso!")
print(df.head())

# =========================
# LIMPEZA DOS DADOS
# =========================

print("\nRealizando limpeza dos dados...")

# Remover linhas com dados essenciais ausentes
df = df.dropna(subset=['country', 'listed_in', 'cast'])

print("\nDados após limpeza:")
print(df.info())

# ==========================================================
# VISUALIZAÇÃO 1 - GRÁFICO DE BARRAS
# ==========================================================
# Categoria: Estatística Descritiva
# Objetivo: Mostrar os gêneros mais frequentes
# ==========================================================

print("\nGerando gráfico de barras...")

# Separando gêneros
genres = df['listed_in'].str.split(', ').explode()

# Contagem dos gêneros
top_genres = genres.value_counts().head(10)

# Criando gráfico
plt.figure(figsize=(12, 6))

sns.barplot(
    x=top_genres.values,
    y=top_genres.index
)

plt.title("Top 10 Gêneros da Netflix", fontsize=16)
plt.xlabel("Quantidade")
plt.ylabel("Gênero")

plt.tight_layout()

# Salvar gráfico
plt.savefig("graficos/barras_generos.png")

plt.show()

# ==========================================================
# VISUALIZAÇÃO 2 - GRÁFICO DE LINHAS
# ==========================================================
# Categoria: Visualização Temporal
# Objetivo: Evolução dos lançamentos ao longo do tempo
# ==========================================================

print("\nGerando gráfico temporal...")

# Contagem por ano
year_count = df['release_year'].value_counts().sort_index()

plt.figure(figsize=(14, 6))

plt.plot(
    year_count.index,
    year_count.values,
    marker='o'
)

plt.title("Lançamentos da Netflix por Ano", fontsize=16)
plt.xlabel("Ano")
plt.ylabel("Quantidade de Produções")

plt.grid(True)

plt.tight_layout()

# Salvar gráfico
plt.savefig("graficos/linha_lancamentos.png")

plt.show()

# ==========================================================
# VISUALIZAÇÃO 3 - MAPA GEOGRÁFICO
# ==========================================================
# Categoria: Visualização Geográfica
# Objetivo: Mostrar produções por país
# ==========================================================

print("\nGerando mapa geográfico...")

# Separando países
countries = df['country'].str.split(', ').explode()

# Contagem
country_count = countries.value_counts().reset_index()

country_count.columns = ['country', 'count']

# Criando mapa
fig_map = px.choropleth(
    country_count,
    locations='country',
    locationmode='country names',
    color='count',
    title='Produções da Netflix por País',
    color_continuous_scale='Reds'
)

# Salvar mapa
fig_map.write_html("graficos/mapa_paises.html")

fig_map.show()

# ==========================================================
# VISUALIZAÇÃO 4 - TREEMAP
# ==========================================================
# Categoria: Visualização Hierárquica
# Objetivo: Mostrar hierarquia entre tipo e gênero
# ==========================================================

print("\nGerando Treemap...")

df_treemap = df.copy()

# Pegando primeiro gênero
df_treemap['genre'] = (
    df_treemap['listed_in']
    .str.split(', ')
    .str[0]
)

# Criar treemap
fig_tree = px.treemap(
    df_treemap,
    path=['type', 'genre'],
    title='Hierarquia do Conteúdo da Netflix'
)

# Salvar
fig_tree.write_html("graficos/treemap.html")

fig_tree.show()

# ==========================================================
# ==========================================================
# VISUALIZAÇÃO 5 - NODE LINK (REDE)
# ==========================================================

print("\nGerando rede de atores...")

G = nx.Graph()

# Pegando amostra menor
sample = df.head(15)

for cast in sample['cast']:

    actors = cast.split(', ')[:4]

    for i in range(len(actors)):
        for j in range(i + 1, len(actors)):

            actor1 = actors[i]
            actor2 = actors[j]

            G.add_edge(actor1, actor2)

# Criar figura
plt.figure(figsize=(12, 8))

# Melhor distribuição visual
pos = nx.spring_layout(
    G,
    k=0.8,
    seed=42
)

nx.draw_networkx(
    G,
    pos,
    with_labels=True,
    font_size=8,
    node_size=700
)

plt.title("Rede de Conexões entre Atores")

plt.axis('off')

plt.show()

# ==========================================================
# ANÁLISE DOS RESULTADOS
# ==========================================================

print("\n================================================")
print("ANÁLISE DOS RESULTADOS")
print("================================================")

print("""
1. Os gêneros dramáticos e comédias predominam na plataforma.

2. O número de lançamentos cresce fortemente após 2015.

3. Estados Unidos e Índia aparecem entre os maiores produtores.

4. Filmes ocupam maior proporção do catálogo.

5. A rede de atores mostra conexões frequentes entre artistas.
""")

# ==========================================================
# CONCLUSÃO
# ==========================================================

print("================================================")
print("CONCLUSÃO")
print("================================================")

print("""
O projeto demonstrou como diferentes técnicas de visualização
podem complementar a análise de um mesmo dataset.

As visualizações permitiram identificar:
- padrões;
- tendências temporais;
- distribuição geográfica;
- relações hierárquicas;
- conexões entre atores.

Todas as técnicas utilizadas foram aplicadas de maneira integrada,
utilizando dados reais do catálogo da Netflix.
""")

print("\nProjeto finalizado com sucesso!")
print("Os gráficos foram salvos na pasta 'graficos/'")

# ==========================================================
# FIM DO PROJETO
# ==========================================================