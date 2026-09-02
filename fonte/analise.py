import pandas as pd

# 1. Leitura dos dados da Camada Bronze (JSONL)
df = pd.read_json("dados/data_lake_infracoes.jsonl", lines=True)

# 2. Engenharia de atributos (Camada Prata)
df["excesso_kmh"] = df["velocidade_registrada"] - df["limite_permitido"]

# 3. Métricas analíticas para o negócio (Camada Ouro)
print("=== Total de infrações por motorista ===")
print(df["driver_id"].value_counts())

print("\n=== Média de excesso de velocidade (km/h) ===")
print(df.groupby("driver_id")["excesso_kmh"].mean())

print("\n=== Infrações por tipo de local ===")
print(df["tipo_local"].value_counts())

# 4. Exportação do relatório final
df.to_csv("relatorio_infracoes.csv", index=False)
print("\n✅ Relatório 'relatorio_infracoes.csv' exportado com sucesso!")