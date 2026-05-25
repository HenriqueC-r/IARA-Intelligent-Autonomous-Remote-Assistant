from tools.programs import abrir_programa
from tools.browser import pesquisar_google, abrir_youtube


def executar_acao(acao):

    tool = acao['tool']
    args = acao['args']

    # ======================================
    # ABRIR PROGRAMA
    # ======================================

    if tool == 'abrir_programa':

        abrir_programa(args['programa'])
        return f"Abrindo {args['programa']} 🚀"

    # ======================================
    # PESQUISA WEB
    # ======================================

    elif tool == 'pesquisa_web':

        pesquisar_google(args['query'])
        return f'Pesquisando no Google "{args["query"]}" 🔎'

    # ======================================
    # YOUTUBE
    # ======================================

    elif tool == 'abrir_youtube':

        pesquisa = args.get('pesquisa')

        abrir_youtube(pesquisa)

        if pesquisa:
            return f'Pesquisando no YouTube "{pesquisa}" 📺'

        return 'YouTube aberto 🚀'

    return 'Ação executada.'