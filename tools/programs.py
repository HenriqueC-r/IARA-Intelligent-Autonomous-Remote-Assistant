import subprocess
from tools.browser import abrir_site


sites_sugeridos = {
    'roblox': 'https://www.roblox.com'
}


def obter_site_sugerido(programa):
    return sites_sugeridos.get(programa.lower())


def abrir_programa(programa):

    programa = programa.lower()

    programas = {

        'firefox': 'firefox',
        'chrome': 'google-chrome',
        'brave': 'brave-browser',
        'terminal': 'gnome-terminal',
        'vscode': 'code',

        'spotify': 'spotify',
        'calculadora': 'gnome-calculator'
    }

    sites_fallback = {

        'spotify': 'https://open.spotify.com',
        'github': 'https://github.com',
        'youtube': 'https://youtube.com',
        'vscode': 'https://vscode.dev',
        'chrome': 'https://google.com/chrome',
        'firefox': 'https://www.mozilla.org/firefox/'
    }

    try:

        print(f'\nTentando abrir: {programa}\n')

        comando = programas.get(programa)

        if comando:

            subprocess.Popen([comando])

            print(f'Comando: {comando}')
            print('Programa aberto com sucesso 🚀')

            return True

        # ======================================
        # FALLBACK WEB
        # ======================================

        if programa in sites_fallback:

            print('\nPrograma não instalado. Abrindo versão web...\n')

            abrir_site(sites_fallback[programa])

            return True

        print('Programa não encontrado.')

        return False

    except Exception as erro:

        print('\nERRO AO ABRIR PROGRAMA:')
        print(erro)

        if programa in sites_fallback:

            abrir_site(sites_fallback[programa])
            return True

        return False
