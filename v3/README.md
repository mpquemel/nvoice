# NVoice - Assistente de Voz com IA para NVDA

**Autor:** Melhym Quemel
**Versão:** 2.0.0

## 1\. Sobre o NVoice

O **NVoice** é um complemento que transforma o seu NVDA em um assistente cognitivo conversacional de baixíssima latência. Com ele, você pode dialogar com os modelos de Inteligência Artificial mais avançados do mundo usando a sua própria voz. O NVoice não utiliza bibliotecas pesadas de terceiros; ele faz o processamento de streaming enviando o texto da IA diretamente para a voz nativa do seu NVDA em tempo real, compatível com NVDA de 32 bit e 64 bit.

## 2\. Atalhos de Teclado (Comandos Globais)

O NVoice foi desenhado para ser acionado rapidamente, sem interromper o seu fluxo de trabalho. Abaixo estão os comandos que você utilizará no dia a dia:

  * **\<kbd\>NVDA + Z\</kbd\>**
    **Iniciar/Parar Conversa:** Pressione para que o NVoice comece a ouvir o seu microfone. O NVDA anunciará "Ouvindo...". Fale o que desejar e pressione o atalho novamente para enviar o áudio. O sistema anunciará "Processando..." e a IA responderá em instantes.

  * **\<kbd\>NVDA + Shift + Z\</kbd\>**
    **Enviar Contexto da Tela (Injeção UIA):** Funciona exatamente como o comando anterior, mas com um "superpoder": ele captura o texto exato onde o cursor do seu NVDA está focado (um parágrafo de um site, um documento do Word, uma janela do sistema) e anexa esse texto, de forma invisível, à sua pergunta.
    *Exemplo de uso:* Posicione o foco em um e-mail longo em inglês, pressione \<kbd\>NVDA + Shift + Z\</kbd\> e diga: "Traduza e resuma esta mensagem para mim".

  * **\<kbd\>NVDA + Alt + Z\</kbd\>**
    **Limpar Histórico de Conversa:** O NVoice possui *Memória de Contexto*, ou seja, a IA lembra do que vocês conversaram nas últimas iterações. Se você quiser trocar totalmente de assunto e não quiser que a IA confunda as informações, pressione este atalho. O NVDA avisará que a memória foi zerada. Este comando não apaga o histórico permanente das conversas, um recurso opcional que pode ser configurado para salvar o registro em disco.

## 3\. Configurando Provedores de IA (Nuvem)

Para utilizar os motores de IA em nuvem, você precisará de uma Chave de API (API Key). Acesse o menu do NVDA (NVDA+N), vá em **Preferências \> Configurações \> NVoice**. O NVoice suporta os seguintes provedores:

### Groq (Recomendado para velocidade na conversão de fala em texto, do inglês, Speech to Text - STT)

