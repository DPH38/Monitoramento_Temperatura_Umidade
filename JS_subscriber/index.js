import { connect } from 'mqtt';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';
import { fileURLToPath } from 'url';
import { mqttConfig, dbConfig } from './config.js'; // Importar as configurações

// Obter o diretório atual
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Inicializar o cliente MQTT
var client = connect(mqttConfig);

// Configurar a conexão SQLite
async function setupDatabase() {
    const dbPath = path.resolve(__dirname, dbConfig.dbPath); // Usar o caminho do arquivo de configuração
    const db = await open({
        filename: dbPath,
        driver: sqlite3.Database
    });

    await db.exec(`
        CREATE TABLE IF NOT EXISTS dados_sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura FLOAT NOT NULL,
            umidade FLOAT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    `);

    return db;
}

let db;
setupDatabase().then(database => {
    db = database;
});

// Configurar os callbacks
client.on('connect', function () {
    console.log('Connected');
});

client.on('error', function (error) {
    console.log(error);
});

client.on('message', async function (topic, message) {
    // Chamada cada vez que uma mensagem é recebida
    if (topic === 'sensor/humidity_temperature') {
        const messageStr = message.toString();
        console.log('Received message:', topic, messageStr);
        const regex = /Timestamp:\s([\d-]+\s[\d:]+),\sHumidity:\s([\d.]+)\s% Temperature:\s([\d.]+)\s\*C/;
        const match = messageStr.match(regex);
        
        if (match) {
            const timestamp = match[1];
            const humidity = parseFloat(match[2]);
            const temperature = parseFloat(match[3]);

            console.log(`Timestamp: ${timestamp}, Humidity: ${humidity} %, Temperature: ${temperature} *C`);

            // Log dos dados a serem armazenados
            console.log(`Dados a serem armazenados - Timestamp: ${timestamp}, Umidade: ${humidity}, Temperatura: ${temperature}`);

            // Inserir os dados no banco de dados
            await db.run(`
                INSERT INTO dados_sensor (temperatura, umidade, timestamp)
                VALUES (?, ?, ?)
            `, [temperature, humidity, timestamp]);
        } else {
            console.log('Message format is incorrect:', messageStr);
        }
    } else {
        console.log('Received message:', topic, message.toString());
    }
});

// Inscrever-se no tópico 'sensor/humidity_temperature'
client.subscribe('sensor/humidity_temperature');