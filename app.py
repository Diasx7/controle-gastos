from flask import Flask, render_template, request, redirect, url_for, session
from database import db, Usuario, Transacao
from validar_cpf import validar_cpf
from datetime import datetime

app = Flask(__name__)

app.secret_key = "controle123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# página inicial com resumo
@app.route("/")
def index():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    # pega todas as transações do usuário logado
    transacoes = Transacao.query.filter_by(usuario_id=session["usuario_id"]).all()

    # calcula o resumo
    total_receitas = sum(t.valor for t in transacoes if t.tipo == "receita")
    total_despesas = sum(t.valor for t in transacoes if t.tipo == "despesa")
    saldo = total_receitas - total_despesas

    return render_template("index.html",
        nome=session["usuario_nome"],
        transacoes=transacoes,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo
    )

# cadastrar nova transação
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    erro = None

    if request.method == "POST":
        descricao = request.form["descricao"]
        valor = float(request.form["valor"])
        tipo = request.form["tipo"]
        categoria = request.form["categoria"]

        nova = Transacao(
            descricao=descricao,
            valor=valor,
            tipo=tipo,
            categoria=categoria,
            usuario_id=session["usuario_id"]
        )
        db.session.add(nova)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("adicionar.html", erro=erro)

# deletar transação
@app.route("/deletar/<int:id>")
def deletar(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    transacao = Transacao.query.get(id)

    # garante que o usuário só pode deletar as próprias transações
    if transacao and transacao.usuario_id == session["usuario_id"]:
        db.session.delete(transacao)
        db.session.commit()

    return redirect(url_for("index"))

# cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None

    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        senha = request.form["senha"]

        if not validar_cpf(cpf):
            erro = "CPF inválido. Verifique e tente novamente."
        else:
            usuario_existe = Usuario.query.filter_by(cpf=cpf).first()
            if usuario_existe:
                erro = "Esse CPF já tem uma conta cadastrada."
            else:
                novo_usuario = Usuario(nome=nome, cpf=cpf)
                novo_usuario.definir_senha(senha)
                db.session.add(novo_usuario)
                db.session.commit()
                return redirect(url_for("login"))

    return render_template("cadastro.html", erro=erro)

# login
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        cpf = request.form["cpf"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(cpf=cpf).first()

        if not usuario or not usuario.verificar_senha(senha):
            erro = "CPF ou senha incorretos."
        else:
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