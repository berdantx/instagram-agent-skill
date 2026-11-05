---
name: ig-audit
description: >-
  Autópsia do que o usuário já postou: quais reels funcionaram de verdade,
  por quê, e o que parar de fazer. Use quando o usuário colar os insights do
  Instagram ou posts antigos e perguntar "o que tá funcionando", "por que esse
  flopou", "lê minhas métricas", "analisa meu conteúdo", "faz uma auditoria
  do meu perfil", ou quiser saber do que fazer mais.
---

# ig-audit

A única fonte honesta do que funciona pra uma conta é a própria conta. Toda
regra de todo guia de Instagram, inclusive as deste pacote, é um palpite
inicial. Os últimos 30 posts do usuário são a prova.

## Entrada

Peça o que o usuário tiver:

- Insights por post: visualizações, alcance, interações, tempo assistido,
  salvamentos, compartilhamentos, seguidores ganhos e a fatia do alcance que
  veio de não seguidores. Print serve.
- Ou o gráfico de retenção do melhor e do pior reel recente. Esse print
  sozinho vale mais que todo o resto junto.
- Ou só os posts e as contagens de views, o que já basta pra uma primeira
  passada.

Leia também `~/.claude/instagram/log.md` se existir, porque ele registra qual
fórmula de gancho cada post usou.

## O que medir de verdade

View bruta é o número menos útil da tela, porque depende principalmente de
quantas pessoas já seguem a conta. Calcule estes no lugar e mostre a conta:

| métrica | como | o que ela diz |
| --- | --- | --- |
| **Múltiplo fora da curva** | views / mediana de views da própria conta | se foi um acerto de verdade ou um dia normal |
| **Alcance em não seguidores** | % do alcance vindo de quem não segue | se o post viajou ou não |
| **Retenção aos 3s** | quem ainda estava lá aos 3s / quem começou a assistir | se o gancho funcionou. Essa é a nota do gancho. |
| **Tempo médio assistido** | direto dos insights | se o meio funcionou |
| **Envios por alcance** | compartilhamentos / alcance | o sinal mais forte que dá pra conquistar. Um envio é alguém botando o próprio nome naquilo. |
| **Seguidores por alcance** | seguidores ganhos / alcance | se o perfil converteu a atenção |

Ranqueie por múltiplo fora da curva e envios por alcance, não por views. Um
reel com 4.000 views e 90 envios ganhou do que teve 60.000 views e 11.

## Depois ache o padrão

Com os cinco melhores e os cinco piores lado a lado, procure o que separa os
dois grupos, e esteja disposto a concluir algo que o usuário não vai gostar
de ouvir:

- **Retenção aos 3 segundos.** Se os de cima e os de baixo diferem aqui, é o
  gancho e mais nada, e todo o resto é distração.
- **Fórmula de gancho.** Quais ids do `ig-reel/hooks.json` estão nos cinco
  melhores?
- **Formato.** Reel, carrossel, imagem única.
- **Duração.** Agrupe em menos de 15s, 15 a 30s, 30 a 60s, mais de 60s.
- **Tema.**
- **Se o usuário respondeu os comentários na primeira hora.**
- **Dia e horário.** Olhe isso **por último** e só se o resto não mostrar
  nada. Quase nunca é a causa, e é justamente onde as pessoas querem que seja.

Escreva o achado como uma afirmação com a prova do lado, e diga o grau de
confiança. Com 30 posts dá pra ver um padrão. Com 6 não dá, e dizer isso é
melhor do que inventar um.

## A distinção que economiza meses

**Um reel que tem views e não traz seguidor não é um reel que falhou, é um
problema de perfil.** Um reel sem views é problema de gancho. Separe os dois
antes de recomendar qualquer coisa. Se o alcance em não seguidores está alto
e os seguidores por alcance estão baixos, pare de reescrever gancho e vá pro
`/ig-profile`.

## Saída

```
AUDITORIA  ·  31 posts  ·  12 jun a 5 set  ·  mediana de views 4.100

TOP 5 POR MÚLTIPLO FORA DA CURVA
  18.2x  #3  Ninguém Te Conta     74.600 views  62% não seguidores  ret@3s 71%  128 envios
   6.4x  #1  Confissão de Custo   26.300 views  48% não seguidores  ret@3s 64%   71 envios
  ...

PIORES 5
   0.3x  #11 Lista Com Favorito    1.200 views   9% não seguidores  ret@3s 31%    2 envios
  ...

O QUE OS DADOS DIZEM
1. A retenção aos 3 segundos é a história inteira. Os cinco melhores têm média
   de 66%, os cinco piores, 33%. Tudo o mais que te preocupa vem depois dos
   dois primeiros segundos.
2. Os posts em que quem se queimou foi você: média de 8.1x contra 0.9x de todo
   o resto. n=5. É o sinal mais forte aqui e não tem nem comparação.
3. Lista de ferramentas dá view e mais nada. Alcance alto, zero envio, zero
   seguidor. Três dos seus cinco piores.
4. Dia da semana não mostra nada. As médias de terça e de sexta estão dentro
   do ruído. Pare de otimizar isso.

PARE: listas.
FAÇA MAIS: os que têm um custo que você pagou e um número junto.
```

Depois passe as conclusões pro `/ig-plan`, pra que a próxima semana seja
montada em cima da prova do próprio usuário e não dos padrões, e pro
`/ig-viral`, pra que o swipe file seja filtrado pelas fórmulas que funcionam
pra esta conta especificamente.
