from agents.executador_real import executar_acao

executar_acao({
    "tool": "abrir_site",
    "args": {
        "url": "https://google.com"
    }
})


executar_acao({
    "tool": "digitar",
    "args": {
        "texto": "Python Flask"
    }
})



executar_acao({
    "tool": "pressionar_tecla",
    "args": {
        "tecla": "enter"
    }
})