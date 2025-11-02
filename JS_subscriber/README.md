# 📡 Módulo JS_subscriber - Cliente MQTT

Este módulo contém o cliente JavaScript/Node.js responsável por receber dados MQTT dos sensores IoT e armazenar no banco de dados SQLite compartilhado com a aplicação Flask.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Monitoramento](#-monitoramento)
- [Formato das Mensagens](#-formato-das-mensagens)
- [Solução de Problemas](#-solução-de-problemas)

## 🚀 Funcionalidades

### 📡 **Cliente MQTT**

- Conexão segura com HiveMQ Cloud (SSL/TLS)
- Reconexão automática em caso de falha
- Autenticação com usuário e senha
- Subscrição automática aos tópicos configurados

### 🗄️ **Gerenciamento de Dados**

- Parsing inteligente de mensagens MQTT
- Validação de formato de dados
- Inserção automática no banco SQLite
- Compartilhamento de dados com aplicação Flask

### 🔄 **Processamento em Tempo Real**

- Processamento contínuo de mensagens
- Log detalhado de operações
- Tratamento de erros robusto
- Validação de dados de entrada

### ⚙️ **Configuração Flexível**

- Arquivo de configuração centralizado
- Parâmetros de conexão MQTT customizáveis
- Configurações de banco de dados
- Opções de logging e monitoramento

## 📁 Estrutura do Projeto

```bash
JS_subscriber/
├── index.js          # Aplicação principal Node.js
├── config.js         # Configurações centralizadas
├── package.json      # Dependências e scripts npm
└── README.md         # Este arquivo
```

## 🔧 Pré-requisitos

### **Software Necessário:**

- Node.js 18+ (recomendado LTS)
- npm (gerenciador de pacotes Node.js)

### **Dependências Node.js:**

- `mqtt` v5.10.1+ - Cliente MQTT
- `sqlite3` v5.1.7+ - Driver SQLite
- `sqlite` v5.1.1+ - Wrapper para SQLite3

### **Serviços Externos:**

- Broker MQTT (HiveMQ Cloud configurado)
- Sensores IoT publicando no tópico correto

## 📥 Instalação

### **1. Navegue até o diretório JS_subscriber:**

```bash
cd E:\projetos\Monitoramento_Temperatura_Umidade\JS_subscriber
```

### **2. Instale as dependências:**

```bash
npm install
```

### **3. Verifique a instalação:**

```bash
npm list
```

**Saída esperada:**

```bash
ja_js@1.0.0
├── mqtt@5.10.1
├── sqlite@5.1.1
└── sqlite3@5.1.7
```

## ⚙️ Configuração

### **Arquivo de Configuração: `config.js`**

#### **🌐 Configurações MQTT (HiveMQ Cloud):**

```javascript
export const mqttConfig = {
    host: '7628536e54254fbb9ae92812b9927542.s1.eu.hivemq.cloud',
    port: 8883,                    // Porta SSL
    protocol: 'mqtts',             // SSL/TLS
    username: 'iot_cloud',
    password: 'iOT123456@#',
    rejectUnauthorized: true       // Verificação SSL
};
```

#### **🗄️ Configurações do Banco:**

```javascript
export const dbConfig = {
    dbPath: '../database/monitor.db',  // Compartilhado com Flask
    options: {
        verbose: false,
        cached: true,
        busyTimeout: 30000,
        journalMode: 'WAL',
        synchronous: 'NORMAL'
    }
};
```

#### **📡 Configurações de Tópicos:**

```javascript
export const topicConfig = {
    subscribe: [
        'sensor/humidity_temperature'  // Tópico principal
    ]
};
```

### **Personalização das Configurações:**

#### **1. Alterar Broker MQTT:**

```javascript
// Para broker local
host: 'localhost',
port: 1883,
protocol: 'mqtt',
// Remover username/password se não necessário
```

#### **2. Configurar Tópicos Adicionais:**

```javascript
subscribe: [
    'sensor/humidity_temperature',
    'sensor/pressure',
    'sensor/light'
]
```

#### **3. Ajustar Configurações do Banco:**

```javascript
dbPath: './local_database.db',  // Banco local
options: {
    verbose: true,  // Log detalhado das queries
    busyTimeout: 60000  // Timeout maior
}
```

## 🏃‍♂️ Execução

### **Executar o subscriber:**

```bash
node index.js
```

### **Saída esperada no terminal:**

```bash
Diretório criado: E:\projetos\Monitoramento_Temperatura_Umidade\database
Connected
Received message: sensor/humidity_temperature Timestamp: 2024-11-02 14:30:15, Humidity: 65.2 % Temperature: 23.4 *C
Timestamp: 2024-11-02 14:30:15, Humidity: 65.2 %, Temperature: 23.4 *C
Dados a serem armazenados - Timestamp: 2024-11-02 14:30:15, Umidade: 65.2, Temperatura: 23.4
```

### **Executar em Background (Windows):**

```bash
# Usando start
start /B node index.js

# Ou usando nohup (Git Bash)
nohup node index.js &
```

### **Executar como Serviço:**

```bash
# Instalar PM2 globalmente
npm install -g pm2

# Iniciar com PM2
pm2 start index.js --name "mqtt-subscriber"

# Verificar status
pm2 status

# Ver logs
pm2 logs mqtt-subscriber
```

## 📊 Monitoramento

### **🔍 Logs de Operação:**

- **Conexão MQTT:** Status de conexão/desconexão
- **Mensagens Recebidas:** Todas as mensagens MQTT
- **Dados Processados:** Valores extraídos e validados
- **Inserções no Banco:** Confirmação de armazenamento
- **Erros:** Falhas de conexão ou processamento

### **📈 Métricas Importantes:**

- Taxa de mensagens por minuto
- Tempo de resposta do banco de dados
- Status da conexão MQTT
- Qualidade dos dados recebidos

### **🔧 Comandos de Debug:**

```bash
# Ver logs em tempo real
tail -f ../logs/app.log

# Verificar conexão MQTT
netstat -an | findstr 8883

# Verificar banco de dados
sqlite3 ../database/monitor.db "SELECT COUNT(*) FROM dados_sensor;"
```

## 📨 Formato das Mensagens

### **Formato Esperado:**

```bash
Timestamp: YYYY-MM-DD HH:MM:SS, Humidity: XX.X % Temperature: XX.X *C
```

### **Exemplo Válido:**

```bash
Timestamp: 2024-11-02 14:30:15, Humidity: 65.2 % Temperature: 23.4 *C
```bash
Timestamp: 2024-11-02 14:30:15, Humidity: 65.2 % Temperature: 23.4 *C
```

### **Regex de Validação:**

```javascript
const regex = /Timestamp:\s([\d-]+\s[\d:]+),\sHumidity:\s([\d.]+)\s% Temperature:\s([\d.]+)\s\*C/;
```

### **Campos Extraídos:**

```javascript
const match = messageStr.match(regex);
if (match) {
    const timestamp = match[1];
    const humidity = parseFloat(match[2]);
    const temperature = parseFloat(match[3]);
}
- **Timestamp:** Data e hora da medição
- **Humidity:** Umidade relativa (%)  
- **Temperature:** Temperatura (°C)

### **Validação de Dados:**
```javascript
// Configuração padrão em config.js
validation: {
    temperature: { min: -50, max: 100 },
    humidity: { min: 0, max: 100 }
}
```

## 🗄️ Banco de Dados

### **Tabela: `dados_sensor`**

```sql
CREATE TABLE IF NOT EXISTS dados_sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura FLOAT NOT NULL,
    umidade FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### **Localização:**

- **Arquivo:** `../database/monitor.db`
- **Tipo:** SQLite3
- **Compartilhado:** Com aplicação Flask

### **Operações Automáticas:**

- Criação da tabela se não existir
- Inserção de dados validados
- Criação automática do diretório

### **Verificar Dados:**

```bash
sqlite3 ../database/monitor.db
```

```sql
-- Ver últimas 10 medições
SELECT * FROM dados_sensor ORDER BY timestamp DESC LIMIT 10;

-- Contar total de registros
SELECT COUNT(*) FROM dados_sensor;

-- Ver dados de hoje
SELECT * FROM dados_sensor WHERE DATE(timestamp) = DATE('now');
```

## ⚙️ Configurações Avançadas

### **🔄 Reconexão Automática:**

```javascript
mqttConfig: {
    reconnectPeriod: 1000,    // 1 segundo
    connectTimeout: 4000,     // 4 segundos
    clean: true               // Sessão limpa
}
```

### **🔒 Configurações SSL/TLS:**

```javascript
// Para certificados customizados
mqttConfig: {
    ca: fs.readFileSync('ca.crt'),
    cert: fs.readFileSync('client.crt'),
    key: fs.readFileSync('client.key'),
    rejectUnauthorized: false  // Apenas para desenvolvimento
}
```

### **📝 Configurações de Log:**

```javascript
logConfig: {
    level: 'debug',           // error, warn, info, debug
    logToFile: true,
    logFilePath: '../logs/mqtt.log',
    logToConsole: true
}
```

## 🔧 Solução de Problemas

### **❌ Erro: "Cannot find module 'config.js'"**

**Causa:** Arquivo config.js não existe
**Solução:**

```bash
# Verificar se existe
ls -la config.js

# Recriar se necessário
cp config.js.example config.js
```

### **❌ Erro: "SQLITE_CANTOPEN: unable to open database"**

**Causa:** Diretório database não existe
**Solução:** O código agora cria automaticamente, mas manualmente:

```bash
mkdir ../database
```

### **❌ Erro: "Connection refused" (MQTT)**

**Soluções:**

1. **Verificar conectividade:**

```bash
ping 7628536e54254fbb9ae92812b9927542.s1.eu.hivemq.cloud
```

 **Testar porta 8883:**

```bash
telnet 7628536e54254fbb9ae92812b9927542.s1.eu.hivemq.cloud 8883
```

**Verificar credenciais:**

```javascript
// Em config.js
username: '**********',
password: '**********'
```

### **❌ Erro: "Message format is incorrect"**

**Causa:** Formato da mensagem MQTT não reconhecido
**Diagnóstico:**

```javascript
// Adicionar log de debug em index.js
console.log('Raw message:', messageStr);
console.log('Regex match:', match);
```

### **❌ Alta CPU/Memória**

**Soluções:**

1. **Verificar loop infinito:**

```javascript
// Adicionar delay entre operações
await new Promise(resolve => setTimeout(resolve, 100));
```

**Otimizar banco:**

```javascript
dbConfig: {
    options: {
        journalMode: 'WAL',
        synchronous: 'NORMAL',
        cacheSize: -64000  // 64MB cache
    }
}
```

### **❌ Mensagens duplicadas**

**Solução:** Adicionar verificação de duplicatas:

```sql
-- Verificar duplicatas
SELECT timestamp, COUNT(*) 
FROM dados_sensor 
GROUP BY timestamp 
HAVING COUNT(*) > 1;
```

## 📊 Monitoramento de Performance

### **Scripts Úteis:**

#### **1. Verificar Performance:**

```bash
# Ver uso de CPU/Memória
tasklist | findstr node

# Monitorar conexões de rede
netstat -an | findstr 8883
```

#### **2. Backup do Banco:**

```bash
# Backup automático
sqlite3 ../database/monitor.db ".backup backup_$(date +%Y%m%d).db"
```

#### **3. Limpeza de Logs:**

```bash
# Limpar logs antigos (manter últimos 7 dias)
find ../logs -name "*.log" -mtime +7 -delete
```

## 🚀 Otimizações

### **Performance:**

- Use WAL mode para SQLite
- Configure cache adequado
- Implemente throttling se necessário

### **Confiabilidade:**

- Monitore conexão MQTT
- Implemente retry logic
- Configure alertas para falhas

### **Escalabilidade:**

- Consider usar clustering
- Implemente load balancing
- Use connection pooling

### **Logs Importantes:**

- Console output para status de conexão
- Mensagens MQTT recebidas
- Erros de parsing ou banco de dados
- Métricas de performance

**Desenvolvido para o Sistema de Monitoramento de Temperatura e Umidade** 📡🌡️💧
