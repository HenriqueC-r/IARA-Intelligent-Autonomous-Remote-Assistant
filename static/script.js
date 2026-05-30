const inputMensagem = document.getElementById("mensagem")
const chatBox = document.getElementById("chat-box")
const voiceButton = document.getElementById("voice-button")

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
let recognition = null
let modoVozAtivo = false
let reconhecimentoRodando = false
let falandoAgora = false
let textoFaladoAgora = ""
let fallbackPendente = null
let vozIara = null
let audioIara = null
let ttsNeuralDisponivel = true
let falaAtualId = 0


function escolherVozIara() {
    if (!("speechSynthesis" in window)) {
        return null
    }

    let vozes = window.speechSynthesis.getVoices()

    if (!vozes.length) {
        return null
    }

    let prioridades = [
        (voz) => voz.lang === "pt-BR" && /google/i.test(voz.name),
        (voz) => voz.lang === "pt-BR" && /microsoft|francisca|maria/i.test(voz.name),
        (voz) => voz.lang === "pt-BR" && voz.localService === false,
        (voz) => voz.lang === "pt-BR",
        (voz) => /^pt/i.test(voz.lang),
        (voz) => /google|microsoft|natural|neural/i.test(voz.name),
    ]

    for (let prioridade of prioridades) {
        let voz = vozes.find(prioridade)

        if (voz) {
            return voz
        }
    }

    return vozes[0]
}


function carregarVozIara() {
    vozIara = escolherVozIara()
}


function adicionarMensagem(texto, tipo) {
    let msg = document.createElement("div")

    msg.className = `message ${tipo}`
    msg.innerText = texto

    chatBox.appendChild(msg)
    chatBox.scrollTop = chatBox.scrollHeight
}


function falarComNavegador(texto) {
    if (!("speechSynthesis" in window) || !texto) {
        return
    }

    window.speechSynthesis.cancel()

    let fala = new SpeechSynthesisUtterance(texto)

    falandoAgora = true
    textoFaladoAgora = texto

    if (!vozIara) {
        carregarVozIara()
    }

    if (vozIara) {
        fala.voice = vozIara
    }

    fala.lang = "pt-BR"
    fala.rate = 0.96
    fala.pitch = 1.04
    fala.volume = 1

    fala.onend = function () {
        falandoAgora = false
        textoFaladoAgora = ""
    }

    fala.onerror = function (erro) {
        console.warn("Erro na voz da IARA:", erro)

        falandoAgora = false
        textoFaladoAgora = ""
    }

    setTimeout(function () {
        window.speechSynthesis.speak(fala)
    }, 80)
}


async function falar(texto) {
    if (!texto) {
        return
    }

    pararFalaAtual()

    let minhaFalaId = ++falaAtualId

    falandoAgora = true
    textoFaladoAgora = texto

    if (!ttsNeuralDisponivel) {
        falarComNavegador(texto)
        return
    }

    try {
        let resposta = await fetch("/tts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                texto: texto
            })
        })

        if (!resposta.ok) {
            if (resposta.status === 503) {
                ttsNeuralDisponivel = false
            }

            if (minhaFalaId === falaAtualId) {
                falarComNavegador(texto)
            }
            return
        }

        let blob = await resposta.blob()
        let url = URL.createObjectURL(blob)

        if (minhaFalaId !== falaAtualId) {
            URL.revokeObjectURL(url)
            return
        }

        audioIara = new Audio(url)

        audioIara.onended = function () {
            falandoAgora = false
            textoFaladoAgora = ""
            URL.revokeObjectURL(url)
            audioIara = null
        }

        audioIara.onerror = function () {
            URL.revokeObjectURL(url)
            audioIara = null
            falarComNavegador(texto)
        }

        await audioIara.play()
    }
    catch (erro) {
        console.warn("TTS neural indisponível:", erro)
        if (minhaFalaId === falaAtualId) {
            falarComNavegador(texto)
        }
    }
}


function pararFalaAtual() {
    falaAtualId++

    if (audioIara) {
        audioIara.pause()
        audioIara.currentTime = 0
        audioIara = null
    }

    if ("speechSynthesis" in window && (window.speechSynthesis.speaking || falandoAgora)) {
        window.speechSynthesis.cancel()
    }

    falandoAgora = false
    textoFaladoAgora = ""
}


function normalizarTextoVoz(texto) {
    return texto
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^\w\s]/g, "")
        .replace(/\s+/g, " ")
        .trim()
}


