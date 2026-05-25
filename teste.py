import time

from automation.screen import capturar_tela
from automation.screen import encontrar_texto

from automation.mouse import clicar

from automation.keyboard import digitar
from automation.keyboard import apertar



print('\nVocê tem 3 segundos...')

time.sleep(3)



capturar_tela()


posicao = encontrar_texto('Firefox')

if posicao:

    x, y = posicao

    clicar(x, y)

    print('\nFirefox encontrado!')


    time.sleep(1)

    digitar('youtube')
    apertar('enter')


    print('\nPesquisa realizada!')


else:

    print('\nFirefox não encontrado.')