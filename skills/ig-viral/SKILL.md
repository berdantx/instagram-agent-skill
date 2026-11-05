---
name: ig-viral
description: >-
  Vai atrás dos reels que estão funcionando de verdade agora no nicho do
  usuário, ranqueia cada um por quanto ele superou a própria conta, nomeia a
  fórmula de gancho que cada um usou e transforma isso num swipe file pronto
  pra gravar. Use quando o usuário disser "acha uns vídeos virais", "o que tá
  funcionando agora", "o que a galera tá postando no meu nicho", "faz
  engenharia reversa desse perfil", "monta um swipe file pra mim", "por que
  esse reel tá bombando", ou perguntar o que gravar em seguida sem ter dado
  nenhum pra responder.
---

# ig-viral

A skill de pesquisa. Todo o resto deste pacote escreve; esta aqui vai lá e
olha. Rode uma vez por mês, não todo dia. Fórmula dura uma temporada.

Tem uma ferramenta nesta pasta e ela roda:

```bash
python3 swipe.py captured.tsv --out ~/.claude/instagram/swipe.md
```

## A ideia que faz isso valer a pena

**View bruta não é prova.** Uma conta com dois milhões de seguidores fazendo
400 mil views teve uma terça-feira fraca. Uma conta com quatro mil seguidores
fazendo 400 mil views achou alguma coisa, e essa coisa dá pra copiar.

Então tudo aqui é ranqueado pelo **múltiplo fora da curva**: views divididas
pela mediana recente daquela mesma conta. Acima de 3x é sinal. Abaixo de 1,5x
é o dia normal daquela conta e não te ensina nada, por maior que o número
pareça.

Junte contas **com até umas 10x o tamanho do usuário**. Uma fórmula que
funciona com 2 milhões de seguidores muitas vezes funciona justamente porque
a conta tem 2 milhões de seguidores.

## Passo 1: escolha as contas

Peça ao usuário de 6 a 12 contas, ou proponha e peça aprovação:

- **4 diretas**: mesmo nicho, mesma oferta, um pouco à frente.
- **4 vizinhas**: nicho diferente, mesmo público. É daqui que os formatos são
  emprestados antes de alguém do nicho usar.
- **2 a 4 gigantes**: contas bem maiores, só pelo formato, nunca pela
  frequência ou pelo tom.

Peça também pra ele abrir a **coleção de Salvos** dele. É o acervo mais rápido
e mais relevante que existe, e já vem filtrado pelo gosto dele.

## Passo 2: vá lá olhar

Use a ferramenta de navegação que esta sessão tiver de verdade: um navegador
embutido, uma extensão conectada ao Chrome do próprio usuário ou uma
ferramenta de uso do computador. Não existe API pra isso e nem precisa,
porque o volume é pequeno o bastante pra ler.

**Regras inegociáveis:**

- **Nunca faça login no Instagram pelo usuário e nunca peça senha.** Se uma
  página pede login, quem já está logado é o usuário. Opere o navegador dele
  com ele presente, ou peça pra ele colar as informações.
- **Isso é leitura, não raspagem.** Dez contas, uma dúzia de reels cada, em
  velocidade de gente. Coleta automatizada em volume viola os Termos de Uso do
  Instagram e faz a conta levar bloqueio de ação. Não monte um crawler, não use
  serviço de scraping e não deixe isso rodando em segundo plano.
- **Copie a fórmula, nunca o vídeo.** O formato do gancho, a estrutura, a
  duração, o ritmo dos cortes. Não o roteiro, não a voz, não a edição. Atribua
  cada linha do swipe file à conta de onde ela veio.

**O que anotar de cada reel**, nas palavras do próprio criador:

| campo | observação |
| --- | --- |
| conta | @ |
| seguidores | do perfil |
| mediana | olhe os últimos 12 reels e pegue a contagem de views do meio |
| views | deste reel |
| gancho | a primeira frase, falada ou na tela, palavra por palavra, inclusive com erro de português |
| na tela | a primeira cartela de texto, se for diferente |
| duração | segundos |
| cta | o que ele pediu no final |

A mediana é a mais importante. Sem ela você volta a ranquear por número de
seguidores, que é exatamente o que esta skill existe pra impedir.

**Quando o Instagram não mostra o suficiente:** a mesma gramática de gancho
roda no YouTube Shorts, onde contagem de views e transcrição são públicas e
não tem login no meio. É um segundo acervo legítimo, e lá fica mais fácil
pegar o gancho falado:

