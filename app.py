from flask import Flask, render_template, request, redirect, url_for, session
from database import db, Usuario
from validar_cpf import validar_cpf

app = Flask(__name__)

# chave secreta pra sessão funcionar
app.secret_key = "controle123"

# configuração do banco de dados (arquivo local sqlite)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# conecta o banco ao app
db.init_app(app)

# cria as tabelas no banco se não existirem
with app.app_context():
    db.create_all()

# página inicial - só aparece se estiver logado
@app.route("/")
def index():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", nome=session["usuario_nome"])

# página de cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None

    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        senha = request.form["senha"]

        # valida o cpf antes de salvar
        if not validar_cpf(cpf):
            erro = "CPF inválido. Verifique e tente novamente."
        else:
            # verifica se o cpf já tá cadastrado
            usuario_existe = Usuario.query.filter_by(cpf=cpf).first()
            if usuario_existe:
                erro = "Esse CPF já tem uma conta cadastrada."
            else:
                # cria o usuário e salva no banco
                novo_usuario = Usuario(nome=nome, cpf=cpf)
                novo_usuario.definir_senha(senha)
                db.session.add(novo_usuario)
                db.session.commit()
                return redirect(url_for("login"))

    return render_template("cadastro.html", erro=erro)

# página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        cpf = request.form["cpf"]
        senha = request.form["senha"]

        # busca o usuário pelo cpf
        usuario = Usuario.query.filter_by(cpf=cpf).first()

        if not usuario or not usuario.verificar_senha(senha):
            erro = "CPF ou senha incorretos."
        else:
            # salva o usuário na sessão
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            return redirect(url_for("index"))

    return render_template("login.html", erro=erro)

# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)