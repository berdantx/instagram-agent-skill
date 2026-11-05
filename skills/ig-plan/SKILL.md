---
name: ig-plan
description: >-
  Monta a semana no Instagram: o que postar, em qual formato, quando, e com
  quem interagir. Use quando o usuário disser "planeja minha semana", "o que eu
  posto essa semana", "o que eu posto", "calendário de conteúdo", "não tenho
  nada pra postar", "monta meu cronograma", ou quiser uma grade de postagem e
  uma lista de perfis pra engajar.
---

# ig-plan

A sala de controle. Todo o resto do pacote executa; esta skill decide o que vai
ser executado. Rode uma vez por semana, sempre no mesmo dia.

## Entrada

Se `~/.claude/instagram/voice.md`, `swipe.md` e `log.md` existirem, leia. O
swipe é a prova do próprio usuário, tirada do `/ig-viral`, sobre quais fórmulas
estão funcionando no nicho dele agora, e vale mais que qualquer coisa escrita
aqui. O log impede o plano de repetir um tema das últimas duas semanas.

Se não existirem, pergunte quatro coisas e anote:

1. O que o usuário vende, e pra quem.
2. Os três ou quatro temas pelos quais ele quer ser conhecido.
3. O que aconteceu de verdade essa semana: uma call com cliente, um número, um
   erro, uma coisa que ele construiu, uma discussão que teve. É daí que saem os
   posts.
4. Dez perfis onde vale a pena ser visto.

## O que postar

Quatro a cinco posts por semana, e pelo menos três deles Reels. Reels são o
único formato do Instagram que chega com consistência em quem não segue a
conta. Carrossel aprofunda com quem já segue. Story é diário e é planejado à
parte.

Misture ao longo da semana, nunca dois do mesmo tipo em seguida:

| tipo | frequência | função |
| --- | --- | --- |
| **Prova** | 1 por semana | algo que aconteceu, com um número. Reel. |
| **Ensino** | 1 a 2 por semana | uma coisa que a pessoa pode fazer hoje. Reel ou carrossel. |
| **Opinião** | 1 por semana | uma posição que pode te fazer perder seguidor. Reel. |
| **História** | 1 a cada duas semanas | uma cena com um custo. Reel. |
| **Oferta** | 1 a cada duas semanas | o que você vende, dito sem rodeio e sem pedir desculpa. Carrossel ou stories. |

Pra cada espaço da grade, entregue: o tema, o ângulo específico tirado do que
aconteceu de verdade na semana, o formato, e o número da fórmula de gancho do
`ig-reel/hooks.json`. Não é um assunto, é um ângulo. "IA" não é plano. "A
proposta que a gente perdeu porque o rascunho tinha um travessão" é um Reel.

## Quando postar

Poste quando o público do usuário está acordado e fora do trabalho. Pra maioria
dos públicos de consumo isso é no começo da noite, no horário local; pra
público de negócios, no começo da manhã.

Mas diga com todas as letras: **o horário importa muito menos que os dois
primeiros segundos.** O Instagram continua mostrando um Reel por dias se ele
performa, e enterra um bem cronometrado que não performa. Se o usuário está
otimizando horário antes de o gancho funcionar, ele está polindo a coisa errada,
e você deve falar isso.

Use o fuso horário do público, não o do usuário, se forem diferentes.

## A rodada de engajamento, que não é opcional

20 minutos por dia, antes de postar, não depois. Monte uma lista de 10:

- **5 de alcance**: perfis com o público que o usuário quer, onde um bom
  comentário é visto. Comente cedo, antes de a conversa ter 200 respostas.
- **3 pares**: mesmo tamanho, mesma área. É o grupo que retribui.
- **2 compradores**: gente que poderia comprar de verdade. Comente por semanas
  antes de qualquer DM, e nunca venda num comentário.

Passe a lista pro `/ig-comment`.

## Saída

```
SEMANA DE 15/09

SEG  só engajamento  (20 min, lista abaixo)
TER  19h30  REEL       PROVA     #5  Tempo Encolhido     - proposta de 5h pra 20 min
QUA  só stories + engajamento
QUI  19h00  CARROSSEL  ENSINO    legenda Função B        - a cláusula destrinchada em 4 slides
SEX  19h30  REEL       OPINIÃO   #2  Comando Negativo    - para de fazer call de diagnóstico
SÁB  -
DOM  18h00  REEL       HISTÓRIA  #21 Começo no Meio da Frase - o e-mail do reembolso

STORIES  todo dia, 3 a 5 quadros, caixinha de perguntas na quinta.

ENGAJAR  (5 alcance / 3 pares / 2 compradores)
  ...

Fala "escreve a de terça" que eu faço o rascunho.
```

Salve o plano em `~/.claude/instagram/plan.md` pra que as outras skills possam
ler. Nada é agendado nem publicado em lugar nenhum. Isso é um plano, e quem
executa é o usuário.
