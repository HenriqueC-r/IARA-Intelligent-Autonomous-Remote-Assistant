import pyautogui


def digitar(texto):

    pyautogui.write(
        texto,
        interval=0.03
    )


def apertar(tecla):

    pyautogui.press(tecla)


def atalho(*teclas):

    pyautogui.hotkey(*teclas)