# 🌡️ Sistema de Monitoramento de Temperatura e Umidade

Sistema IoT completo para coleta, armazenamento e visualização de dados de temperatura e umidade utilizando ESP32, MQTT e Flask.

## 📊 Arquitetura do Sistema

- **ESP32 + DHT11** → Coleta dados dos sensores
- **HiveMQ Cloud** → Broker MQTT (SSL/TLS)
- **JS_subscriber** → Cliente MQTT + Banco SQLite
- **Flask App** → Dashboard web interativo

## 🏗️ Estrutura do Projeto

```bash
Monitoramento_Temperatura_Umidade/
├── Flask/                 # Aplicação web Flask
│   ├── app.py            # Servidor principal
│   ├── templates/        # Templates HTML
│   └── static/           # CSS e assets
├── JS_subscriber/        # Cliente MQTT Node.js
│   ├── index.js         # Subscriber principal
│   └── config.js        # Configurações MQTT
├── database/            # Banco SQLite (criado automaticamente)
└── logs/               # Logs do sistema
```

## ⚡ Início Rápido

### 🔧 1. Configurar Cliente MQTT

```bash
cd JS_subscriber
npm install
node index.js
```

### 🌐 2. Iniciar Dashboard Flask

```bash
cd Flask
pip install -r requirements.txt
python app.py
```

### 📱 3. Acessar Dashboard

```bash
Abra no navegador:  **http://localhost:5000**
```

## 🛠️ Pré-requisitos

- **Node.js 18+** para o cliente MQTT
- **Python 3.8+** para a aplicação Flask
- **ESP32 + DHT11** para coleta de dados (repositório separado)

## 📡 Configuração MQTT

O sistema utiliza **HiveMQ Cloud** com conexão SSL:

- **Host:** `********`

- **Porta:** `8883` (SSL)
- **Tópico:** `******`

## 📊 Recursos do Dashboard

- **Gráficos Interativos** com dois eixos Y
- **Filtros por Data** personalizáveis
- **Exportação CSV** dos dados
- **Autenticação** de usuários

## 🗄️ Banco de Dados

- **SQLite** compartilhado entre módulos
- **Localização:** `database/monitor.db`
- **Criação automática** de tabelas e diretórios

## 📖 Documentação Detalhada

- **Flask:** [Flask/README.md](Flask/README.md)
- **JS_subscriber:** [JS_subscriber/README.md](JS_subscriber/README.md)

### 👥 Equipe

Ana Carolina Gomes • Diego Ribeiro Porto • Gabriel Neri e Costa • João Ribeiro Aiub • Luana Estevam Bruno Carvalho
