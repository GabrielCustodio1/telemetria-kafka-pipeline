import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("dados/relatorio_infracoes.csv")

contagem_motoristas = df["driver_id"].value_counts()
contagem_motoristas.plot(kind="bar")

plt.title("Total de Infrações por Motorista")
plt.xlabel("Motorista")
plt.ylabel("Quantidade de Infrações")
plt.xticks(rotation=0)
plt.savefig("imagens/grafico_infracoes.png")
plt.show()

contagem_lugares = df["tipo_local"].value_counts()
contagem_lugares.plot(kind="barh")

plt.title("Total de Infrações por Localidade")
plt.xlabel("Número de infrações")
plt.ylabel("Local")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("imagens/grafico_local.png")
plt.show()

media_excesso = df.groupby("driver_id")["excesso_kmh"].mean()
media_excesso.plot(kind="bar")

plt.title("Média de severidade de excesso por motorista")
plt.xlabel("Motorista")
plt.ylabel("Média de excesso (km/h)")
plt.xticks(rotation=0)
plt.savefig("imagens/grafico_media_excesso.png")
plt.show()