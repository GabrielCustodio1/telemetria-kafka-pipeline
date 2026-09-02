import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# 1. Configuração de conexão com o broker local
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    # Serializa os dados em formato JSON codificado em UTF-8
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPICO = 'gps-tracking'
MOTORISTAS = ['driver_01', 'driver_02', 'driver_03']

print(f"Iniciando transmissão para o tópico '{TOPICO}'... Pressione Ctrl+C para parar.\n")

try:
    while True:
        # 2. Simulação de coordenadas (ex: região central de São Paulo)
        evento = {
            "driver_id": random.choice(MOTORISTAS),
            "timestamp": datetime.now().isoformat(),
            "latitude": round(random.uniform(-23.560, -23.540), 6),
            "longitude": round(random.uniform(-46.660, -46.630), 6),
            "speed_kmh": random.randint(0, 80)
        }

        # 3. Envio da mensagem para a fila
        producer.send(TOPICO, value=evento)
        print(f"🛰️ Mensagem enviada: {evento}")

        # Intervalo de 2 segundos entre envios
        time.sleep(2)

except KeyboardInterrupt:
    print("\nEncerrando o envio de mensagens...")
finally:
    producer.flush()
    producer.close()