O Groq utiliza uma arquitetura de processamento ultrarrápida (LPU). É o motor principal recomendado para a transcrição da sua voz (STT) usando o modelo *Whisper-Large* e para chat com modelos como o *Llama 3*.

  * **Onde conseguir a API Key:** [Groq Console API Keys](https://console.groq.com/keys)
  * **Custo:** Possui uma franquia gratuita extremamente generosa.

### Google Gemini

A inteligência artificial do Google. Excelente para respostas fluídas, textos criativos e análises detalhadas.

  * **Onde conseguir a API Key:** [Google AI Studio](https://aistudio.google.com/app/apikey)
  * **Custo:** O modelo *Gemini Flash Latest* possui alto limite de requisições gratuitas diárias.

### OpenAI (ChatGPT)

A criadora do ChatGPT oferece os poderosos modelos GPT-5, GPT-5-turbo e superiores.

  * **Onde conseguir a API Key:** [OpenAI Platform](https://platform.openai.com/api-keys)
  * **Custo:** Plataforma pré-paga (Pay-as-you-go). Exige adição de créditos.

### OpenRouter (Multi-Modelos)

Um hub definitivo. Com apenas uma chave do OpenRouter, você pode conversar com centenas de modelos diferentes (Claude da Anthropic, Mistral, Meta Llama, etc.).

  * **Onde conseguir a API Key:** [OpenRouter Keys](https://openrouter.ai/keys)
  * **Custo:** Pague apenas pelo que usar. Muitos modelos possuem versões "Free" na plataforma.

## 4\. Privacidade Total: Rodando IA Local com Ollama

Se você precisa de privacidade absoluta, trabalha com dados sensíveis, ou está sem internet, o NVoice se integra perfeitamente ao **Ollama**. O Ollama permite baixar e rodar modelos de Inteligência Artificial diretamente na sua própria máquina.

> **Configuração Padrão:** O NVoice já vem configurado para buscar o Ollama no endereço local padrão: `http://localhost:11434`. Basta instalar o Ollama, selecionar "ollama" como seu provedor no painel de configurações do NVDA e clicar no botão "Buscar Modelos" para ver os modelos que você tem baixados.

### Modelos recomendados para Computadores Modestos (Sem placa de vídeo dedicada):

Se o seu computador for mais antigo ou tiver pouca memória RAM, você não precisa ficar de fora\! Baixe modelos "SLM" (Small Language Models), que são ágeis e não travam o PC:

  * `qwen2:0.5b` - Extremamente pequeno e rápido, responde em qualquer notebook básico.
  * `llama3.2:1b` - A nova versão super enxuta da Meta, excelente para textos rápidos.
  * `phi3:mini` - O modelo pequeno da Microsoft, com alta capacidade de raciocínio.

Para baixar um modelo, abra o *Prompt de Comando* (cmd) do Windows e digite, por exemplo: `ollama pull llama3.2:1b`

## 5\. 📚 Tutorial: Como instalar o Whisper e o Ollama (IA Local) no Windows

O usuário que quiser a versão Offline completa — com Reconhecimento de Voz (Whisper) e Inteligência Artificial de Texto (Ollama) rodando direto no computador — precisará fazer o seguinte:

### Passo 1: Instalar o Python e o FFmpeg

O Whisper depende do Python no Windows e do FFmpeg (um "canivete suíço" de áudio) para processar as ondas sonoras.

A forma mais fácil de instalar tudo é abrir o **Prompt de Comando (CMD)** como Administrador e rodar os comandos abaixo, um por vez:

`winget install Python.Python.3.11`

`winget install Gyan.FFmpeg`

*(Importante: Após a instalação do FFmpeg, é necessário reiniciar o computador para ele entrar na variável de ambiente PATH do Windows).*

### Passo 2: Instalar o Whisper da OpenAI

Após reiniciar o computador, abra o **Prompt de Comando (CMD)** novamente e rode o comando oficial da OpenAI para instalar o motor de transcrição:

`pip install -U openai-whisper`

### Passo 3: Instalar o Ollama

O Ollama é o programa responsável por rodar os modelos de Inteligência Artificial de texto localmente, com muita facilidade. No mesmo Prompt de Comando, digite:

`winget install Ollama.Ollama`

*(Dica: Se o instalador pedir alguma confirmação na tela, basta pressionar Enter ou "Y" para aceitar. Após a instalação, feche e abra o CMD novamente para garantir que o Windows reconheça o comando).*

### Passo 4: Baixar os Modelos Leves de IA (0.5B e 1B)

Com o Ollama instalado, precisamos baixar os "cérebros" da IA. Selecionamos modelos pequenos e muito rápidos, ideais para computadores com menos recursos e que respondem de forma ágil. No CMD, rode os comandos abaixo (aguarde o primeiro terminar antes de rodar o segundo):

Para baixar o Qwen 2.5 (modelo ultra rápido de 0.5 bilhões de parâmetros):
`ollama pull qwen2.5:0.5b`

Para baixar o Llama 3.2 (modelo leve de 1 bilhão de parâmetros da Meta):
`ollama pull llama3.2:1b`

### Passo 5: A Primeira Execução e Tempos de Espera

  * **Para o Whisper:** A primeira vez que você pressionar \<kbd\>NVDA + Z\</kbd\> usando o "Local (Whisper CLI Offline)", ele vai demorar um pouco (pode ser 1 ou 2 minutos), porque o script vai baixar silenciosamente o modelo base de áudio (cerca de 140 MB) para o seu computador. A partir da segunda vez, ele usará o modelo salvo e o áudio será transcrito em questão de segundos\!
  * **Para o Ollama:** O download inicial dos modelos no Passo 4 vai depender da velocidade da sua internet (eles têm entre 400 MB e 1.3 GB). No entanto, uma vez que o download chegue a 100%, eles ficam salvos no seu disco. A partir daí, qualquer consulta feita a esses modelos será processada localmente, garantindo total privacidade e respostas quase instantâneas.

-----

Desenvolvido com precisão técnica e acessibilidade real por **Melhym Quemel**.

**E-mail de Contato:** [mpquemel@gmail.com](mailto:mpquemel@gmail.com)

**Repositório Oficial:** [https://github.com/mpquemel/nvoice](https://github.com/mpquemel/nvoice)

© 2026 Melhym Quemel - Licença GPL v2+