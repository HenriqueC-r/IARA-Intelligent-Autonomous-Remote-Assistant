import subprocess


def abrir_programa(programa):

    programas = {

        'firefox':'firefox',
        'chrome':'google-chrome',
        'brave':'brave-browser',
        'terminal':'gnome-terminal',
        'vscode':'code'

    }


    try:

        print(f'\nTentando abrir: {programa}\n')


        comando = programas.get(programa)


        if not comando:

            print('Programa não encontrado.')

            return


        subprocess.Popen(comando)


        print(f'Comando: {comando}')
        print('Programa aberto com sucesso 🚀')


    except Exception as erro:

        print('\nERRO AO ABRIR PROGRAMA:')
        print(erro)