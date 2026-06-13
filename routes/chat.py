import json
import os
from collections import OrderedDict
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

from flask import request, jsonify, render_template, Response

from main import app

from agents.planner import gerar_plano, _parece_automacao
from agents.executor import executar_plano
from agents.executador_real import executar_acao, executar_acoes

from llm.ollama_client import perguntar_ia


DEBUG_LOGS = os.environ.get('IARA_DEBUG') == '1'
TTS_CACHE = OrderedDict()
TTS_CACHE_MAX = int(os.environ.get('IARA_TTS_CACHE_MAX', '32'))

historico_conversa = []


def debug_print(*args):
    if DEBUG_LOGS:
        print(*args)


def _cache_tts(chave, audio):
    TTS_CACHE[chave] = audio
    TTS_CACHE.move_to_end(chave)

    while len(TTS_CACHE) > TTS_CACHE_MAX:
        TTS_CACHE.popitem(last=False)


def _resposta_audio(audio):
    return Response(
        audio,
        mimetype='audio/mpeg',
        headers={
            'Cache-Control': 'no-store'
        }
    )


# ======================================
# HOME
# ======================================

@app.route('/')
def inicio():
    return render_template('painel.html')


@app.route('/tts', methods=['POST'])
def tts():

    api_key = os.environ.get('OPENAI_API_KEY')

    if not api_key:
        return jsonify({
            "erro": "OPENAI_API_KEY não configurada."
        }), 503

    dados = request.get_json() or {}
    texto = (dados.get('texto') or '').strip()

    if not texto:
        return jsonify({
            "erro": "Texto vazio."
        }), 400

    payload = {
        "model": os.environ.get('OPENAI_TTS_MODEL', 'gpt-4o-mini-tts'),
        "voice": os.environ.get('OPENAI_TTS_VOICE', 'marin'),
        "input": texto[:4096],
        "instructions": (
            "Fale em português brasileiro com naturalidade, como uma assistente "
            "calma, próxima e humana. Use ritmo conversacional, sem soar como "
            "locução comercial."
        ),
        "response_format": "mp3"
    }

    cache_key = (
        payload["model"],
        payload["voice"],
        payload["input"],
        payload["instructions"]
    )

    if cache_key in TTS_CACHE:
        TTS_CACHE.move_to_end(cache_key)
        return _resposta_audio(TTS_CACHE[cache_key])

    requisicao = urlrequest.Request(
        'https://api.openai.com/v1/audio/speech',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    try:
        with urlrequest.urlopen(requisicao, timeout=30) as resposta:
            audio = resposta.read()
    except HTTPError as erro:
        return jsonify({
            "erro": erro.read().decode('utf-8', errors='ignore')
        }), erro.code
    except URLError as erro:
        return jsonify({
            "erro": str(erro)
        }), 502

    _cache_tts(cache_key, audio)

    return _resposta_audio(audio)


# ======================================
# CHAT (PLANNER + IA)
# ======================================

@app.route('/chat', methods=['POST'])
def chat():

    global historico_conversa

    dados = request.get_json()
    mensagem = dados['mensagem']

    # ======================================
    # SÓ ENTRA NO PLANNER SE PARECER AUTOMAÇÃO
    # ======================================

    if _parece_automacao(mensagem):

        plano = gerar_plano(mensagem)

        debug_print('\n========= PLANO =========')
        debug_print(plano)
        debug_print('=========================\n')

        if len(plano) > 0:

            resposta = executar_plano(plano)

            return jsonify({
                "resposta": resposta
            })

    # ======================================
    # CHAT NORMAL (COM HISTÓRICO)
    # ======================================

    historico_conversa.append({
        'role': 'user',
        'content': mensagem
    })

    resposta = perguntar_ia(historico_conversa)

    historico_conversa.append({
        'role': 'assistant',
        'content': resposta
    })

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


@app.route('/executar-plano', methods=['POST'])
def executar_plano_real():

    dados = request.get_json()

    acoes = dados.get('acoes', [])

    respostas = executar_acoes(acoes)

    return jsonify({
        "respostas": respostas
    })