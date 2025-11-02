# 🌡️ Módulo Flask - Dashboard de Monitoramento

Este módulo contém a aplicação web Flask para visualização e gerenciamento dos dados de temperatura e umidade coletados pelo sistema de monitoramento.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Uso da Aplicação](#-uso-da-aplicação)
- [API Endpoints](#-api-endpoints)
- [Personalização](#-personalização)
- [Solução de Problemas](#-solução-de-problemas)

## 🚀 Funcionalidades

### 🔐 **Sistema de Autenticação**

- Login e registro de usuários
- Autenticação com Flask-Login
- Senhas criptografadas com Werkzeug
- Sessões temporárias (não persistentes)

### 📊 **Dashboard Interativo**

- Gráficos de temperatura e umidade em tempo real
- **Dois eixos Y independentes:**
  - Eixo esquerdo (vermelho): Temperatura em °C
  - Eixo direito (azul): Umidade em % (0-100%)
- Filtros por data personalizáveis
- Visualização dos últimos 7 dias por padrão
- Hover interativo com informações detalhadas

### 📈 **Análise de Dados**

- Histórico completo de medições
- Gráficos responsivos com Plotly.js
- Interface escura otimizada para visualização
- Exportação de dados em formato CSV

### 📱 **Interface Responsiva**

- Design moderno e intuitivo
- Compatível com dispositivos móveis
- Tema escuro para melhor experiência visual

## 📁 Estrutura do Projeto

```python
Flask/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── .python-version       # Versão do Python (pyenv)
├── static/               # Arquivos estáticos
│   ├── styles.css        # Estilos gerais
│   └── dashboard.css     # Estilos específicos do dashboard
└── templates/            # Templates HTML
    ├── base.html         # Template base
    ├── login.html        # Página de login
    ├── register.html     # Página de registro
    ├── index.html        # Página inicial
    └── dashboard.html    # Dashboard principal
```

## 🔧 Pré-requisitos

### **Software Necessário:**

- Python 3.12+ (recomendado 3.12+)
- pip (gerenciador de pacotes Python)

### **Dependências Python:**

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- WTForms
- Werkzeug
- Plotly
- sqlite3 (nativo do Python)

## 📥 Instalação

### **1. Navegue até o diretório Flask:**

```bash
cd E:\projetos\Monitoramento_Temperatura_Umidade\Flask
```

### **2. (Opcional) Configure ambiente virtual:**

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### **3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### **Configurações Automáticas:**

A aplicação configura automaticamente:

- **Banco de dados:** `../database/monitor.db` (SQLite)
- **Logs:** `../logs/app.log`
- **Chave secreta:** "UNISENAI" (alterar em produção)

### **Configurações Manuais (Opcionais):**

#### **1. Alterar porta do servidor:**

```python
# No final do app.py
host = '127.0.0.1'
port = 8080  # Alterar porta aqui
```

#### **2. Configurar chave secreta personalizada:**

```python
app.config["SECRET_KEY"] = "sua_chave_secreta_aqui"
```

#### **3. Configurar host externo:**

```python
# Para acessar de outros dispositivos na rede
host = '0.0.0.0'  # Permitir acesso externo
```

## 🏃‍♂️ Execução

### **Executar a aplicação:**

```bash
python app.py
```

### **Saída esperada no terminal:**

```bash
============================================================
🌐 SERVIDOR FLASK INICIADO COM SUCESSO!
============================================================
📍 URL de Acesso: http://127.0.0.1:5000
🔗 Link direto: http://localhost:5000
📊 Dashboard: http://localhost:5000/dashboard
🔑 Login: http://localhost:5000/login
📝 Registro: http://localhost:5000/register
============================================================
⚠️  Para parar o servidor: Ctrl+C
============================================================
```

## 💻 Uso da Aplicação

### **1. Primeiro Acesso:**

1. Acesse: `http://localhost:5000`
2. Clique em "Registrar" para criar uma conta
3. Preencha: usuário, email e senha
4. Faça login com suas credenciais

### **2. Navegação:**

- **🏠 Página Inicial:** Tela de boas-vindas
- **📊 Dashboard:** Visualização dos gráficos
- **📤 Exportar:** Download dos dados em CSV
- **🚪 Logout:** Sair da sessão

### **3. Dashboard:**

- **Gráfico Principal:** Mostra temperatura (°C) e umidade (%)
- **Filtros de Data:** Use os parâmetros URL:

  ```bash
  http://localhost:5000/dashboard?start_date=2024-01-01&end_date=2024-01-31
  ```

- **Exportar CSV:** Botão para download dos dados

## 🌐 API Endpoints

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/` | Página inicial | ✅ Requerida |
| GET/POST | `/login` | Login de usuário | ❌ Pública |
| GET/POST | `/register` | Registro de usuário | ❌ Pública |
| POST | `/logout` | Logout de usuário | ✅ Requerida |
| GET | `/dashboard` | Dashboard principal | ✅ Requerida |
| GET | `/export_csv` | Exportar dados CSV | ✅ Requerida |
| GET | `/force_logout` | Logout forçado | ❌ Pública |

### **Parâmetros do Dashboard:**

- `start_date`: Data inicial (formato: YYYY-MM-DD)
- `end_date`: Data final (formato: YYYY-MM-DD)

## 🗄️ Banco de Dados

### **Modelos de Dados:**

#### **Tabela: users**

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);
```

#### **Tabela: dados_sensor**

```sql
CREATE TABLE dados_sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura FLOAT NOT NULL,
    umidade FLOAT NOT NULL,
    timestamp DATETIME NOT NULL
);
```

### **Localização do Banco:**

- **Arquivo:** `../database/monitor.db`
- **Tipo:** SQLite
- **Criação:** Automática na primeira execução

## 🎨 Personalização

### **1. Alterar Cores do Gráfico:**

```python
# Em app.py, na função dashboard()
line=dict(color="#FF6347")  # Temperatura (vermelho)
line=dict(color="#4682B4")  # Umidade (azul)
```

### **2. Modificar Tema:**

```python
# Alterar cores de fundo
plot_bgcolor="#2f2f2f"   # Fundo do gráfico
paper_bgcolor="#2f2f2f"  # Fundo do papel
```

### **3. Personalizar CSS:**

- **Arquivo:** `static/styles.css` (estilos gerais)
- **Arquivo:** `static/dashboard.css` (estilos específicos)

### **4. Alterar Templates:**

- **Base:** `templates/base.html`
- **Dashboard:** `templates/dashboard.html`

## 🔧 Solução de Problemas

### **❌ Erro: "No such table: dados_sensor"**

**Solução:** Execute o JS_subscriber primeiro para criar a tabela, ou execute:

```python
from app import app, db
with app.app_context():
    db.create_all()
```

### **❌ Erro: "Permission denied" no banco**

**Solução:** Verifique permissões da pasta `database/`:

```bash
# Windows
icacls database /grant Users:F

# Linux/Mac
chmod 755 database/
```

### **❌ Erro: "Port already in use"**

**Solução:** Altere a porta no `app.py`:

```python
port = 8080  # ou outra porta disponível
```

### **❌ Gráfico não carrega**

**Soluções:**

1. Verifique se há dados na tabela `dados_sensor`
2. Confirme conexão com o banco de dados
3. Verifique console do navegador para erros JavaScript

### **❌ Erro de importação de módulos**

**Solução:** Reinstale as dependências:

```bash
pip install -r requirements.txt --force-reinstall
```

**Desenvolvido para o Sistema de Monitoramento de Temperatura e Umidade** 🌡️💧
