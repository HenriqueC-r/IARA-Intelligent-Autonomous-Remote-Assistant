import webbrowser
import urllib.parse
import pyautogui


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


def pesquisar_spotify(pesquisa):

    if not pesquisa:
        webbrowser.open("https://open.spotify.com")
        print("Spotify aberto")
        return

    q = urllib.parse.quote(pesquisa)
    url = f"https://open.spotify.com/search/{q}"

    webbrowser.open(url)

    print(f"Pesquisando no Spotify: {pesquisa}")


# ======================================
# NOVAS TOOLS GENÉRICAS
# ======================================

def abrir_site(url):

    webbrowser.open(url)

    print(f"Abrindo site: {url}")


def digitar(texto):

    pyautogui.write(texto, interval=0.03)

    print(f"Digitando: {texto}")


def pressionar_tecla(tecla):

    pyautogui.press(tecla)

    print(f"Tecla pressionada: {tecla}")
