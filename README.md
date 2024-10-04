# Projeto de Monitoramento de Temperatura e Umidade

Este projeto consiste em um sistema de monitoramento de temperatura e umidade utilizando uma placa ESP32 para coleta e transmissão de dados para um Broker, um serviço de assintatura do Broker MQTT para receber e armazenar dados, escrito em JavaScript e um servidor Flask para visualização dos dados em um dashboard.

## Estrutura do Projeto

Flask/ app.py static/ dashboard.css styles.css templates/ dashboard.html index.html

JS_subscriber/ index.js package.json

README.md

## Configuração do Firmware (ESP32)

A placa ESP32 é responsável por coletar os dados de temperatura e umidade utilizando um sensor DHT11 e enviar esses dados para um broker MQTT na HiveMQ Cloud, este projeto está em outro repositório.

### Dependências

#### Configuração do Subscriber (Node.js)

O subscriber em Node.js é responsável por receber os dados do broker MQTT e armazená-los no banco de dados SQLite.

Dependências
Instale as dependências do subscriber listadas no arquivo package.json:

```npm install```

Executando o Subscriber
Para iniciar o subscriber, execute o seguinte comando:

```node JS_subscriber/index.js```

#### Configuração do Banco de Dados

O banco de dados SQLite é configurado no arquivo ```/index.js```:

Na chamada da função:

```setupDatabase()```

#### Configuração do Servidor Flask

O servidor Flask é responsável por ler os dados armazenados no banco de dados e gerar páginas com demonstração gráfica dos dados.

Dependências
Instale as dependências do servidor Flask listadas no arquivo requirements.txt:

```pip install -r requirements.txt```

Executando o Servidor
Para iniciar o servidor Flask, execute o seguinte comando:

```python Flask/app.py```

Acesse o dashboard no navegador pelo link gerado no Flask.

#### Observações

Certifique-se de que a placa ESP32 esteja transmitindo os dados corretamente.
O broker MQTT utilizado é o HiveMQ Cloud.
Licença
Este projeto está licenciado sob a MIT License.
