from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
import plotly.io as pio
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    current_user,
    logout_user,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import logging
import os
from pathlib import Path
from io import StringIO
import csv
from flask import Response
from datetime import datetime, timedelta




app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = "UNISENAI"

# Ajuste do caminho do banco de dados para usar caminho relativo
BASE_DIR = Path(__file__).resolve().parent.parent  # Diretório raiz do projeto
DB_PATH = BASE_DIR / "database" / "monitor.db"

# Criar o diretório database se não existir
DB_PATH.parent.mkdir(exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
app.config["SESSION_PERMANENT"] = False  # Sessão não permanente

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Configuração de logging
LOG_PATH = BASE_DIR / "logs" / "app.log"
LOG_PATH.parent.mkdir(exist_ok=True)
log_file_path = str(LOG_PATH)
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


# Modelo de Usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    logger.info(f"Carregando usuário com ID: {user_id}")
    return User.query.get(int(user_id))


# Modelo de Dados do Sensor
class DadosSensor(db.Model):
    __tablename__ = 'dados_sensor'
    
    id = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float, nullable=False)
    umidade = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


# Formulários
class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    # remember = BooleanField("Remember Me")  # Removido para não lembrar a sessão


class RegisterForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5)])


# Rotas
@app.route("/login", methods=["GET", "POST"])
def login():
    logger.info("Acessando a rota de login")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # Removido remember=form.remember.data
            logger.info(f"Usuário {user.username} logado com sucesso")
            return redirect(url_for("index"))
        logger.warning("Tentativa de login falhou")
        flash("Senha ou Usuário incorreto", "danger")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    logger.info("Acessando a rota de registro")
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if existing_user:
            flash("Usuário já existente. Por favor, redefina sua senha.", "danger")
            return redirect(url_for("login"))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        logger.info(f"Usuário {user.username} registrado com sucesso")
        flash("Registrado com sucesso!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logger.info(f"Usuário {current_user.username} deslogado")
    logout_user()
    return redirect(url_for("login"))


@app.route("/force_logout")
def force_logout():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    logger.info("Acessando a rota index")
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    logger.info("Acessando a rota dashboard")

    # Obter as datas de início e fim dos parâmetros da URL
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # Se as datas não forem fornecidas, definir o intervalo padrão para os últimos 7 dias
    if not start_date_str or not end_date_str:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
    else:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Ajustar o end_date para incluir o final do dia
    end_date = end_date + timedelta(days=1) - timedelta(seconds=1)

    # Filtrar os dados com base no intervalo de datas
    dados = DadosSensor.query.filter(DadosSensor.timestamp >= start_date, DadosSensor.timestamp <= end_date).order_by(DadosSensor.timestamp.asc()).all()
    timestamps = [d.timestamp.strftime("%Y-%m-%d %H:%M:%S") for d in dados]
    temperaturas = [d.temperatura for d in dados]
    umidades = [d.umidade for d in dados]

    fig = go.Figure()
    
    # Traço da Temperatura (eixo Y esquerdo)
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=temperaturas,
            mode="lines+markers",
            name="Temperatura (°C)",
            line=dict(color="#FF6347", width=3),
            marker=dict(size=6),
            hovertemplate="Data: %{x}<br>Temperatura: %{y}°C<extra></extra>",
            yaxis="y1"  # Usar o eixo Y esquerdo
        )
    )
    
    # Traço da Umidade (eixo Y direito)
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=umidades,
            mode="lines+markers",
            name="Umidade (%)",
            line=dict(color="#4682B4", width=3),
            marker=dict(size=6),
            hovertemplate="Data: %{x}<br>Umidade: %{y}%<extra></extra>",
            yaxis="y2"  # Usar o eixo Y direito
        )
    )
    fig.update_layout(
        title_text="TEMPERATURA E UMIDADE",
        title_x=0.5,
        xaxis_title="Data e Hora",
        
        # Configuração do eixo X
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(128, 128, 128, 0.3)",
            tickangle=-45,
            zeroline=True,  # Mostrar linha base no 0
            zerolinecolor="rgba(255, 255, 255, 0.8)",
            zerolinewidth=2,
            nticks=10
        ),
        
        # Eixo Y esquerdo - Temperatura (°C)
        yaxis=dict(
            title="Temperatura (°C)",
            titlefont=dict(color="#FF6347", size=14),
            tickfont=dict(color="#FF6347"),
            showgrid=True,
            gridcolor="rgba(255, 99, 71, 0.2)",
            zeroline=True,
            zerolinecolor="rgba(255, 99, 71, 0.3)",
            side="left"
        ),
        
        # Eixo Y direito - Umidade (%)
        yaxis2=dict(
            title="Umidade (%)",
            titlefont=dict(color="#4682B4", size=14),
            tickfont=dict(color="#4682B4"),
            showgrid=False,  # Não mostrar grid para não conflitar
            zeroline=False,
            overlaying="y",  # Sobrepor ao eixo Y principal
            side="right",
            range=[0, 100]  # Fixar range de 0 a 100% para umidade
        ),
        
        # Configurações gerais do layout
        legend=dict(
            x=0.01, 
            y=0.99, 
            font=dict(size=12, color="white"), 
            bgcolor="rgba(0, 0, 0, 0.5)",
            bordercolor="rgba(255, 255, 255, 0.2)",
            borderwidth=1
        ),
        plot_bgcolor="#2f2f2f",  # Fundo do gráfico
        paper_bgcolor="#2f2f2f",  # Fundo do papel
        font=dict(color="white"),  # Cor da fonte para contraste
        margin=dict(l=80, r=80, t=50, b=100),  # Margens ajustadas para os dois eixos
        hovermode="x unified",  # Hover unificado para ambas as séries
    )
    combined_graph = pio.to_html(fig, full_html=False)
    return render_template("dashboard.html", combined_graph=combined_graph)


@app.route('/export_csv', methods=['GET'])
@login_required
def export_csv():
    logger.info("Exportando dados para CSV")
    dados = DadosSensor.query.order_by(DadosSensor.timestamp.asc()).all()

    # Criação do CSV
    def generate():
        data = StringIO()
        writer = csv.writer(data)
        writer.writerow(('Timestamp', 'Temperatura', 'Umidade'))  # Cabeçalho do CSV

        for dado in dados:
            writer.writerow((dado.timestamp.strftime("%d/%m/%Y %H:%M:%S"), dado.temperatura, dado.umidade))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # Retornar o CSV como resposta
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=dados.csv"})



# Inicialização do banco de dados
def init_db():
    with app.app_context():
        db.create_all()
        logger.info("Tabelas criadas no banco de dados.")


if __name__ == "__main__":
    init_db()
    logger.info("Iniciando o servidor Flask...")
    
    # Configurações do servidor
    host = '127.0.0.1'
    port = 5000
    
    print("\n" + "="*60)
    print("🌐 SERVIDOR FLASK INICIADO COM SUCESSO!")
    print("="*60)
    print(f"📍 URL de Acesso: http://{host}:{port}")
    print(f"🔗 Link direto: http://localhost:{port}")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("🔑 Login: http://localhost:5000/login")
    print("📝 Registro: http://localhost:5000/register")
    print("="*60)
    print("⚠️  Para parar o servidor: Ctrl+C")
    print("="*60 + "\n")
    
    app.run(debug=True, host=host, port=port)  # Inicia o servidor com configurações explícitas
