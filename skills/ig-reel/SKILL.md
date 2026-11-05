---
name: ig-reel
description: >-
  Escreve um Reel do Instagram a partir de uma ideia crua: opções de gancho
  tiradas de 26 fórmulas, o roteiro falado, o texto na tela e um roteiro
  cronometrado por blocos, na voz do próprio usuário e com nota antes de
  gravar. Use sempre que o usuário quiser um Reel, um roteiro de vídeo curto,
  um gancho, uma narração, "escreve o roteiro do reel", "faz um reel sobre X",
  "o que eu falo nesse vídeo", "me dá um gancho", ou quando ele vai gravar e
  ainda não tem a primeira frase.
---

# ig-reel

Pega uma ideia crua e transforma num Reel que a pessoa assiste até o fim.

Tem duas ferramentas nesta pasta e as duas rodam de verdade. Use. Não avalie o
gancho no olho e não chute a duração.

```bash
python3 hookscore.py hooks.txt              # ranqueia suas opções de gancho
python3 hookscore.py --hook "uma frase"     # dá nota pra um gancho só
python3 beats.py script.txt --target 30     # roteiro cronometrado antes de gravar
```

O `hookscore.py` detecta o idioma de cada gancho sozinho (`--lang auto`, o
padrão). Se um gancho misturar português e inglês e a detecção errar, force com
`--lang pt`. O `beats.py` funciona nos dois idiomas sem opção.

## Antes de escrever

1. Leia `~/.claude/instagram/voice.md` se ele existir. É o perfil de voz do
   usuário: como ele fala na câmera, o que ele nunca diz, com quem ele está
   falando. Se não existir, peça **três reels dele mesmo**, transcreva ou leia,
   deduza a voz e escreva o arquivo. Roteiro na voz errada não serve pra nada,
   porque ele vai ter que falar aquilo em voz alta.
2. Leia `hooks.json` nesta pasta. São 26 fórmulas, cada uma com um modelo, um
   exemplo preenchido, a versão pra tela, pra que serve e como costuma ser
   estragada. Quatro delas estão lá porque apareciam o tempo todo em ganchos
   reais, não pra fechar um padrão bonito. Para conteúdo em português, use o
   bloco `pt` de cada fórmula (nome, modelo, exemplo, versão pra tela) e a
   lista `rules_pt`. Os campos de fora do `pt` são a versão original em inglês.
3. Se a ideia estiver rala, não encha linguiça. Faça uma pergunta só, com tudo
   junto: o que aconteceu, com quem, e quanto custou ou quanto rendeu. Um Reel
   precisa de uma coisa específica e verdadeira. Consiga isso antes de escrever.
4. Se `~/.claude/instagram/swipe.md` existir, leia. Quem escreve esse arquivo é
   o `/ig-viral`, e ele é a prova do próprio usuário sobre quais fórmulas estão
   funcionando no nicho dele agora. Isso vale mais que os padrões deste arquivo.

## A estrutura

Um Reel se decide nos dois primeiros segundos e se segura nos cinco seguintes.

```
0:00 - 0:02   GANCHO      a afirmação. Fala e texto na tela, escritos
                          separados. Movimento no primeiro frame, não um rosto parado.
0:02 - 0:07   O RISCO     por que isso importa pra quem está assistindo. Uma frase.
0:07 - ...    O MEIO      uma ideia por bloco, e o enquadramento muda a cada bloco.
ÚLTIMOS 3s    A ENTREGA   entrega o que o gancho prometeu, depois o pedido único.
ÚLTIMA FRASE  O LOOP      repete uma palavra do gancho pro replay encaixar limpo.
```

Duração: de 15 a 45 segundos é a faixa que funciona. Reel vai até 3 minutos e
quase ninguém deveria usar isso. Abaixo de 7 segundos a contagem de loops
infla e nada mais melhora.

## O processo

**1. Escolha três ganchos, não um.** Passe a ideia pelo `hooks.json`, escolha
três fórmulas que encaixem de verdade e escreva a fala e o texto de tela de
cada uma. Fórmulas diferentes, não três versões da mesma.

**2. Dê nota.** Coloque as três falas num arquivo, uma por linha, e rode o
`hookscore.py`. Mostre o ranking pro usuário. Se o primeiro colocado ficou
abaixo de 50, você ainda não tem o gancho, e nenhuma edição resolve isso.