function pareceEcoDaIara(texto) {
    if (!textoFaladoAgora) {
        return false
    }

    let ouvido = normalizarTextoVoz(texto)
    let falado = normalizarTextoVoz(textoFaladoAgora)

    if (ouvido.length < 4 || falado.length < 4) {
        return false
    }

    return falado.includes(ouvido) || ouvido.includes(falado)
}


function limparComandoVoz(texto) {
    return texto
        .trim()
        .replace(/^(iara|yara|lara|ia ra)[,\s]+/i, "")
        .trim()
}


function nomeDoSite(url) {
    let nomes = {
        "google.com": "Google",
        "youtube.com": "YouTube",
        "github.com": "GitHub",
        "instagram.com": "Instagram",
        "facebook.com": "Facebook"
    }

    for (let dominio in nomes) {
        if (url.includes(dominio)) {
            return nomes[dominio]
        }
    }

    return url
        .replace(/^https?:\/\//, "")
        .replace(/^www\./, "")
        .replace(/\/$/, "")
}


function juntarItens(itens) {
    if (itens.length === 0) {
        return ""
    }

    if (itens.length === 1) {
        return itens[0]
    }

    return `${itens.slice(0, -1).join(", ")} e ${itens[itens.length - 1]}`
}


function nomeDoPrograma(programa) {
    let nomes = {
        "roblox": "Roblox",
        "vscode": "VS Code",
        "spotify": "Spotify"
    }

    return nomes[programa] || programa
}


function respostaAutomacao(acoes, respostas) {
    let falhas = respostas.filter((resposta) => resposta.startsWith("Não consegui"))

    if (falhas.length > 0) {
        return falhas.join(" ")
    }

    let aberturas = []
    let outras = []

    for (let acao of acoes) {
        let args = acao.args || {}

        if (acao.tool === "abrir_programa") {
            aberturas.push(nomeDoPrograma(args.programa))
        }
        else if (acao.tool === "abrir_site") {
            aberturas.push(nomeDoSite(args.url || "site"))
        }
        else if (acao.tool === "abrir_youtube") {
            if (args.pesquisa) {
                outras.push(`pesquisando ${args.pesquisa} no YouTube`)
            }
            else {
                aberturas.push("YouTube")
            }
        }
        else if (acao.tool === "pesquisar_spotify") {
            if (args.pesquisa || args.query) {
                outras.push(`buscando ${args.pesquisa || args.query} no Spotify. Não consigo garantir o play automático`)
            }
            else {
                aberturas.push("Spotify")
            }
        }
        else if (acao.tool === "pesquisa_web") {
            outras.push(`pesquisando ${args.query || args.texto}`)
        }
        else if (acao.tool === "digitar") {
            outras.push(`digitando ${args.texto}`)
        }
        else if (acao.tool === "pressionar_tecla") {
            outras.push(`pressionando ${args.tecla}`)
        }
    }

    if (aberturas.length > 0 && outras.length === 0) {
        return `Claro, abrindo ${juntarItens(aberturas)}.`
    }

    if (outras.length > 0 && aberturas.length === 0) {
        return `Claro, ${juntarItens(outras)}.`
    }

    if (aberturas.length > 0 && outras.length > 0) {
        return `Claro, abrindo ${juntarItens(aberturas)} e ${juntarItens(outras)}.`
    }

    return respostas.join(" ")
}


function ehConfirmacao(texto) {
    return /^(sim|s|claro|pode|pode sim|ok|beleza|manda|abrir)$/i.test(texto.trim())
}


function ehNegacao(texto) {
    return /^(nao|não|n|cancelar|cancela)$/i.test(texto.trim())
}


function deveDesligarVoz(texto) {
    return /^(iara\s+)?(para|pare|parar|desliga|desligue|cancela|cancelar)\s+(de\s+)?(o\s+|a\s+)?(ouvir|escutar|me ouvir|microfone|mic)$/i.test(texto.trim())
}


function atualizarBotaoVoz() {
    if (!voiceButton) {
        return
    }

    voiceButton.classList.toggle("listening", modoVozAtivo)
    voiceButton.title = modoVozAtivo ? "Desligar microfone" : "Usar microfone"
    voiceButton.setAttribute("aria-label", modoVozAtivo ? "Desligar microfone" : "Usar microfone")
}


function iniciarReconhecimento() {
    if (!recognition || reconhecimentoRodando || !modoVozAtivo) {
        return
    }

    try {
        recognition.start()
    }
    catch (erro) {
        console.warn("Reconhecimento já estava ativo.")
    }
}


function desligarModoVoz(responder = true) {
    modoVozAtivo = false
    atualizarBotaoVoz()

    if (recognition && reconhecimentoRodando) {
        recognition.stop()
    }

    if (responder) {
        let resposta = "Tudo bem, parei de ouvir."

        adicionarMensagem(resposta, "ai")
        falar(resposta)
    }
}


async function enviarMensagem(textoForcado = null) {
    let texto = textoForcado || inputMensagem.value

    texto = texto.trim()

    if (texto === "") {
        return
    }

    adicionarMensagem(texto, "user")

    inputMensagem.value = ""

    if (deveDesligarVoz(texto)) {
        desligarModoVoz()
        return
    }

    if (fallbackPendente && ehConfirmacao(texto)) {
        let pendente = fallbackPendente
        fallbackPendente = null

        await fetch("/executar-plano", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                acoes: [{
                    tool: "abrir_site",
                    args: {
                        url: pendente.url
                    }
                }]
            })
        })

        let resposta = `Claro, abrindo ${pendente.nome} no navegador.`

        adicionarMensagem(resposta, "ai")
        falar(resposta)
        return
    }

    if (fallbackPendente && ehNegacao(texto)) {
        fallbackPendente = null

        let resposta = "Tudo bem, não vou abrir."

        adicionarMensagem(resposta, "ai")
        falar(resposta)
        return
    }

    try {
        let resposta = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                mensagem: texto
            })
        })

        let dados = await resposta.json()

        if (Array.isArray(dados.resposta)) {
            let acoes = dados.resposta.map((item) => item.acao)

            let executar = await fetch("/executar-plano", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    acoes: acoes
                })
            })

            let resultado = await executar.json()
            let respostaFinal = respostaAutomacao(acoes, resultado.respostas || [])
            let pediuFallback = respostaFinal.includes("Posso abrir no navegador?")

            if (pediuFallback) {
                let acao = acoes.find((item) => item.tool === "abrir_programa")
                let programa = acao && acao.args ? acao.args.programa : "site"

                fallbackPendente = {
                    nome: nomeDoPrograma(programa),
                    url: "https://www.roblox.com"
                }
            }

            adicionarMensagem(respostaFinal, "ai")
            falar(respostaFinal)

            return
        }

        adicionarMensagem(dados.resposta, "ai")
        falar(dados.resposta)
    }
    catch (erro) {
        console.error("ERRO JS:")
        console.error(erro)

        let mensagemErro = "Não consegui processar isso agora."

        adicionarMensagem(mensagemErro, "ai")
        falar(mensagemErro)
    }
}


