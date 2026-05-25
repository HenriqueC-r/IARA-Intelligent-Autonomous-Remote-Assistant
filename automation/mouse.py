import pyautogui


def clicar(x, y):

    pyautogui.moveTo(x, y, duration=0.3)
    pyautogui.click()