```bash
# contagem de views dos shorts de um canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@HANDLE/shorts" > channel.json

# a primeira frase falada de um short, pelas legendas automáticas
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "en.*" \
  --sub-format json3 -o hook "https://www.youtube.com/watch?v=VIDEO_ID"
```

Pra canais brasileiros, troque `--sub-langs "en.*"` por `--sub-langs "pt.*"`.
Se o canal mistura os dois idiomas, `--sub-langs "pt.*,en.*"` traz os dois.

Pegue toda palavra da legenda com marcação de tempo abaixo de 3.0 segundos.
Esse é o gancho, do jeito que foi dito, não do jeito que foi escrito.

## Passo 3: ranqueie

Preencha um arquivo separado por tabulação, com uma linha de cabeçalho, e rode
o script. Os nomes de coluna podem ser em português (`conta`, `seguidores`,
`mediana`, `views`, `gancho`) ou em inglês (`account`, `followers`, `median`,
`views`, `hook`):

```
conta	seguidores	mediana	views	gancho
@alguem	48000	11000	412000	ninguém te conta que seus primeiros 30 reels são pra flopar
```

```bash
python3 swipe.py captured.tsv --out ~/.claude/instagram/swipe.md
```

Ele calcula o múltiplo fora da curva, nomeia a fórmula do gancho usando as
mesmas 26 fórmulas com que o `/ig-reel` escreve, dá nota pra cada gancho com o
`hookscore.py` e mostra o que separa o terço de cima do terço de baixo.

## Passo 4: diga o que significa, com cuidado

Reporte três coisas e mais nada:

1. **Quais fórmulas aparecem acima do esperado** no terço de cima, com
   contagem. Duas fórmulas aparecendo quatro vezes cada em seis contas é um
   achado. Uma aparecendo duas vezes não é.
2. **O que o terço de cima tem em comum na estrutura** que o terço de baixo
   não tem: tamanho do gancho, se a entrega é visual, se o primeiro frame tem
   movimento, onde fica o pedido.
3. **As linhas não classificadas.** Todo gancho que o classificador não
   conseguiu nomear (o script marca como "não classificado") é ruído ou é uma
   fórmula que ainda não está no `hooks.json`. Leia uma por uma. É a coluna
   mais valiosa da saída e é por isso que o script mostra a contagem.

Depois diga o tamanho da amostra e a confiança com todas as letras. Quarenta
reels em seis contas sustentam uma afirmação. Doze não, e dizer isso é a
diferença entre pesquisa e horóscopo.

## Passo 5: transforme em algo pra gravar

Para as três fórmulas do topo, escreva **a versão do usuário**: a história
dele, o número dele, no formato que está funcionando. Passe cada uma pro
`/ig-reel` com o id da fórmula já escolhido.

Nunca devolva "faz um reel igual a esse". Devolva uma frase de gancho que ele
consiga falar amanhã.

## Saída

```
SWIPE FILE  ·  38 reels  ·  7 contas  ·  base: mediana da conta

FORA DA CURVA (acima de 3x)
  38.4x  gancho 86  #3  Ninguém Te Conta   @conta_a    412.000  (mediana 10.700)
  11.2x  gancho 79  #9  Rouba Isso         @conta_c    180.000  (mediana 16.100)
  ...

O QUE ESTÁ FUNCIONANDO NESTE LOTE
  #3 Ninguém Te Conta   x5 no terço de cima, 0 no de baixo
  #2 Comando Negativo   x4
  tamanho mediano do gancho 8 palavras em cima, 19 embaixo

NÃO CLASSIFICADOS (6)
  Dois deles têm o mesmo formato e ele não está no hooks.json: um gancho que
  abre lendo em voz alta o comentário de outra pessoa. Vale adicionar.

SUA VERSÃO
  #3  "Ninguém te conta que as primeiras 20 propostas são pra perder."
  ...
```

Escreva o swipe file em `~/.claude/instagram/swipe.md`. O `/ig-reel` e o
`/ig-plan` leem esse arquivo, e é essa a graça: depois que isto roda uma vez,
o resto do pacote passa a trabalhar com a prova do próprio usuário em vez dos
padrões.

Esta skill não posta, não segue, não curte e não manda mensagem pra ninguém.
Ela lê.