function configurarMicrofone() {
    if (!SpeechRecognition || !voiceButton) {
        if (voiceButton) {
            voiceButton.disabled = true
            voiceButton.title = "Microfone indisponível neste navegador"
        }

        return
    }

    recognition = new SpeechRecognition()
    recognition.lang = "pt-BR"
    recognition.continuous = true
    recognition.interimResults = false

    recognition.onstart = function () {
        reconhecimentoRodando = true
        atualizarBotaoVoz()
    }

    recognition.onend = function () {
        reconhecimentoRodando = false

        if (modoVozAtivo) {
            setTimeout(iniciarReconhecimento, 250)
            return
        }

        atualizarBotaoVoz()
    }

    recognition.onerror = function (evento) {
        if (!modoVozAtivo || evento.error === "no-speech" || evento.error === "aborted") {
            return
        }

        let texto = "Não consegui ouvir direito, mas sigo ouvindo."

        adicionarMensagem(texto, "ai")
        falar(texto)
    }

    recognition.onresult = function (evento) {
        let resultado = evento.results[evento.results.length - 1][0].transcript

        if (falandoAgora || window.speechSynthesis.speaking) {
            if (pareceEcoDaIara(resultado)) {
                return
            }

            pararFalaAtual()
        }

        let comando = limparComandoVoz(resultado)

        enviarMensagem(comando)
    }

    voiceButton.addEventListener("click", function () {
        if (modoVozAtivo) {
            desligarModoVoz(false)
            return
        }

        modoVozAtivo = true
        atualizarBotaoVoz()
        iniciarReconhecimento()
        falar("Estou ouvindo.")
    })
}


inputMensagem.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        enviarMensagem()
    }
})


configurarMicrofone()

if ("speechSynthesis" in window) {
    carregarVozIara()
    window.speechSynthesis.onvoiceschanged = carregarVozIara
}
