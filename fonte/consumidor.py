import json
import math
from kafka import KafkaConsumer

# 1. Cadastro de Zonas de Risco (Escolas e Hospitais na região simulada)
ZONAS_DE_RISCO = [
    {"nome": "Hospital das Clínicas", "tipo": "hospital", "lat": -23.555, "lon": -46.652, "raio_km": 0.5},
    {"nome": "Escola Estadual Central", "tipo": "escola", "lat": -23.545, "lon": -46.638, "raio_km": 0.4}
]

ARQUIVO_DATA_LAKE = "data_lake_infracoes.jsonl"

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    """Calcula a distância aproximada em km entre dois pontos geográficos."""
    raio_terra = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return raio_terra * c

def verificar_zona_risco(lat, lon):
    """Verifica se o veículo está dentro do raio de alguma zona cadastrada."""
    for zona in ZONAS_DE_RISCO:
        distancia = calcular_distancia_km(lat, lon, zona["lat"], zona["lon"])
        if distancia <= zona["raio_km"]:
            return zona
    return None

def registrar_infracao_no_datalake(registro):
    """Grava o evento de infração no Data Lake (arquivo local simulado)."""
    with open(ARQUIVO_DATA_LAKE, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

# 2. Inicialização do Consumer
consumer = KafkaConsumer(
    'gps-tracking',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',          # Lê a partir das mensagens mais novas
    group_id='monitoramento-velocidade', # Identificador do grupo de consumidores
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("👂 Consumidor ativo e escutando o tópico 'gps-tracking'...")
print(f"📁 Infrações serão gravadas em: {ARQUIVO_DATA_LAKE}\n")

try:
    for mensagem in consumer:
        dado = mensagem.value
        driver_id = dado["driver_id"]
        velocidade = dado["speed_kmh"]
        lat = dado["latitude"]
        lon = dado["longitude"]

        zona = verificar_zona_risco(lat, lon)
        em_zona_risco = zona is not None

        # Definição do limite conforme a zona
        limite = 40 if em_zona_risco else 60

        if velocidade > limite:
            motivo = f"Zona de risco ({zona['nome']})" if em_zona_risco else "Via comum"
            print(f"🚨 [ALERTA] Motorista {driver_id} a {velocidade} km/h! (Limite: {limite} km/h - {motivo})")

            # Estrutura do dado para o Data Lake
            infracao = {
                "timestamp": dado["timestamp"],
                "driver_id": driver_id,
                "velocidade_registrada": velocidade,
                "limite_permitido": limite,
                "tipo_local": motivo,
                "latitude": lat,
                "longitude": lon
            }
            registrar_infracao_no_datalake(infracao)
        else:
            print(f"✅ Motorista {driver_id} dentro do limite ({velocidade} km/h)")

except KeyboardInterrupt:
    print("\nEncerrando o consumidor...")
finally:
    consumer.close()