from tools.programs import abrir_programa


def executar_plano(plano):

    respostas = []

    for passo in plano:

        tool = passo['tool']
        args = passo['args']

        # ======================================
        # ABRIR PROGRAMA
        # ======================================

        if tool == 'abrir_programa':

            programa = args['programa']

            respostas.append({
                'tipo': 'confirmacao',
                'mensagem': f'Posso abrir o {programa}?',
                'acao': passo
            })

        # ======================================
        # PESQUISA WEB
        # ======================================

        elif tool == 'pesquisa_web':

            query = args['query']

            respostas.append({
                'tipo': 'confirmacao',
                'mensagem': f'Posso pesquisar no Google por "{query}"?',
                'acao': passo
            })

        # ======================================
        # YOUTUBE
        # ======================================

        elif tool == 'abrir_youtube':

            pesquisa = args.get('pesquisa')

            if pesquisa:
                msg = f'Posso pesquisar no YouTube por "{pesquisa}"?'
            else:
                msg = 'Posso abrir o YouTube?'

            respostas.append({
                'tipo': 'confirmacao',
                'mensagem': msg,
                'acao': passo
            })

    return respostas