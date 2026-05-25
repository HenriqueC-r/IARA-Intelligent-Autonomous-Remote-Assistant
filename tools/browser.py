import webbrowser
import urllib.parse


def pesquisar_google(pesquisa):

    if not pesquisa:
        return

    q = urllib.parse.quote(pesquisa)
    url = f"https://www.google.com/search?q={q}"

    webbrowser.open(url)

    print(f"Pesquisando no Google: {pesquisa}")


def abrir_youtube(pesquisa=None):

    if not pesquisa:
        webbrowser.open("https://youtube.com")
        print("YouTube aberto 🚀")
        return

    q = urllib.parse.quote(pesquisa)
    url = f"https://www.youtube.com/results?search_query={q}"

    webbrowser.open(url)

    print(f"Pesquisando no YouTube: {pesquisa}")