async function enviarMensagem(){

    let input = document.getElementById("mensagem")

    let texto = input.value


    if(texto == ""){

        return

    }


    let chatBox = document.getElementById("chat-box")


    // ======================================
    // MENSAGEM USUÁRIO
    // ======================================

    let userMsg = document.createElement("div")

    userMsg.className = "message user"

    userMsg.innerText = texto

    chatBox.appendChild(userMsg)

    input.value = ""


    // ======================================
    // ENVIAR
    // ======================================

    let resposta = await fetch("/chat", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            mensagem:texto
        })

    })


    let dados = await resposta.json()


    // ======================================
    // CONFIRMAÇÕES
    // ======================================

    if(Array.isArray(dados.resposta)){

        for(let item of dados.resposta){

            let confirmar = confirm(item.mensagem)


            // ======================================
            // ACEITOU
            // ======================================

            if(confirmar){

                let executar = await fetch("/executar", {

                    method:"POST",

                    headers:{
                        "Content-Type":"application/json"
                    },

                    body:JSON.stringify({
                        acao:item.acao
                    })

                })


                let resultado = await executar.json()


                let aiMsg = document.createElement("div")

                aiMsg.className = "message ai"

                aiMsg.innerText = resultado.resposta

                chatBox.appendChild(aiMsg)

            }


            // ======================================
            // NEGOU
            // ======================================

            else{

                let aiMsg = document.createElement("div")

                aiMsg.className = "message ai"

                aiMsg.innerText = "Ação cancelada."

                chatBox.appendChild(aiMsg)

            }

        }

    }


    // ======================================
    // CHAT NORMAL
    // ======================================

    else{

        let aiMsg = document.createElement("div")

        aiMsg.className = "message ai"

        aiMsg.innerText = dados.resposta

        chatBox.appendChild(aiMsg)

    }


    chatBox.scrollTop = chatBox.scrollHeight
}


document.getElementById("mensagem")
.addEventListener("keypress", function(e){

    if(e.key === "Enter"){

        enviarMensagem()

    }

})