# Instagram agent skill, em português

Treze skills do Claude para tocar uma conta de Instagram. De graça, MIT, sem
cadastro, sem chave de API, nada para conectar.

Esta é a adaptação para português do Brasil do
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
do Jake Schincariol. As skills foram traduzidas e adaptadas para o mercado
brasileiro, e as cinco ferramentas em Python agora entendem português: o
humanizador tem um léxico de clichês em PT, o avaliador de gancho reconhece
número falado ("dezoito mil reais"), saudação ("oi gente") e preâmbulo ("neste
vídeo eu vou te mostrar"), e o classificador de fórmulas tem regex escritos
para fala brasileira. Texto em inglês continua funcionando: o idioma é
detectado sozinho.

Uma das skills escreve seus Reels a partir de 26 fórmulas de gancho e dá nota
ao gancho antes de você gastar um take nele. Outra vai atrás dos reels que
estão funcionando no seu nicho e ranqueia cada um pelo quanto ele superou a
própria conta. Outra escreve a legenda e mostra exatamente o que o feed exibe
antes do "... mais". Outra dá nota ao seu perfil de 0 a 100 e reescreve o que
perdeu ponto. Outra planeja a semana.

E uma é o humanizador, que é o motivo de as outras serem usáveis. Ele tira os
travessões, o vocabulário de IA e os caracteres invisíveis de um rascunho, e
depois dá nota ao que sobrou num painel de cinco checagens antes de você ver.

**Nada é postado até você dizer sim.** Essas skills escrevem. Você posta.

## Instalação

Cole isto no Claude:

```
https://github.com/berdantx/instagram-agent-skill

Instala essa skill e confirma que o /ig-reel funciona.
```

Ou faça você mesmo, no Claude Code:

```bash
git clone https://github.com/berdantx/instagram-agent-skill.git
cp -r instagram-agent-skill/skills/ig-* ~/.claude/skills/
```

Ou como plugin:

```
/plugin marketplace add berdantx/instagram-agent-skill
/plugin install instagram-agent
```

Para usar só num projeto, copie as mesmas pastas para o `.claude/skills/` do
repositório. Sem Claude Code? Cole qualquer `SKILL.md` no começo de uma
conversa e ele funciona como um modo. Você perde as cinco ferramentas em
Python, que são boa parte da graça do `/ig-reel` e do `/ig-human`, mas o resto
funciona.

Depois, gaste dez minutos no `templates/voice.md`. Copie para
`~/.claude/instagram/voice.md` e preencha, ou mande três reels seus para o
Claude e diga "escreve meu voice.md a partir desses". Todas as skills leem esse
arquivo. Aqui ele pesa mais do que em outras redes, porque você vai ter que
falar as palavras em voz alta.

## As treze

| comando | o que faz |
| --- | --- |
| `/ig-reel` | Uma ideia vira um Reel. Três ganchos a partir de [26 fórmulas](skills/ig-reel/hooks.json), com nota, depois o roteiro, o texto na tela e um roteiro cronometrado. |
| `/ig-viral` | Vai atrás do que está funcionando no seu nicho, ranqueia pelo múltiplo sobre a mediana de cada conta, dá nome à fórmula e escreve o swipe file. |
| `/ig-caption` | A legenda, revisada. Mostra os 125 caracteres que o feed exibe antes do toque. |
| `/ig-carousel` | Carrossel. A capa que faz arrastar, o texto de cada slide e os arquivos 1080x1350. |
| `/ig-story` | A sequência de stories do dia, qual figurinha faz qual trabalho, e o funil de DM que começa com a pessoa se mexendo primeiro. |
| `/ig-profile` | Dá nota ao perfil numa [rubrica de 12 itens](skills/ig-profile/rubric.json), de 0 a 100, e reescreve na ordem do que mais perdeu ponto. |
| `/ig-plan` | A semana. O que postar, em qual formato, quando, e as 10 contas para engajar. |
| `/ig-human` | O humanizador. Dois scripts que rodam de verdade. Veja abaixo. |
| `/ig-comment` | Comentários em posts dos outros. Nove tipos, escolhidos pelo que o post realmente é. Nunca "🔥🔥🔥". |
| `/ig-reply` | Os comentários do seu próprio post. Separa em palavra-chave / lead / substância / pergunta / apoio / ruído e responde nessa ordem. |
| `/ig-dm` | A entrega da palavra-chave, a primeira mensagem, a proposta de collab e os dois follow-ups. Dois. |
| `/ig-repurpose` | Um vídeo, podcast ou newsletter vira uma semana de reels e carrosséis que se sustentam sozinhos. |
| `/ig-audit` | Autópsia do que você já postou. Ranqueia por múltiplo fora da curva e envios por alcance, não por views. |

## As cinco ferramentas que rodam de verdade

Sem dependências, sem rede, nada enviado. Rodam na sua máquina, no seu texto.
Todas detectam o idioma sozinhas (dá para forçar com `--lang pt` ou
`--lang en` no hookscore, no humanize e no detect) e respondem em português.

### Ganchos

```bash
python3 hookscore.py ganchos.txt            # ranqueia suas opções
python3 beats.py roteiro.txt --target 30    # cronometra antes de gravar
```

```
RANKING DE GANCHOS
==============================================================================
->  87.0 FORTE   Ninguém te conta que seus primeiros 30 reels vão flopar
        ponto fraco: ESPECIFICIDADE (75)
    64.8 OK      Perdi R$ 18 mil por causa de uma cláusula que faltou no con...
        ponto fraco: ALVO (35)
    18.4 FRACO   Para de rolar o feed se você quer crescer no Instagram em 2...
        ponto fraco: TENSÃO (20)
        eliminatório: Abre com "para de rolar". Pedir atenção prova que você ainda não ganhou.
        eliminatório: Emoji no gancho. Texto na tela em tamanho de gancho tem espaço para palavras ou para emoji, não os dois.
     9.6 FRACO   Oi gente, hoje eu quero falar sobre estratégia de conteúdo
        ponto fraco: FRENTE (0)
        eliminatório: Saudação. Ninguém abriu o feed para ser cumprimentado.
```

O `beats.py` estima quanto tempo cada linha leva para ser dita, empilha tudo
em minutagem e aponta as quatro coisas que matam um Reel na edição: gancho que
passa de três segundos, batida longa o bastante para a pessoa sair, uma
sequência de linhas sem nada concreto, e falta de loop com a primeira linha.

```
ROTEIRO CRONOMETRADO  ·  55 palavras  ·  ~20.0s a 165 ppm  ·  alvo 30.0s
========================================================================
  0:00.0   2.5s  GANCHO  Perdi R$ 18.000 por causa de um contrato.
  0:02.5   9.1s  MEIO    Aqui está a cláusula exata que eu coloco em todo contrato...
                         ^ 9.1s numa batida só
  0:11.6   2.9s          Seção 4. Pagamento na entrega, não na aprovação.
  0:14.6   2.2s          Aprovação é sentimento. Entrega é data.
  0:16.7   3.3s  CTA     Essa troca de uma palavra vale R$ 18.000 pra mim.
------------------------------------------------------------------------
  - Batida(s) 2 passam de 4s. Divida a linha ou mude o que está na tela dentro dela.
    Quadro parado é onde as pessoas saem.
  - Loop: a última batida repete "R$ 18.000" do gancho. Segunda assistida é alcance de graça.
  - 10.0s abaixo do alvo. Acrescente 27 palavras ou grave curto. Curto costuma estar certo.
```

### A legenda

```bash
python3 caption.py legenda.txt --keywords "contrato de cliente,precificação"
```

O Instagram mostra uns 125 caracteres da legenda no feed e esconde o resto
atrás de um toque. Quase toda legenda que falha, falha ali. Então a primeira
coisa que isto imprime é essa janela, numa caixa, do jeito que um estranho
rolando o feed lê:

```
  O QUE O FEED MOSTRA
  +------------------------------------------------------+
  | Perdi R$ 18 mil por causa de uma cláusula que faltou |
  | no contrato. E eu tinha lido duas vezes antes de     |
  | assinar.                                             |
  |                                                      |
  | Hoje toda pro                                        |
  +-------------------------------------------- ... mais +

  OK    TAMANHO           329 / 2200 caracteres
  OK    PRIMEIRA LINHA    110 caracteres, aparece inteira
  OK    GANCHO CONCRETO   1 número(s) ou nome(s) no trecho visível
  AVISO HASHTAGS          3 tags, 1 delas genéricas (#paravocê). Essas não descrevem nada
  OK    POSIÇÃO DAS TAGS  as tags ficam depois do corte
  OK    LINKS             nenhum link morto no texto
  OK    UM PEDIDO         um pedido: comentar palavra-chave
  OK    EMOJI             0 emoji, 0.0 a cada 100 caracteres
  AVISO TERMOS DE BUSCA   1/2 presentes, 0 no trecho visível. Faltando: precificação
```

Ele aplica o limite atual de hashtags, que é **cinco por post**, não trinta.
O Instagram cortou em 18 de dezembro de 2025. O pedido por palavra-chave só
conta com a palavra em caixa alta ("Comenta CONTRATO"); "comenta aqui embaixo"
não é palavra-chave.

### O humanizador

```bash
python3 humanize.py rascunho.txt --report    # limpa e mostra cada mudança
python3 detect.py rascunho.txt               # dá nota, cinco checagens
python3 detect.py antes.txt depois.txt       # prova a diferença
```

**O que sai automaticamente:**

- **Caracteres invisíveis.** Espaços e junções de largura zero, word joiners,
  hífens condicionais, marcas de ordem de byte, caracteres de tag Unicode,
  separadores invisíveis, espaços rígidos e estreitos. Seu teclado não produz
  isso. Eles sobrevivem ao copiar e colar e são invisíveis em qualquer editor.
- **Tipografia.** Travessão vira vírgula, meia-risca vira hífen, aspas curvas
  viram retas, reticências viram três pontos, e a pontuação solta que isso
  deixa é limpa.
- **O léxico.** Em português ([`slop.pt.json`](skills/ig-human/slop.pt.json)):
  "alavancar", "potencializar", "crucial", "jornada", "no mundo acelerado de
  hoje", "vale ressaltar que", e o bloco de Instagram: "para de rolar o feed",
  "neste vídeo eu vou te mostrar", "segue pra mais conteúdo", "marca alguém que
  precisa ver isso", "o algoritmo ama". Em inglês, o léxico original em
  [`slop.json`](skills/ig-human/slop.json). Os dois foram feitos para ser
  editados: se uma palavra que você usa de verdade está lá, tire.

**O que é apontado em vez de corrigido:** "Não é só X, é Y", trincas, o
preâmbulo de vídeo, lista com emoji de marcador, três palavras gritadas
seguidas, parede de hashtags, isca de seguir ou marcar, frases todas do mesmo
tamanho. Mudar o formato de uma frase pede julgamento, então isso volta para
ser reescrito em vez de ser estragado por um regex.

Rodando numa legenda escrita para ser a pior possível:

```
  VARIAÇÃO       ############............  48.5
  ESPECIFICIDADE ........................   0.0
  CLICHÊS        ........................   0.0    14 clichês, 18.7 a cada 100 palavras
  DIGITAL        ################........  65.7    1 travessão
  VOZ            #######.................  30.6    7 padrões estruturais
  --------------------------------------------------------------
  NOTA HUMANA    ####....................  17.4   SINALIZADO
```

Depois do `humanize.py`, com os padrões estruturais ainda sem reescrever:

```
  NOTA HUMANA    ###########.............  45.2   SINALIZADO   (+27.8)
```

O resto do caminho até APROVADO é reescrever à mão o que ele apontou, e é de
propósito que o script não faz isso.

Em português, a checagem de VOZ conta marcas de fala ("tá", "pra", "né",
"a gente", "cê") no lugar das contrações do inglês, e os pronomes pessoais
("eu", "você", "a gente").

### O swipe file

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

View bruta não é prova. Uma conta de 2 milhões de seguidores fazendo 400 mil
views teve uma terça fraca. Uma conta de 4 mil seguidores fazendo 400 mil
views achou alguma coisa. O `swipe.py` ranqueia pelo múltiplo sobre a mediana
de cada conta, dá nome à fórmula do gancho e mostra o que separa o terço de
cima do terço de baixo. As colunas podem estar em português (conta,
seguidores, mediana, views, gancho) e os números podem vir como "48k", "12
mil" ou "1,2 mi".

```
SWIPE FILE  ·  4 reels  ·  4 contas  ·  base: mediana da conta
==============================================================================
    60.0x  gancho  51  #9  Rouba Isso               @c                 180.000
           "rouba esse follow-up de quatro linhas que eu levei dois anos pra escrever"
    37.5x  gancho  87  #3  Ninguém Te Conta         @a                 412.000
           "ninguém te conta que seus primeiros 30 reels vão flopar"
     2.6x  gancho  83  #1  Confissão de Custo       @d                  52.000
           "esse erro me custou quarenta mil reais no meu primeiro lançamento"
     1.3x  gancho  13  -   não classificado         @b               1.200.000
           "neste vídeo eu vou te mostrar minha rotina da manhã"
```

Se algumas contas vierem com mediana e outras só com seguidores, ele avisa
("base: misto") e marca as linhas calculadas por seguidores, porque os dois
múltiplos não são comparáveis.

## O que foi medido, que é a parte que vale ler

O autor original não quis publicar um avaliador de gancho com base em "parece
certo", então testou. O corpus foram **74 ganchos reais de vídeo curto**: os
três primeiros segundos da legenda automática dos oito melhores e dos oito
piores shorts de cinco canais, com views de 931 a 550.000.

Foram YouTube Shorts e não Reels, porque o Instagram não entrega número de
views que dê para coletar sem entrar na conta de alguém, e raspar isso violaria
os Termos que este repositório diz para não violar. A gramática do gancho é a
mesma e a fonte é pública. É uma limitação real e está dita aqui, não
escondida.

**Três resultados, dois deles desconfortáveis:**

**1. Ele pega gancho ruim bem.** Contra dez ganchos escritos de propósito para
serem ruins, AUC 0,83, e nove dos dez ficaram abaixo da mediana do corpus real.
Se o seu gancho abre com saudação, preâmbulo ou nada concreto, isto avisa.

**2. Ele não escolhe vencedor.** Para separar os acertos de um bom criador dos
erros desse mesmo criador: **AUC 0,56, onde 0,50 é cara ou coroa.** Das cinco
checagens, só ESPECIFICIDADE separou os grupos de forma relevante, por 60
pontos de mediana. TENSÃO e ALVO tiveram a mesma mediana nos dois grupos, ou
seja, nesse corpus não mediram nada.

Então o uso honesto é: matar os ganchos obviamente fracos antes de gravar, e
depois confiar no seu próprio gráfico de retenção. Nada que lê texto consegue
dizer qual de dois ganchos decentes vai viajar, porque isso é decidido pelo seu
rosto, sua edição, seu áudio e para quem o Instagram mostra.

**3. O classificador de fórmulas estava quebrado e foi o teste que pegou.** Os
regex de `match` do `hooks.json` foram escritos a partir dos próprios modelos e
reconheciam **8%** dos ganchos reais. Gente não fala em modelo. Reescrever
contra fala transcrita de verdade levou a **49%**, e cinco fórmulas entraram
no conjunto porque apareciam o tempo todo: Virada Contrária, A Estatística, A
Revelação, O Resultado de Outra Pessoa e O Superlativo. Nos outros 51% ele se
abstém, o que é correto: muito vídeo curto é corte de podcast sem fórmula
nenhuma.

**O que isso significa para a versão em português.** Toda essa medição foi
feita em inglês. Os regex `pt.match`, as listas de palavras em português e o
léxico em PT **não foram validados num corpus real de Reels brasileiros**.
Foram testados contra cerca de 80 ganchos escritos à mão (em
[`tests/hook_cases_pt.py`](tests/hook_cases_pt.py)), o que pega regressão mas
não prova acerto. A expectativa honesta é que a cobertura em fala real seja
menor que nos testes, como foi no inglês. Se você rodar isso num corpus de
verdade (o método está no [`/ig-viral`](skills/ig-viral/SKILL.md), com
`--sub-langs "pt.*"`), os números que saírem dali valem mais do que qualquer
coisa escrita aqui.

## As letras miúdas, que são a parte honesta

**Essas skills não postam no Instagram.** Existe uma API de publicação de
conteúdo de verdade para contas profissionais, e ela pede um app de
desenvolvedor da Meta, uma Página vinculada, um token de longa duração e
revisão do app, que não é algo que uma skill consegue te entregar. Todo o
resto que as pessoas usam para automatizar post, comentário, follow ou DM é
automação de navegador ou ferramenta de terceiro, e as duas violam os
[Termos de Uso do Instagram](https://help.instagram.com/581066165581870) e
levam a conta a bloqueio de ação. Então toda skill aqui termina igual: um
bloco pronto para copiar, e você posta. Isso não é uma limitação colada
depois, é o desenho, e é por isso que a aprovação é de verdade e não uma
configuração.

A única exceção são as respostas automáticas por palavra-chave na DM, que o
Instagram suporta pelas próprias ferramentas e por parceiros aprovados, e que
só disparam depois que a pessoa comenta primeiro. O `/ig-dm` diz onde fica
essa linha.

**O `/ig-viral` lê, não raspa.** Dez contas, uma dúzia de reels cada, em
velocidade humana, com você dirigindo o seu próprio navegador. Ele nunca pede
sua senha e nunca entra como você. Coleta automática em volume é o que leva
conta a ser restringida, e um crawler não é o que isto é.

**As cinco checagens de detecção são heurísticas locais, não APIs de
detector.** São modeladas nos sinais que os detectores públicos olham e rodam
inteiras na sua máquina. Não são GPTZero, Originality, Copyleaks, Winston nem
Turnitin, não chamam esses serviços e não podem prometer o veredito deles.
Corrigir o que elas medem costuma mexer nesses números, porque medem as mesmas
coisas por baixo. Essa é a promessa inteira. Ninguém pode honestamente te
vender "indetectável", e quem vende está te vendendo outra coisa.

**A passada de caracteres invisíveis é real e é estreita.** Ela remove os
caracteres de largura zero e de formatação que aparecem em texto gerado e
sobrevivem ao copiar e colar. É uma digital real e checável. Não é uma
promessa de derrotar um esquema criptográfico de marca d'água, e este
repositório não faz essa promessa.

**Nada aqui inventa.** Nenhuma métrica, cliente ou resultado inventado vai com
o seu nome. Se um rascunho precisa de um número que você não deu, ele volta
com `{{seu número}}` e um aviso, toda vez.

**Número de plataforma envelhece.** O limite de hashtags caiu de 30 para 5 em
dezembro de 2025 enquanto o repositório original era escrito, e o linter tinha
o número velho até alguém checar. Se algo aqui contradiz o que o Instagram está
fazendo quando você ler, o Instagram está certo.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

Só biblioteca padrão. Cobrem os dois idiomas: os números em inglês são os do
README original, para garantir que a adaptação não mudou o comportamento em
inglês.

## Arquivos

```
skills/ig-reel/hooks.json          26 fórmulas de gancho: modelo, exemplo, texto na tela,
                                   pra que serve, como estraga e regex de classificação,
                                   em inglês e no bloco "pt" de cada uma
skills/ig-reel/hookscore.py        o painel de cinco critérios do gancho
skills/ig-reel/beats.py            roteiro para minutagem por batida
skills/ig-caption/caption.py       a prévia do corte do feed e o linter de legenda
skills/ig-human/slop.json          caracteres invisíveis, tipografia e o léxico em inglês
skills/ig-human/slop.pt.json       o léxico e os padrões estruturais em português
skills/ig-human/humanize.py        as três passadas de limpeza
skills/ig-human/detect.py          o painel de cinco checagens
skills/ig-viral/swipe.py           ranking fora da curva e classificação de fórmula
skills/ig-profile/rubric.json      a nota de 100 pontos do perfil
templates/voice.md                 o seu perfil de voz. Preencha primeiro.
tests/                             testes de regressão
```

## Crédito

Criado por Jake Schincariol, [opusjake.ai](https://opusjake.ai), em
[Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill).
Adaptação para português do Brasil por berdantx.

Repositório irmão do original, mesma ideia para outra rede:
[linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill).

## Licença

MIT, mantida do original. Pegue, mude, publique. O aviso de copyright do
[LICENSE](LICENSE) tem que ir junto.
