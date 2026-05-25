import time

import mss
import pytesseract

from PIL import Image


# ======================================
# CAPTURAR TELA
# ======================================

def capturar_tela():

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = sct.grab(monitor)

        img = Image.frombytes(

            'RGB',
            screenshot.size,
            screenshot.rgb

        )

        img.save('screenshot.png')

        print('\nScreenshot salva!')


# ======================================
# LER TELA
# ======================================

def ler_tela():

    imagem = Image.open('screenshot.png')

    texto = pytesseract.image_to_string(imagem)

    return texto


# ======================================
# ENCONTRAR TEXTO
# ======================================

def encontrar_texto(texto_procurado):

    # ESPERAR UI CARREGAR
    time.sleep(1)


    imagem = Image.open('screenshot.png')


    dados = pytesseract.image_to_data(

        imagem,
        output_type=pytesseract.Output.DICT
    )


    encontrados = []


    for i, texto in enumerate(dados['text']):

        texto = texto.strip()


        # IGNORAR VAZIOS
        if texto == '':

            continue


        # ======================================
        # MATCH FLEXÍVEL
        # ======================================

        if texto_procurado.lower() in texto.lower():

            x = dados['left'][i]
            y = dados['top'][i]
            w = dados['width'][i]
            h = dados['height'][i]


            # CONFIANÇA OCR
            try:

                confianca = int(float(dados['conf'][i]))

            except:

                confianca = 0


            centro_x = x + (w // 2)
            centro_y = y + (h // 2)


            encontrados.append({

                'texto': texto,
                'x': centro_x,
                'y': centro_y,
                'confianca': confianca

            })


    # ======================================
    # NÃO ENCONTROU
    # ======================================

    if len(encontrados) == 0:

        print(f'\nTexto não encontrado: {texto_procurado}')

        return None


    # ======================================
    # MELHOR MATCH
    # ======================================

    melhor = max(

        encontrados,
        key=lambda item: item['confianca']
    )


    print('\n======= MELHOR MATCH =======')
    print(melhor)
    print('============================\n')


    return melhor['x'], melhor['y']