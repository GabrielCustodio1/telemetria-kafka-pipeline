```markdown
# 🚗 Pipeline de Telemetria e Detecção de Infrações de Trânsito

Pipeline de dados ponta a ponta que simula, ingere e processa eventos de telemetria veicular em tempo real utilizando Apache Kafka, arquitetura em camadas (Bronze, Prata e Ouro) com Pandas e geração de visualizações analíticas com Matplotlib.

---

## 📂 Estrutura do Projeto

```text
.
├── docker-compose.yml       # Orquestração do Kafka e Zookeeper
├── requirements.txt         # Dependências do projeto
├── .gitignore               # Arquivos e diretórios ignorados pelo Git
├── README.md                # Documentação técnica do projeto
├── dados/                   # Camadas de dados (Bronze, Prata e Ouro)
│   ├── data_lake_infracoes.jsonl
│   └── relatorio_infracoes.csv
├── imagens/                 # Gráficos analíticos gerados
│   ├── grafico_infracoes.png
│   ├── grafico_local.png
│   └── grafico_media_excesso.png
└── fonte/                   # Código-fonte da aplicação
    ├── produtor.py
    ├── consumidor.py
    ├── analise.py
    └── visualizacao.py

```

---

## 🏗️ Arquitetura da Solução

O pipeline adota o padrão de arquitetura medalhão para fluxo de streaming e processamento analítico em lote:

* 📡 **Produtor (`fonte/produtor.py`):** Simula o envio contínuo de eventos de telemetria veicular (identificador do condutor, velocidade e zona de tráfego) para um tópico do Apache Kafka.
* 🛑 **Consumidor (`fonte/consumidor.py`):** Consome eventos em tempo real, aplica regras de negócio (limites de velocidade e zonas monitoradas) e persiste as violações detectadas no formato JSONL em `dados/data_lake_infracoes.jsonl` (**Camada Bronze**).
* ⚙️ **Processamento e Análise (`fonte/analise.py`):** Realiza limpeza de dados, tratamento de valores ausentes, cálculo da métrica de severidade (`excesso_kmh`) (**Camada Prata**) e consolida as métricas agregadas em `dados/relatorio_infracoes.csv` (**Camada Ouro**).
* 📊 **Visualização (`fonte/visualizacao.py`):** Consome os dados refinados e gera gráficos analíticos de volumetria, concentração geográfica e severidade, salvando os resultados em `imagens/`.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

* Python 3.10+
* Docker e Docker Compose instalados

---

### 1. Preparar o Ambiente Python

Crie e ative seu ambiente virtual (via Conda ou venv) e instale as dependências:

```bash
pip install -r requirements.txt

```

### 2. Iniciar a Infraestrutura (Kafka + Zookeeper)

Na raiz do projeto, suba os serviços em segundo plano:

```bash
docker compose up -d

```

Verifique se os contêineres estão em execução:

```bash
docker compose ps

```

### 3. Executar o Pipeline de Streaming

Abra dois terminais com o ambiente virtual ativo:

* **Terminal 1 (Consumidor):** Inicie o consumidor para aguardar e processar os eventos:
```bash
python fonte/consumidor.py

```


* **Terminal 2 (Produtor):** Dispare a simulação de telemetria:
```bash
python fonte/produtor.py

```



### 4. Processamento Analítico e Visualização

Após coletar as mensagens desejadas, execute a transformação dos dados e a geração dos gráficos:

```bash
# Limpeza, enriquecimento e agregação (Camadas Prata e Ouro)
python fonte/analise.py

# Geração dos gráficos analíticos na pasta imagens/
python fonte/visualizacao.py

```

---

## 📊 Resultados e Visualizações

Abaixo estão os artefatos visuais gerados pela camada analítica para suporte à tomada de decisão:

### 1. Volumetria de Infrações por Motorista

Mapeia a reincidência de infrações por condutor:

> **Insight:** Permite inferir qual dos motoristas possui a maior quantidade de infrações registradas.

---

### 2. Distribuição Espacial de Infrações

Analisa a concentração de ocorrências por tipo de via:

> **Insight:** Permite inferir quais localizações tiveram maior número de violações para direcionamento de fiscalização e sinalização preventiva.

---

### 3. Severidade Média de Excesso de Velocidade

Mede a gravidade das infrações ao calcular a média em km/h acima do limite permitido:

> **Insight:** Permite inferir a média de velocidade excedida por cada motorista, separando pequenas infrações de condutas de risco severo.

```
