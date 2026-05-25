from automation.browser_manager import abrir_pagina


def pesquisar_google(pesquisa):

    pagina = abrir_pagina()

    pagina.goto('https://google.com')

    pagina.fill('textarea', pesquisa)

    pagina.keyboard.press('Enter')