```markdown
# 🛰️ Pipeline de Telemetria e Streaming com Apache Kafka

Pipeline de dados em tempo real desenvolvido em Python e Apache Kafka para ingestão de telemetria veicular (GPS), aplicação de regras de negócio em trânsito (detecção de excesso de velocidade) e persistência de dados em formato JSON Lines (*Data Lake*).

---

## 📌 Visão Geral da Arquitetura

O sistema implementa o padrão produtor-consumidor baseado em eventos:

* 🚗 **Produtor (`fonte/produtor.py`):** Simula múltiplos veículos enviando coordenadas GPS, identificadores (`driver_id`) e velocidade instantânea para o tópico `gps-tracking`.
* 📬 **Broker (`Apache Kafka via Docker`):** Gerencia a fila de mensagens distribuída, retenção e particionamento do tópico.
* ⚙️ **Consumidor (`fonte/consumidor.py`):** Processa o stream em tempo real, aplica geofencing simples e limites de velocidade dinâmicos (vias comuns vs. zonas de risco como hospitais e escolas) e emite alertas no terminal.
* 💾 **Armazenamento (`dados/data_lake_infracoes.jsonl`):** Persiste apenas os eventos classificados como infração diretamente em disco em formato `.jsonl`.

---

## 📂 Estrutura do Diretório

```text
projeto-kafka-streaming/
├── dados/
│   └── data_lake_infracoes.jsonl    # Eventos de infrações persistidos
├── fonte/
│   ├── consumidor.py                # Processamento de regras e alertas
│   └── produtor.py                  # Gerador de eventos de telemetria GPS
├── docker-compose.yml               # Orquestração do cluster Kafka / Zookeeper
├── requirements.txt                 # Dependências Python do projeto
└── README.md

```

---

## ⚙️ Pré-requisitos

* [Docker](https://www.docker.com/) e Docker Compose instalados.
* [Python 3.10+](https://www.python.org/) configurado.

---

## 🚀 Como Executar

### 1. Inicializar a Infraestrutura Kafka

Suba os contêineres do Zookeeper e Kafka em segundo plano:

```bash
docker compose up -d

```

Verifique se os serviços estão saudáveis:

```bash
docker compose ps

```

---

### 2. Configurar o Ambiente Virtual Python

Crie e ative o ambiente virtual para isolar as bibliotecas:

* **Windows:**
```bash
python -m venv kafka_env
.\kafka_env\Scripts\activate

```


* **Linux / macOS:**
```bash
python3 -m venv kafka_env
source kafka_env/bin/activate

```



Instale as dependências listadas no `requirements.txt`:

```bash
pip install -r requirements.txt

```

> ⚠️ **Nota sobre dependências:** Este projeto utiliza a biblioteca `kafka-python-ng` para garantir compatibilidade com versões recentes do Python (3.12+ no Windows), substituindo a versão legada e evitando falhas de descritor de arquivo (`selectors`).

---

### 3. Iniciar o Consumidor (Processamento de Regras)

Em um terminal com o ambiente virtual ativado:

```bash
python fonte/consumidor.py

```

O consumidor ficará ativo aguardando novas mensagens no tópico `gps-tracking`.

---

### 4. Iniciar o Produtor (Transmissão de Telemetria)

Abra um segundo terminal, ative o ambiente virtual e inicie a transmissão:

```bash
python fonte/produtor.py

```

Os eventos de telemetria serão transmitidos a cada 2 segundos.

---

## 🔍 Inspeção dos Dados Persistidos

As infrações filtradas são salvas automaticamente na pasta `dados/`. Para inspecionar os registros salvos:

* **Windows (CMD):**
```cmd
type dados\data_lake_infracoes.jsonl

```


* **Linux / macOS / PowerShell:**
```bash
cat dados/data_lake_infracoes.jsonl

```



Exemplo de registro gravado no Data Lake:

```json
{
  "timestamp": "2026-09-02T01:07:08.969841",
  "driver_id": "driver_02",
  "velocidade_registrada": 69,
  "limite_permitido": 40,
  "tipo_local": "Zona de risco (Hospital das Clínicas)",
  "latitude": -23.554104,
  "longitude": -46.650596
}

```

---

## 🛑 Gerenciamento da Infraestrutura

Para pausar os scripts Python nos terminais, utilize o atalho **`Ctrl + C`**.

Para gerenciar os contêineres Docker:

| Ação | Comando | Descrição |
| --- | --- | --- |
| **Pausar** | `docker compose stop` | Congela a execução sem remover redes ou contêineres. |
| **Encerrar** | `docker compose down` | Desliga e remove os contêineres e redes criadas. |
| **Reset Total** | `docker compose down -v` | Remove os contêineres, redes e volumes (apaga dados persistidos no Kafka). |

