// Configurações do MQTT
export const mqttConfig = {
    // Configurações básicas do broker MQTT
    host: 'your-mqtt-broker.com',           // Endereço do seu broker MQTT
    port: 8883,                             // Porta SSL para MQTT (1883 para não-SSL, 8883 para SSL)
    protocol: 'mqtts',                      // Protocolo (mqtt, mqtts, ws, wss)
    
    // Configurações de conexão
    clientId: 'js_subscriber_' + Math.random().toString(16).substr(2, 8), // ID único do cliente
    clean: true,                            // Sessão limpa
    connectTimeout: 4000,                   // Timeout de conexão em ms
    reconnectPeriod: 1000,                  // Período de reconexão em ms
    
    // Credenciais do broker MQTT (configure com seus valores)
    username: 'your_mqtt_username',
    password: 'your_mqtt_password',
    
    // Configurações SSL/TLS
    rejectUnauthorized: true                // Verificar certificados SSL (recomendado para produção)
    
    // Para certificados customizados (descomente se necessário):
    // ca: fs.readFileSync('path/to/ca.crt'),
    // cert: fs.readFileSync('path/to/client.crt'),
    // key: fs.readFileSync('path/to/client.key'),
};

// Configurações do banco de dados SQLite
export const dbConfig = {
    // Caminho para o arquivo do banco de dados
    dbPath: '../database/monitor.db',       // Mesmo banco usado pelo Flask
    
    // Configurações adicionais do SQLite
    options: {
        // Configurações do driver sqlite3
        verbose: false,                     // Log detalhado das queries (true para debug)
        cached: true,                       // Cache de statements
        
        // Configurações de performance
        busyTimeout: 30000,                 // Timeout para operações em ms
        
        // Configurações de journal
        journalMode: 'WAL',                 // Write-Ahead Logging para melhor performance
        synchronous: 'NORMAL'               // Nível de sincronização
    }
};

// Configurações dos tópicos MQTT
export const topicConfig = {
    // Tópicos para subscrição
    subscribe: [
        'sensor/humidity_temperature',      // Tópico principal de dados
        // 'sensor/pressure',               // Adicione outros sensores conforme necessário
        // 'sensor/light'
    ],
    
    // Tópicos para publicação (se necessário)
    publish: {
        status: 'client/status',            // Status do cliente
        heartbeat: 'client/heartbeat'       // Heartbeat do cliente
    }
};

// Configurações de logging
export const logConfig = {
    // Nível de log (error, warn, info, debug)
    level: 'info',
    
    // Log para arquivo
    logToFile: false,                       // Habilitar log em arquivo
    logFilePath: '../logs/mqtt_subscriber.log',
    
    // Log para console
    logToConsole: true,                     // Log no console
    
    // Formato de timestamp
    timestampFormat: 'YYYY-MM-DD HH:mm:ss'
};

// Configurações da aplicação
export const appConfig = {
    // Nome da aplicação
    name: 'Temperature & Humidity Monitor',
    version: '1.0.0',
    
    // Intervalo para operações periódicas (em ms)
    heartbeatInterval: 30000,               // 30 segundos
    
    // Configurações de retry
    maxRetries: 3,                          // Máximo de tentativas
    retryDelay: 5000,                       // 5 segundos entre tentativas
    
    // Configurações de validação de dados
    validation: {
        temperature: {
            min: -50,                       // Temperatura mínima válida (°C)
            max: 100                        // Temperatura máxima válida (°C)
        },
        humidity: {
            min: 0,                         // Umidade mínima válida (%)
            max: 100                        // Umidade máxima válida (%)
        }
    }
};

// Exportação de todas as configurações como um objeto único (opcional)
export default {
    mqtt: mqttConfig,
    database: dbConfig,
    topics: topicConfig,
    logging: logConfig,
    app: appConfig
};