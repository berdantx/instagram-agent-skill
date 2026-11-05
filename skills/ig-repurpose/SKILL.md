---
name: ig-repurpose
description: >-
  Transforma um conteúdo longo (vídeo do YouTube, podcast, live, newsletter,
  post de blog, call com cliente, aula do lançamento) numa semana de reels e
  carrosséis. Use quando o usuário disser "reaproveita isso", "transforma isso
  em reels", "corta essa live", "tenho um vídeo/podcast/transcrição", "picota
  esse conteúdo", ou colar algo longo e quiser levar pro Instagram.
---

# ig-repurpose

Um conteúdo longo bom tem de quatro a seis posts dentro. A maioria das pessoas
tira um e joga o resto fora.

## Entrada

Uma transcrição, um artigo, uma newsletter, um roteiro, um resumo de call, uma
live. Se o usuário mandar um link e esta sessão tiver ferramenta de
transcrição, use; se não, peça pra ele colar. Leia tudo antes de extrair
qualquer coisa.

Se a fonte for um vídeo do próprio usuário, peça o arquivo também. Um Reel
feito com as imagens dele ganha de um feito com as palavras dele lidas de novo.

## Extraia, não resuma

Resumo de vídeo não é Reel. Ninguém quer o resumo. Passe pelo conteúdo e tire
as coisas que se sustentam sozinhas:

| extração | o que é |
| --- | --- |
| **Afirmações** | toda frase que começaria uma discussão |
| **Números** | todo valor, custo, duração, porcentagem |
| **Histórias** | todo momento com uma pessoa, uma cena e um custo |
| **Mecanismos** | todo "o jeito que isso funciona de verdade é..." |
| **Erros** | toda admissão de algo que deu errado |
| **Frases** | toda frase que já dá pra citar do jeito que está |

Liste o que encontrou, com as contagens, antes de escrever qualquer coisa. Se o
conteúdo render menos de quatro itens, ele é fraco, e quatro posts espremidos
dele vão sair fracos também. Diga isso.

## Depois escolha o formato de cada extração

Nem tudo é Reel.

- **Afirmação, erro, história** viram Reel. Precisam de voz e de rosto.
- **Mecanismo, lista numerada** viram carrossel. Precisam ser relidos.
- **Uma frase citável** vira um quadro de story, não um post.

## Depois monte a semana

Cada extração vira um post, e cada post se sustenta completamente sozinho. Quem
assiste não viu a fonte e nunca vai ver. Nunca escreva "como eu falei no meu
último vídeo". O post é a coisa.

Atribua uma fórmula de gancho do `ig-reel/hooks.json` pra cada um e varie.
Cinco posts da mesma fonte com o mesmo formato de gancho parecem fábrica de
conteúdo, porque são.

Se a fonte é vídeo do próprio usuário, **use as imagens de verdade**. O trecho
em que ele disse a coisa, com a reação real nele, ganha de uma regravação
sempre. Corte na frase, não na respiração.

Ordene a semana assim: a afirmação mais forte primeiro, a história no meio da
semana, e o mecanismo por último, quando quem gostou dos anteriores já está
esperando por ele.

## Saída

```
FONTE: "Por que a gente matou a call de diagnóstico" (podcast de 42 min, 8.900 palavras)

ENCONTREI  5 afirmações, 9 números, 3 histórias, 4 mecanismos, 2 erros, 7 frases citáveis

SEMANA
TER  REEL       #2  Comando Negativo          Para de fazer call de diagnóstico
                                              usa o trecho de 14:20, ele ri no final
QUA  CARROSSEL  legenda Função B              O formulário de 4 perguntas que substituiu a call
SEX  REEL       #21 Começo no Meio da Frase   "...e nove dias depois ele pediu reembolso"
DOM  REEL       #5  Tempo Encolhido           Seis horas por semana de volta, um link apagado

Fala "escreve a de terça" que eu faço o rascunho.
```

Depois, rascunhe sob pedido, um de cada vez, cada um passando pelo `/ig-reel` e
pelo `/ig-human`. Não despeje quatro roteiros prontos de uma vez. Vão sair
todos com a mesma cara e o usuário não vai gravar nenhum.
