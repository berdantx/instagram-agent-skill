---
name: ig-profile
description: >-
  Dá nota de 0 a 100 pra um perfil do Instagram numa rubrica de 12 itens e
  reescreve as partes que perdem ponto: campo de nome, bio, link, destaques,
  os três fixados, grade. Use quando o usuário disser "otimiza meu perfil",
  "arruma minha bio", "dá uma nota pro meu Instagram", "por que ninguém me
  segue", "minha bio tá boa?", ou colar o perfil e perguntar como ele soa.
---

# ig-profile

Quase todo mundo otimiza a coisa errada aqui. O perfil não é uma vitrine onde
as pessoas passeiam. É uma **tela de decisão**, onde a pessoa chega vinda de
um reel, e ele tem uns três segundos pra responder uma pergunta: tem mais
disso aqui, e isso é pra mim?

## Entrada

Peça pro usuário colar ou mandar print de: campo de nome, @, bio, pra onde o
link aponta, nomes dos destaques, o que está fixado e as capas dos nove
primeiros posts da grade. Um print do topo do perfil mais as duas primeiras
linhas da grade já bastam pra uma primeira passada.

Não faça login no Instagram pelo usuário.

## Dê a nota

Leia o `rubric.json` nesta pasta. Doze itens, 100 pontos, cada um com como é
a nota máxima e como ele costuma falhar. Dê nota pra todos os itens, mostre a
tabela, dê o total. Seja honesto. A maioria dos perfis fica entre 30 e 49 na
primeira passada, e nota generosa não serve pra nada.

```
NOTA DO PERFIL  38/100

  campo de nome       2/12   só o nome, nenhuma palavra que alguém busca
  bio, linha um       3/12   três substantivos e um emoji de café
  três fixados        0/10   nada fixado
  destaques           2/8    "Aleatório", "Vida", "2023"
  leitura da grade    4/8    seis das nove capas são um rosto no meio da fala
  ...
```

## Depois reescreva, nesta ordem

Corrija do item que mais perdeu ponto pro que menos perdeu. Não reescreva
tudo de uma vez: o usuário tem que ir lá e mudar cada uma dessas coisas.

**1. O campo de nome (30 caracteres).** A linha em negrito embaixo da foto,
não o @. É o campo que a busca do Instagram usa pra encontrar a conta, e a
maioria coloca só um nome nele e mais nada. Formato que funciona:
`{Nome} | {o que você faz, nas palavras que as pessoas buscam}`. Dê três
opções.

**2. A primeira linha da bio.** Pra quem é e o que muda pra essa pessoa. Não
um cargo, não adjetivos, não uma lista de identidades separadas por barra. O
resto dos 150 caracteres leva uma prova ou uma oferta simples.

**3. Os três fixados.** Três espaços, três trabalhos diferentes: a melhor
prova, a explicação mais clara da oferta, a melhor apresentação da pessoa. É
a correção que mais rende no perfil inteiro e leva quatro toques. Uma grade
sem nada fixado mostra o que foi postado por último, o que é cara ou coroa.

**4. Destaques.** De quatro a seis, com o nome das perguntas que um comprador
faz: Preço, Resultados, Como funciona, Sobre. Não "Aleatório". Apague o resto.

**5. O link.** Um destino que bate com o que a bio acabou de prometer. Dá pra
colocar cinco; dois já viram um cardápio, e cardápio converte pior que uma
porta.

**6. Capas da grade.** As nove primeiras no tamanho de miniatura. Capa de
reel se escolhe, não fica sendo o primeiro frame que veio. Quatro palavras de
texto na capa fazem a grade ser lida de uma olhada.

## Saída

Tabela de notas, depois as reescritas como blocos prontos pra copiar, na
ordem do que corrigir primeiro, cada uma passada pelo `/ig-human`. Dê a nota
de novo no final e mostre a diferença com honestidade. Se a reescrita chegou
a 84 e não a 98, diga 84, e diga o que falta pro resto, que normalmente é uma
grade, o hábito de postar story e um post fixado que ainda não existe. Nada
disso é reescrita.

Esta skill não salva nada no Instagram. O usuário edita cada campo.
