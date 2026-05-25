from duckduckgo_search import DDGS


def pesquisar_web(pergunta):

    try:

        with DDGS() as ddgs:

            resultados = list(

                ddgs.text(

                    pergunta,
                    max_results=3

                )

            )


        texto = ''


        for resultado in resultados:

            texto += f'''
Título: {resultado["title"]}

Conteúdo:
{resultado["body"]}

Link:
{resultado["href"]}


'''


        return texto


    except Exception as erro:

        print(erro)

        return 'Erro ao pesquisar.'