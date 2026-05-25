from automation.browser_manager import abrir_pagina


def pesquisar_youtube(canal):

    pagina = abrir_pagina()

    pagina.goto('https://youtube.com')

    pagina.fill(
        'input[name="search_query"]',
        canal
    )

    pagina.keyboard.press('Enter')