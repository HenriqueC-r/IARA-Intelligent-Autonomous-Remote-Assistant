def executar_plano(plano):

    respostas = []

    for passo in plano:

        tool = passo["tool"]
        args = passo.get("args", {})

        # ======================================
        # ABRIR PROGRAMA
        # ======================================

        if tool == "abrir_programa":

            programa = args["programa"]

            respostas.append({
                "tipo": "confirmacao",
                "mensagem": f'Posso abrir {programa}?',
                "acao": passo
            })

        # ======================================
        # PESQUISA WEB
        # ======================================

        elif tool == "pesquisa_web":

            query = args.get("query") or args.get("texto")

            respostas.append({
                "tipo": "confirmacao",
                "mensagem": f'Posso pesquisar "{query}"?',
                "acao": passo
            })

        # ======================================
        # YOUTUBE
        # ======================================

        elif tool == "abrir_youtube":

            pesquisa = args.get("pesquisa")

            if pesquisa:
                msg = f'Posso pesquisar "{pesquisa}" no YouTube?'
            else:
                msg = "Posso abrir o YouTube?"

            respostas.append({
                "tipo": "confirmacao",
                "mensagem": msg,
                "acao": passo
            })

        # ======================================
        # SPOTIFY
        # ======================================

        elif tool == "pesquisar_spotify":

            pesquisa = args.get("pesquisa") or args.get("query")

            if pesquisa:
                msg = f'Posso buscar "{pesquisa}" no Spotify?'
            else:
                msg = "Posso abrir o Spotify?"

            respostas.append({
                "tipo": "confirmacao",
                "mensagem": msg,
                "acao": passo
            })

        # ======================================
        # ABRIR SITE
        # ======================================

        elif tool == "abrir_site":

            url = args["url"]

            respostas.append({
                "tipo": "confirmacao",
                "mensagem": f'Abrir {url}?',
                "acao": passo
            })

        # ======================================
        # DIGITAR
        # ======================================

        elif tool == "digitar":

            respostas.append({
                "tipo": "confirmacao",
                "mensagem": f'Digitar "{args["texto"]}"?',
                "acao": passo
            })

        # ======================================
        # PRESSIONAR TECLA
        # ======================================

        elif tool == "pressionar_tecla":

            respostas.append({
                "tipo": "confirmacao",
                "mensagem": f'Pressionar {args["tecla"]}?',
                "acao": passo
            })

    return respostas
