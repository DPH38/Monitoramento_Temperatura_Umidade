# ⚙️ Configuração do JS_subscriber

## 🔧 Setup Inicial

1. **Copie o arquivo de exemplo:**

   ```bash
   cp config.js.example config.js
   ```

2. **Configure seus valores no `config.js`:**
   - **Host MQTT:** Substitua `your-mqtt-broker.com`
   - **Porta:** Ajuste se necessário (1883 para não-SSL, 8883 para SSL)
   - **Credenciais:** Configure `username` e `password`
   - **Protocolo:** `mqtt` ou `mqtts` (SSL)

## 📝 Exemplo de Configuração

### Para HiveMQ Cloud

```javascript
host: 'your-cluster.hivemq.cloud',
port: 8883,
protocol: 'mqtts',
username: 'your_username',
password: 'your_password'
```

### Para Broker Local

```javascript
host: 'localhost',
port: 1883,
protocol: 'mqtt'
// Remover username/password se não necessário
```

## 🛡️ Segurança

- ⚠️ **NUNCA** commite o arquivo `config.js` real
- ✅ O `.gitignore` já está configurado para ignorá-lo
- 🔒 Mantenha credenciais seguras e privadas

## 🚀 Executar

Após configurar:

```bash
npm install
node index.js
```
