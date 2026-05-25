from playwright.sync_api import sync_playwright


# ======================================
# PLAYWRIGHT GLOBAL
# ======================================

playwright = sync_playwright().start()


# ======================================
# NAVEGADOR GLOBAL
# ======================================

browser = playwright.chromium.launch(

    headless=False,
    slow_mo=300

)


# ======================================
# ESTADO DA AIRA
# ======================================

estado = {

    'navegador_aberto': False,
    'pagina': None,
    'ultima_pesquisa': None,
    'ultimo_site': None

}


# ======================================
# ABRIR PÁGINA
# ======================================

def abrir_pagina():

    global estado

    # ======================================
    # SE JÁ EXISTE PÁGINA
    # ======================================

    if estado['pagina']:

        return estado['pagina']


    # ======================================
    # CRIAR NOVA PÁGINA
    # ======================================

    pagina = browser.new_page()


    estado['pagina'] = pagina
    estado['navegador_aberto'] = True


    print('\nNavegador da AIRA iniciado 🚀')


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

    global estado


    if estado['pagina']:

        estado['pagina'].close()


    estado['pagina'] = None
    estado['navegador_aberto'] = False


    print('\nNavegador fechado.')