**3. Escreva o roteiro** em cima do gancho vencedor. Linguagem falada, do
jeito que o usuário fala de verdade. "Tá", "pra", "a gente". Frases curtas.
Nenhuma frase que ele precise ensaiar.

**4. Cronometre.** Rode `beats.py script.txt --target {duração}`. Corrija todo
alerta: gancho passando de 3 segundos, qualquer bloco acima de 4 segundos, uma
sequência de blocos sem nada concreto, falta de loop. Rode de novo até sair
limpo. O cabeçalho da saída fica assim, e cada bloco vem marcado como GANCHO,
MEIO ou CTA:

```
ROTEIRO CRONOMETRADO  ·  73 palavras  ·  ~26.6s a 165 ppm  ·  alvo 30.0s
```

**5. Humanize.** Passe o roteiro pelo `/ig-human` antes de mostrar. Frase com
cara de texto escrito fica óbvia no momento em que alguém fala em voz alta.

**6. Entregue o bloco.** O roteiro num bloco de código, o texto de tela numa
lista separada com os tempos, e depois:

```
REEL PRONTO
gancho:     #3 Ninguém Te Conta, nota 86 FORTE
duração:    28.4s em 9 blocos a 165 ppm
na tela:    6 cartelas
humanizer:  4 marcas removidas, nota humana 81 APROVADO
legenda:    rode /ig-caption em seguida

Responda "sim" pra registrar, ou me diga o que mudar.
```

**7. Nunca publique.** Esta skill entrega um roteiro. O usuário grava e posta.
No "sim", acrescente em `~/.claude/instagram/log.md` a data, a fórmula de
gancho usada e a primeira frase, pra que o `/ig-audit` tenha histórico depois.

## Texto na tela é um roteiro à parte

Escreva separado, sempre. Ele é lido antes de ser ouvido.

- **Seis palavras ou menos por cartela.** Quem lê está com o celular na mão,
  de longe, e ainda não está prestando atenção no áudio.
- **A cartela do gancho aparece no frame 1**, não depois de um silêncio.
- **Fique dentro da área segura.** Num frame de 1080x1920, nada acima de y=230
  ou abaixo de y=1440, e deixe livres os 230 pixels da direita. A interface
  fica por cima de tudo que está fora dessa caixa: a legenda, a barra de
  botões, a faixa do áudio.
- **Nunca coloque o gancho onde fica a legenda.** É a parte de baixo do frame
  e ela fica coberta.
- **Legenda embutida no meio do vídeo.** A maioria assiste sem som primeiro.

## Regras que fazem a diferença

- **Uma ideia por Reel.** Se o roteiro tem duas, são dois Reels. Fale isso.
- **Número em vez de adjetivo.** "R$ 4.200" ganha de "muito dinheiro". Se o
  usuário não deu o número, peça, em vez de escrever em volta do buraco.
- **Corte a introdução.** Sem "oi, gente", sem "nesse vídeo", sem nome, sem
  vinheta de logo. O vídeo começa na frase que você normalmente só falaria no
  sexto segundo.
- **Mude o enquadramento a cada bloco.** Plano parado por 8 segundos é onde as
  pessoas saem, e o `beats.py` vai apontar isso.
- **Um pedido no final.** Comentar uma palavra, salvar ou seguir. Um só.
- **Nunca invente.** Nada de métrica, cliente, faturamento ou resultado
  inventado no nome do usuário, nem como provisório. Se precisa de um número e
  ele não é conhecido, deixe `{{seu número}}` no roteiro e avise.
- **Não escreva roteiro em cima de um áudio em alta que o usuário não pode
  usar.** Se a ideia precisa da voz dele, diga isso.

## Exemplo

```
/ig-reel a gente cortou o tempo de proposta de 5 horas pra 20 minutos com um modelo
```

```
GANCHOS  (com nota)
  86  FORTE  #5  Tempo Encolhido     "Proposta me tomava cinco horas. Hoje são vinte minutos."
                                     na tela: 5 HORAS -> 20 MIN
  71  FORTE  #1  Confissão de Custo  "Cobrei quatro horas por semana só de formatação. Por dois anos."
                                     na tela: 2 ANOS JOGADOS FORA
  54  OK     #9  Rouba Isso          "Rouba o modelo de proposta que fez isso."
                                     na tela: ROUBA ISSO

Vou de #5: a proporção é crível, dá pra ler de uma olhada na tela,
e o número é seu.
```
