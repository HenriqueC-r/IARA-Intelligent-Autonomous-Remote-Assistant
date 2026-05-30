from llm.ollama_client import perguntar_ia
import json
import os
import re
import unicodedata


DEBUG_LOGS = os.environ.get("IARA_DEBUG") == "1"


def debug_print(*args):
    if DEBUG_LOGS:
        print(*args)


SITES = {
    "google": "https://google.com",
    "youtube": "https://youtube.com",
    "github": "https://github.com",
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
}

PROGRAMAS = {
    "vscode",
    "terminal",
    "chrome",
    "firefox",
    "brave",
    "spotify",
    "calculadora",
    "roblox",
}

PALAVRAS_AUTOMACAO = (
    "abra",
    "abre",
    "abrir",
    "pesquise",
    "pesquisa",
    "pesquisar",
    "procure",
    "procurar",
    "digite",
    "digitar",
    "pressione",
    "apertar",
    "aperte",
    "assistir",
    "ver",
    "ouvir",
    "escutar",
    "tocar",
    "toca",
    "reproduzir",
    "youtube",
    "spotify",
)


def _normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(char for char in texto if not unicodedata.combining(char))


def _limpar_alvo(texto):
    texto = re.sub(r"^(o|a|os|as|um|uma)\s+", "", texto.strip())
    return texto.strip(" .,!?:;")


