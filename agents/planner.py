from llm.ollama_client import perguntar_ia
import json
import re


def gerar_plano(mensagem):

    prompt = """
Você é um planner de automação da IARA.

Sua função:
converter pedidos em passos JSON.

IMPORTANTE:
- responda SOMENTE JSON
- SEM explicações
- SEM markdown
- SEM texto extra
- SEM conversa
- NÃO invente tools

SEMPRE responda uma LISTA JSON.

AS ÚNICAS TOOLS EXISTENTES SÃO:

- abrir_programa
- pesquisa_web
- abrir_youtube

REGRAS IMPORTANTES:

1. Se mencionar "youtube":
   use "abrir_youtube"

2. Se não mencionar plataforma:
   use "pesquisa_web"

3. Se pedir navegador:
   use "abrir_programa"

4. Se NÃO for automação:
   responda []

---

EXEMPLOS:

Mensagem:
abre youtube

Resposta:
[
  {
    "tool": "abrir_youtube",
    "args": {
      "pesquisa": null
    }
  }
]

---

Mensagem:
abre youtube e pesquisa aqueles caras

Resposta:
[
  {
    "tool": "abrir_youtube",
    "args": {
      "pesquisa": "aqueles caras"
    }
  }
]

---

Mensagem:
pesquisa python flask

Resposta:
[
  {
    "tool": "pesquisa_web",
    "args": {
      "query": "python flask"
    }
  }
]

---

Mensagem:
abre chrome

Resposta:
[
  {
    "tool": "abrir_programa",
    "args": {
      "programa": "chrome"
    }
  }
]

---

Mensagem:
"""

    prompt += mensagem

    resposta = perguntar_ia(prompt)

    print('\n========= RESPOSTA IA =========')
    print(resposta)
    print('=================================\n')

    try:
        resposta = resposta.strip()

        match = re.search(r'\[.*\]', resposta, re.DOTALL)

        if not match:
            return []

        plano = json.loads(match.group(0))

        if isinstance(plano, dict):
            plano = [plano]

        tools_validas = [
            'abrir_programa',
            'pesquisa_web',
            'abrir_youtube'
        ]

        plano_filtrado = [
            passo for passo in plano
            if passo.get("tool") in tools_validas
        ]

        print('\n========= PLANO =========')
        print(plano_filtrado)
        print('=========================\n')

        return plano_filtrado

    except Exception as erro:
        print('\nERRO PLANNER:')
        print(erro)
        return []