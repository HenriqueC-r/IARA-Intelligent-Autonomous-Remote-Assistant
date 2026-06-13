from playwright.sync_api import sync_playwright


# ======================================
# ESTADO GLOBAL (começa tudo None)
# ======================================

_playwright = None
_browser = None

estado = {
    'navegador_aberto': False,
    'pagina': None,
    'ultima_pesquisa': None,
    'ultimo_site': None
}


# ======================================
# INICIALIZAR PLAYWRIGHT (lazy)
# ======================================

def _garantir_browser():
    global _playwright, _browser

    if _browser is not None:
        return

    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(
        headless=False,
        slow_mo=300
    )

    print('\nPlaywright iniciado 🚀')


# ======================================
# ABRIR PÁGINA
# ======================================

def abrir_pagina():
    global estado

    if estado['pagina']:
        return estado['pagina']

    _garantir_browser()

    pagina = _browser.new_page()

    estado['pagina'] = pagina
    estado['navegador_aberto'] = True

    print('\nNavegador da IARA iniciado 🚀')

    return pagina


# ======================================
# PEGAR PÁGINA ATUAL
# ======================================

def pegar_pagina():
    return estado['pagina']


# ======================================
# SALVAR ÚLTIMO SITE
# ======================================

def salvar_site(site):
    estado['ultimo_site'] = site


# ======================================
# SALVAR PESQUISA
# ======================================

def salvar_pesquisa(pesquisa):
    estado['ultima_pesquisa'] = pesquisa


# ======================================
# FECHAR NAVEGADOR
# ======================================

def fechar_navegador():
    global estado, _browser, _playwright

    if estado['pagina']:
        estado['pagina'].close()

    if _browser:
        _browser.close()
        _browser = None

    if _playwright:
        _playwright.stop()
        _playwright = None

    estado['pagina'] = None
    estado['navegador_aberto'] = False

    print('\nNavegador fechado.')