from tools.programs import abrir_programa, obter_site_sugerido

from tools.browser import (
    pesquisar_google,
    abrir_youtube,
    pesquisar_spotify,
    abrir_site,
    digitar,
    pressionar_tecla
)


def _nome_programa(programa):
    nomes = {
        "roblox": "Roblox",
        "vscode": "VS Code",
        "spotify": "Spotify"
    }

    return nomes.get(programa, programa)


def executar_acao(acao):

    tool = acao["tool"]
    args = acao.get("args", {})

    # ======================================
    # ABRIR PROGRAMA
    # ======================================

    if tool == "abrir_programa":

        programa = args["programa"]
        abriu = abrir_programa(programa)

        if abriu:
            return f"Abrindo {programa} 🚀"

        site = obter_site_sugerido(programa)

        if site:
            return f"Não consegui encontrar o {_nome_programa(programa)}. Posso abrir no navegador?"

        return f"Não consegui encontrar o {_nome_programa(programa)} instalado."

    # ======================================
    # PESQUISA WEB
    # ======================================

    elif tool == "pesquisa_web":

        query = args.get("query") or args.get("texto")

        pesquisar_google(query)

        return f'Pesquisando "{query}" 🔎'

    # ======================================
    # YOUTUBE
    # ======================================

    elif tool == "abrir_youtube":

        pesquisa = args.get("pesquisa")

        abrir_youtube(pesquisa)

        if pesquisa:
            return f'Pesquisando "{pesquisa}" no YouTube 📺'

        return "YouTube aberto 🚀"

    # ======================================
    # SPOTIFY
    # ======================================

    elif tool == "pesquisar_spotify":

        pesquisa = args.get("pesquisa") or args.get("query")

        pesquisar_spotify(pesquisa)

        if pesquisa:
            return f'Pesquisando "{pesquisa}" no Spotify. Não consigo garantir o play automático, mas deixei a busca aberta.'

        return "Spotify aberto 🚀"

    # ======================================
    # ABRIR SITE
    # ======================================

    elif tool == "abrir_site":

        abrir_site(args["url"])
        return f'Abrindo {args["url"]} 🌐'

    # ======================================
    # DIGITAR
    # ======================================

    elif tool == "digitar":

        digitar(args["texto"])
        return f'Digitando "{args["texto"]}" ⌨️'

    # ======================================
    # PRESSIONAR TECLA
    # ======================================

    elif tool == "pressionar_tecla":

        pressionar_tecla(args["tecla"])
        return f'Tecla "{args["tecla"]}" pressionada ⌨️'

    return "Ação desconhecida"


def executar_acoes(acoes):
    resultados = []

    for acao in acoes:
        resultados.append(executar_acao(acao))

    return resultados
