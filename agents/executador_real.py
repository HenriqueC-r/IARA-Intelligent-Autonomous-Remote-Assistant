from tools.tool_registry import executar_tool, TOOLS
from tools.programs import abrir_programa, obter_site_sugerido


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
    # ABRIR PROGRAMA (tratamento especial)
    # ======================================

    if tool == "abrir_programa":
        programa = args["programa"]
        abriu = abrir_programa(programa)

        if abriu:
            return f"Abrindo {_nome_programa(programa)} 🚀"

        site = obter_site_sugerido(programa)

        if site:
            return f"Não consegui encontrar o {_nome_programa(programa)}. Posso abrir no navegador?"

        return f"Não consegui encontrar o {_nome_programa(programa)} instalado."

    # ======================================
    # TODAS AS OUTRAS TOOLS VIA REGISTRY
    # ======================================

    if tool == "pesquisa_web":
        args["query"] = args.get("query") or args.get("texto")

    if tool == "pesquisar_spotify":
        args["pesquisa"] = args.get("pesquisa") or args.get("query")

    executar_tool(tool, args)

    MENSAGENS = {
        "pesquisa_web":      lambda a: f'Pesquisando "{a.get("query")}" 🔎',
        "abrir_youtube":     lambda a: f'Pesquisando "{a.get("pesquisa")}" no YouTube 📺' if a.get("pesquisa") else "YouTube aberto 🚀",
        "pesquisar_spotify": lambda a: f'Buscando "{a.get("pesquisa")}" no Spotify 🎵' if a.get("pesquisa") else "Spotify aberto 🚀",
        "abrir_site":        lambda a: f'Abrindo {a.get("url")} 🌐',
        "digitar":           lambda a: f'Digitando "{a.get("texto")}" ⌨️',
        "pressionar_tecla":  lambda a: f'Tecla "{a.get("tecla")}" pressionada ⌨️',
    }

    mensagem = MENSAGENS.get(tool)

    if mensagem:
        return mensagem(args)

    return "Ação desconhecida."


def executar_acoes(acoes):
    return [executar_acao(acao) for acao in acoes]