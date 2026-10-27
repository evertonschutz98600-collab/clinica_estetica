import json
import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "sua_unica_chave_secreta_para_sessoes"

ARQUIVO_SERVICOS = "servicos.json"
ARQUIVO_CLIENTES = "clientes.json"
ARQUIVO_AGENDAMENTOS = "agendamentos.json"

def carregar_dados(caminho_ficheiro):
    if not os.path.exists(caminho_ficheiro):
        return []
    with open(caminho_ficheiro, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_dados(caminho_ficheiro, dados):
    with open(caminho_ficheiro, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Rota Principal - Acesso direto sem login obrigatório
@app.route('/')
def index():
    servicos = carregar_dados(ARQUIVO_SERVICOS)
    return render_template('index.html', servicos=servicos)

# Rota para salvar agendamentos vindos da barra flutuante
@app.route('/salvar_agendamento', methods=['POST'])
def salvar_agendamento():
    dados = request.get_json()
    if not dados:
        return jsonify({"status": "erro", "mensagem": "Dados inválidos"}), 400

    agendamentos = carregar_dados(ARQUIVO_AGENDAMENTOS)
    
    novo_agendamento = {
        "id": len(agendamentos) + 1,
        "cliente": dados.get("cliente"),
        "profissional": dados.get("profissional"),
        "data": dados.get("data"),
        "horario": dados.get("horario"),
        "servicos": dados.get("servicos"),
        "pagamento": dados.get("pagamento"),
        "valor_total": dados.get("valor_total"),
        "status": "Pendente"
    }

    agendamentos.append(novo_agendamento)
    guardar_dados(ARQUIVO_AGENDAMENTOS, agendamentos)

    return jsonify({"status": "sucesso"})

# Rotas de acesso direto que não exigem login
@app.route('/login', methods=['GET', 'POST'])
def login_cliente():
    return redirect(url_for('index'))

@app.route('/logout')
def logout_cliente():
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)