def _limpar_pesquisa(texto):
    texto = _limpar_alvo(texto)
    texto = re.sub(r"^(para mim|pra mim)\s+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"^(sobre|por)\s+", "", texto, flags=re.IGNORECASE)
    return texto.strip()


def _limpar_programa(texto):
    texto = _limpar_alvo(texto)
    texto = re.sub(r"\s+para\s+.+$", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\s+pra\s+.+$", "", texto, flags=re.IGNORECASE)
    return texto.strip()


def _parece_automacao(mensagem):
    texto = _normalizar(mensagem)
    return any(re.search(rf"\b{palavra}\b", texto) for palavra in PALAVRAS_AUTOMACAO)


def _extrair_pesquisa(texto):
    padroes = [
        r"\b(?:pesquise|pesquisa|pesquisar|procure|procurar)(?:\s+por)?\s+(.+)",
        r"\be\s+(?:pesquise|pesquisa|pesquisar|procure|procurar)(?:\s+por)?\s+(.+)",
    ]

    for padrao in padroes:
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            return _limpar_pesquisa(match.group(1))

    return None


def _extrair_busca_youtube(original, texto_normalizado):
    if "youtube" in texto_normalizado:
        busca = re.sub(
            r"\s+(?:no|na|pelo|pela)\s+youtube\b",
            "",
            original,
            flags=re.IGNORECASE,
        )
        busca = re.sub(r"\byoutube\b", "", busca, flags=re.IGNORECASE)
        busca = re.sub(
            r"^(quero\s+)?(?:ver|assistir|abrir|abra|abre|pesquisar|pesquise|pesquisa|procure|procurar)\s+",
            "",
            busca.strip(),
            flags=re.IGNORECASE,
        )
        busca = _limpar_pesquisa(busca)
        busca_normalizada = _normalizar(busca)

        if busca_normalizada in {
            "quero ver",
            "quero assistir",
            "ver",
            "assistir",
            "abrir",
            "abra",
            "abre",
            "para mim",
            "pra mim",
        }:
            return None

        return busca or None

    match = re.search(
        r"^(?:eu\s+)?(?:quero\s+)?(?:ver|assistir)\s+(.+)",
        original,
        re.IGNORECASE,
    )

    if not match:
        return None

    busca = _limpar_pesquisa(match.group(1))
    busca_normalizada = _normalizar(busca)

    if busca_normalizada in SITES or busca_normalizada in PROGRAMAS:
        return None

    return busca or None


def _extrair_busca_spotify(original, texto_normalizado):
    if "spotify" not in texto_normalizado:
        return None

    pediu_abrir = re.search(r"\b(?:abrir|abra|abre)\b", texto_normalizado)
    pediu_musica = re.search(
        r"\b(?:ouvir|escutar|tocar|toca|reproduzir|procurar|procure|pesquisar|pesquise|pesquisa)\b",
        texto_normalizado,
    )

    if pediu_abrir and not pediu_musica:
        return None

    busca = re.sub(
        r"\s+(?:no|na|pelo|pela)\s+spotify\b",
        " ",
        original,
        flags=re.IGNORECASE,
    )
    busca = re.sub(r"\bspotify\b", " ", busca, flags=re.IGNORECASE)
    busca = re.sub(
        r"^(voce\s+pode\s+|você\s+pode\s+)?(?:eu\s+)?(?:queria\s+|quero\s+|gostaria\s+de\s+)?(?:ouvir|escutar|tocar|toca|reproduzir|procurar|procure|pesquisar|pesquise|pesquisa)\s+",
        "",
        busca.strip(),
        flags=re.IGNORECASE,
    )
    busca = re.sub(r"^(a\s+)?m[uú]sica\s+", "", busca, flags=re.IGNORECASE)
    busca = _limpar_pesquisa(busca)
    busca_normalizada = _normalizar(busca)

    sem_busca = {
        "",
        "abrir",
        "abra",
        "abre",
        "ouvir",
        "escutar",
        "tocar",
        "reproduzir",
        "quero ouvir",
        "eu queria ouvir",
        "voce pode abrir",
        "você pode abrir",
    }

    if busca_normalizada in sem_busca:
        return None

    return busca


def _plano_rapido(mensagem):
    original = mensagem.strip()
    texto = _normalizar(original)
    plano = []

    busca_spotify = _extrair_busca_spotify(original, texto)
    if busca_spotify:
        return [{
            "tool": "pesquisar_spotify",
            "args": {"pesquisa": busca_spotify}
        }]

    busca_youtube = _extrair_busca_youtube(original, texto)
    if busca_youtube is not None or "youtube" in texto:
        return [{
            "tool": "abrir_youtube",
            "args": {"pesquisa": busca_youtube} if busca_youtube else {}
        }]

    match_ver_site = re.search(
        r"^(?:eu\s+)?(?:quero\s+)?(?:ver|assistir)\s+(.+)",
        original,
        re.IGNORECASE,
    )

    if match_ver_site:
        alvo = _normalizar(_limpar_alvo(match_ver_site.group(1)))

        if alvo in SITES:
            return [{
                "tool": "abrir_site",
                "args": {"url": SITES[alvo]}
            }]

    pesquisa = _extrair_pesquisa(original)

    if pesquisa:
        pesquisa = re.sub(
            r"\s+(?:no|na|pelo|pela)\s+(google|youtube)$",
            "",
            pesquisa,
            flags=re.IGNORECASE,
        ).strip()

        if "youtube" in texto:
            return [{
                "tool": "abrir_youtube",
                "args": {"pesquisa": pesquisa}
            }]

        return [{
            "tool": "pesquisa_web",
            "args": {"query": pesquisa}
        }]

    match_digitar = re.search(r"\b(?:digite|digitar)\s+(.+)", original, re.IGNORECASE)
    if match_digitar:
        return [{
            "tool": "digitar",
            "args": {"texto": _limpar_alvo(match_digitar.group(1))}
        }]

    match_tecla = re.search(
        r"\b(?:pressione|aperte|apertar)\s+(?:a\s+tecla\s+)?(.+)",
        original,
        re.IGNORECASE,
    )
    if match_tecla:
        return [{
            "tool": "pressionar_tecla",
            "args": {"tecla": _limpar_alvo(match_tecla.group(1))}
        }]

    if not re.search(r"\b(?:abra|abre|abrir)\b", texto):
        return []

    trecho = re.sub(r"^.*?\b(?:abra|abre|abrir)\b", "", texto, count=1).strip()
    partes = re.split(r"\s*(?:,|\+|\be\b)\s*", trecho)

    for parte in partes:
        alvo = _normalizar(_limpar_programa(parte))

        if not alvo:
            continue

        if alvo in SITES:
            plano.append({
                "tool": "abrir_site",
                "args": {"url": SITES[alvo]}
            })
        elif alvo in PROGRAMAS:
            plano.append({
                "tool": "abrir_programa",
                "args": {"programa": alvo}
            })

    return plano


def gerar_plano(mensagem):
    plano_rapido = _plano_rapido(mensagem)

    if plano_rapido:
        debug_print("\n========= PLANO RÁPIDO =========")
        debug_print(plano_rapido)
        debug_print("================================\n")

        return plano_rapido

    if not _parece_automacao(mensagem):
        return []

    prompt = f"""
Você é o planner da IARA.

Sua função é converter pedidos em ações JSON.

RESPONDA SOMENTE JSON.

NUNCA:
- converse
- explique
- use markdown
- escreva texto antes
- escreva texto depois

Retorne SEMPRE uma LISTA JSON.

=================================================

TOOLS DISPONÍVEIS:

- abrir_programa
- abrir_site
- digitar
- pressionar_tecla
- pesquisa_web
- abrir_youtube
- pesquisar_spotify

=================================================

PROGRAMAS DISPONÍVEIS:

- vscode
- terminal
- chrome
- firefox
- brave
- spotify
- calculadora
- roblox

=================================================

🔥 REGRA CRÍTICA DE DECISÃO (MUITO IMPORTANTE):

Você DEVE decidir corretamente entre:

- abrir_programa
- abrir_site

### 📌 USE abrir_site quando o usuário mencionar:
- google
- youtube
- github
- instagram
- facebook
- sites
- pesquisar na internet
- qualquer serviço online

EXEMPLOS:
google → https://google.com
youtube → https://youtube.com
github → https://github.com
instagram → https://instagram.com

### 📌 USE abrir_programa quando for:
- aplicativo instalado no computador
- terminal
- vscode
- spotify
- calculadora
- chrome/firefox/brave (como app local)

=================================================

❌ NUNCA FAÇA ISSO:
- "google" como abrir_programa
- "youtube" como abrir_programa
- "github" como abrir_programa

=================================================

EXEMPLOS CORRIGIDOS:

Usuário:
abra o google

Resposta:
[
  {{
    "tool":"abrir_site",
    "args":{{
      "url":"https://google.com"
    }}
  }}
]

=================================================

Usuário:
abra o github

Resposta:
[
  {{
    "tool":"abrir_site",
    "args":{{
      "url":"https://github.com"
    }}
  }}
]

=================================================

Usuário:
abra a calculadora

Resposta:
[
  {{
    "tool":"abrir_programa",
    "args":{{
      "programa":"calculadora"
    }}
  }}
]

=================================================

Usuário:
abra spotify

Resposta:
[
  {{
    "tool":"abrir_programa",
    "args":{{
      "programa":"spotify"
    }}
  }}
]

=================================================

Usuário:
abra vscode

Resposta:
[
  {{
    "tool":"abrir_programa",
    "args":{{
      "programa":"vscode"
    }}
  }}
]

=================================================

Usuário:
abra terminal

Resposta:
[
  {{
    "tool":"abrir_programa",
    "args":{{
      "programa":"terminal"
    }}
  }}
]

=================================================

Usuário:
abra o google e pesquise flask

Resposta:
[
  {{
    "tool":"pesquisa_web",
    "args":{{
      "query":"flask"
    }}
  }}
]

=================================================

Usuário:
pesquise inteligência artificial no youtube

Resposta:
[
  {{
    "tool":"abrir_youtube",
    "args":{{
      "pesquisa":"inteligência artificial"
    }}
  }}
]

=================================================

Usuário:
abra vscode e terminal

Resposta:
[
  {{
    "tool":"abrir_programa",
    "args":{{
      "programa":"vscode"
    }}
  }},
  {{
    "tool":"abrir_programa",
    "args":{{
      "programa":"terminal"
    }}
  }}
]

=================================================

IMPORTANTE FINAL:

Se não for automação clara:
retorne []

Mensagem:
{mensagem}
"""

    resposta = perguntar_ia(prompt)

    debug_print("\n========= RESPOSTA IA =========")
    debug_print(resposta)
    debug_print("=================================\n")

    try:

        resposta = resposta.strip()

        match = re.search(r'\[.*\]', resposta, re.DOTALL)

        if not match:
            return []

        plano = json.loads(match.group(0))

        if isinstance(plano, dict):
            plano = [plano]

        tools_validas = [
            "abrir_programa",
            "abrir_site",
            "digitar",
            "pressionar_tecla",
            "pesquisa_web",
            "abrir_youtube",
            "pesquisar_spotify"
        ]

        plano_filtrado = [
            passo for passo in plano
            if passo.get("tool") in tools_validas
        ]

        debug_print("\n========= PLANO =========")
        debug_print(plano_filtrado)
        debug_print("=========================\n")

        return plano_filtrado

    except Exception as erro:

        debug_print("\nERRO PLANNER:")
        debug_print(erro)

        return []
