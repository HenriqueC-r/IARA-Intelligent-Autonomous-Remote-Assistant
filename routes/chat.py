from flask import request, jsonify, render_template

from main import app

from agents.planner import gerar_plano
from agents.executor import executar_plano
from agents.executador_real import executar_acao

from llm.ollama_client import perguntar_ia
from tools.browser import pesquisar_google



# ======================================
# HOME
# ======================================

@app.route('/')
def inicio():
    return render_template('painel.html')


# ======================================
# CHAT (PLANNER + IA)
# ======================================

@app.route('/chat', methods=['POST'])
def chat():

    dados = request.get_json()
    mensagem = dados['mensagem']

    # ======================================
    # GERA PLANO (AUTOMAÇÃO)
    # ======================================

    plano = gerar_plano(mensagem)

    print('\n========= PLANO =========')
    print(plano)
    print('=========================\n')

    # ======================================
    # SE FOR AUTOMAÇÃO
    # ======================================

    if len(plano) > 0:

        resposta = executar_plano(plano)

        return jsonify({
            "resposta": resposta
        })

    # ======================================
    # CHAT NORMAL (SEM AUTOMAÇÃO)
    # ======================================

    resposta = perguntar_ia(mensagem)

    return jsonify({
        "resposta": resposta
    })


# ======================================
# EXECUÇÃO REAL (CHAMADO PELO FRONTEND)
# ======================================

@app.route('/executar', methods=['POST'])
def executar():

    dados = request.get_json()

    acao = dados['acao']

    resposta = executar_acao(acao)

    return jsonify({
        "resposta": resposta
    })