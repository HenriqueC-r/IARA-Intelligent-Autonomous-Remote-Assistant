# IARA 🤖
### Intelligent Autonomous Remote Assistant

<img width="1919" height="949" alt="IARA Interface" src="https://github.com/user-attachments/assets/273298d4-7a1e-405c-a68f-05c50fab7b58" />

IARA é uma assistente de inteligência artificial local, focada em automação real e interação natural por voz e texto. Desenvolvida do zero com modelos locais via Ollama, sem depender de APIs pagas para o núcleo de IA.

---

## O que a IARA faz

Diferente de um chatbot comum, a IARA age. Ela entende o que você quer e executa no seu computador.

**Conversa**
- Responde perguntas, ensina, ajuda com código
- Mantém contexto ao longo da conversa (memória de sessão)
- Interação por voz em tempo real com reconhecimento de fala e resposta em áudio

**Automação**
- Abre programas instalados (VSCode, terminal, calculadora, Spotify...)
- Pesquisa no Google, YouTube, DuckDuckGo
- Busca músicas no Spotify por nome de artista ou faixa
- Digita texto e pressiona teclas no sistema
- Abre sites diretamente no navegador

---

## Arquitetura

\`\`\`
IARA/
├── agents/
│   ├── planner.py        # Converte linguagem natural em ações JSON
│   ├── executor.py       # Gera confirmações antes de executar
│   └── executador_real.py # Executa as ações no sistema
├── llm/
│   └── ollama_client.py  # Interface com modelos locais via Ollama
├── tools/
│   ├── tool_registry.py  # Registro central de todas as ferramentas
│   ├── browser.py        # Automação de navegador
│   ├── programs.py       # Abertura de programas
│   └── web_search.py     # Pesquisa via DuckDuckGo
├── automation/
│   ├── browser_manager.py # Gerenciamento do Playwright (lazy loading)
│   ├── keyboard.py
│   ├── mouse.py
│   └── screen.py
├── routes/
│   └── chat.py           # Rotas Flask (chat, TTS, execução)
└── main.py
\`\`\`

O fluxo de uma mensagem:

\`\`\`
usuário fala/digita
      ↓
planner detecta se é automação ou conversa
      ↓
[automação] → gera plano JSON → confirmação → executa
[conversa]  → Ollama responde com contexto do histórico
      ↓
resposta em texto + áudio (TTS via OpenAI ou navegador)
\`\`\`

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python + Flask | Backend e servidor web |
| Ollama | Modelos de linguagem locais (llama3, etc) |
| Playwright | Automação de navegador (lazy loading) |
| PyAutoGUI | Controle de teclado e mouse |
| DuckDuckGo Search | Pesquisa na web |
| OpenAI TTS | Síntese de voz neural (opcional) |
| Web Speech API | Reconhecimento de voz no navegador |
| HTML / CSS / JS | Interface do chat |

---

## Instalação

**Pré-requisitos:** Python 3.10+, [Ollama](https://ollama.com) instalado e rodando

\`\`\`bash
# Clone o repositório
git clone https://github.com/HenriqueC-r/IARA-Intelligent-Autonomous-Remote-Assistant.git
cd IARA-Intelligent-Autonomous-Remote-Assistant

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Instale o Playwright
playwright install chromium
\`\`\`

Configure o \`.env\` na raiz:

\`\`\`env
OLLAMA_MODEL=llama3
OLLAMA_NUM_PREDICT=300
OLLAMA_TEMPERATURE=0.7

# Opcional — TTS neural via OpenAI
OPENAI_API_KEY=sua_chave_aqui
\`\`\`

Rode:

\`\`\`bash
python main.py
\`\`\`

Acesse \`http://localhost:5000\`

---

## Status

Em desenvolvimento ativo. A IARA já executa automações reais, mantém histórico de conversa e responde por voz. O foco atual é expandir as ferramentas disponíveis e evoluir o sistema de agentes.

---

## Autor

Desenvolvido por **Caio Henrique** — desenvolvedor Python brasileiro 🇧🇷
