from tools.browser import (
    pesquisar_google,
    abrir_youtube,
    abrir_site,
    digitar,
    pressionar_tecla,
    pesquisar_spotify
)
from tools.programs import abrir_programa


TOOLS = {
    "abrir_programa":    abrir_programa,
    "pesquisa_web":      pesquisar_google,
    "abrir_youtube":     abrir_youtube,
    "pesquisar_spotify": pesquisar_spotify,
    "abrir_site":        abrir_site,
    "digitar":           digitar,
    "pressionar_tecla":  pressionar_tecla,
}


def executar_tool(tool, args):
    func = TOOLS.get(tool)

    if not func:
        return f"Tool '{tool}' não encontrada."

    try:
        return func(**args) or "Feito."
    except Exception as erro:
        return f"Erro ao executar '{tool}': {erro}"