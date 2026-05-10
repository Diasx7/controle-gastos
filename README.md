# Fluxo — Controle de Gastos Pessoais

Sistema de controle financeiro pessoal com visual dark mode, login por CPF e dashboard com gráficos animados.

## O que ele faz

- Cadastro e login com CPF validado matematicamente
- Senha criptografada no banco de dados
- Cadastrar receitas e despesas com categoria e data
- Dashboard com resumo do mês (receitas, despesas, saldo)
- Gráfico de rosca animado com gastos por categoria
- Editar e deletar transações
- Filtrar por mês
- Exportar transações em CSV

## Tecnologias usadas

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- Bootstrap (substituído por CSS próprio)
- Chart.js
- Google Fonts (Syne + DM Sans)

## Como rodar

```powershell
git clone https://github.com/Diasx7/controle-gastos.git
cd controle-gastos
python -m venv venv
.\venv\Scripts\Activate
pip install flask flask-sqlalchemy
python app.py
```

Acesse no navegador: `http://localhost:5000`
