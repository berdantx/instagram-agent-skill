---
name: ig-carousel
description: >-
  Monta um carrossel de Instagram: a capa que faz a pessoa arrastar, o texto
  slide por slide e os arquivos 1080x1350 prontos pra subir. Use quando o
  usuário disser "carrossel", "monta um carrossel", "transforma isso em
  carrossel", "faz os slides", "post de arrastar pro lado", ou tiver uma ideia
  em formato de lista ou de passo a passo que morreria numa imagem só.
---

# ig-carousel

Carrossel é o formato do feed que mais segura a pessoa olhando, porque arrastar
é uma interação e rolar a tela não é. Ele ainda ganha uma segunda chance: o
Instagram pode mostrar o carrossel de novo, já a partir de um slide mais à
frente, pra quem não interagiu da primeira vez. Então o slide dois também
precisa se sustentar sozinho.

O formato premia uma ideia quebrada em passos. E castiga legenda picotada em
pedaços.

## Quando usar em vez de um Reel

Use carrossel quando a ideia tem **sequência e precisa ser relida**: passos, um
método com partes, um antes e depois, uma lista que vale print. Use Reel quando
a ideia tem movimento, um rosto, ou um resultado que precisa ser visto
acontecendo.

Se a ideia é uma afirmação só, não é nenhum dos dois. Passa pro `/ig-reel` e
fala isso pro usuário.

## Estrutura

De 6 a 10 slides. O limite é 20, e 20 quase sempre vira um livro que ninguém
termina. Com menos de 5, a pessoa nem começa a arrastar.

```
1         CAPA      o gancho. 6 palavras ou menos, num tamanho que dá pra ler
                    na miniatura do feed. Uma linha de promessa embaixo.
2         O RISCO   por que isso importa, numa frase. Esse slide também é uma
                    segunda capa, então não pode ser só preparação.
3 a N     UMA IDEIA POR SLIDE. Um título de 3 a 7 palavras e no máximo 25
                    palavras embaixo. Se o slide pede um parágrafo, são dois.
N+1       RESUMO    tudo numa lista. Esse é o slide do print.
ÚLTIMO    CTA       uma ação. Salvar, comentar uma palavra ou seguir. Uma.
```

## Regras do texto dos slides

- **A capa é 80% do resultado.** Seis palavras. Grande. Nada no resto do
  carrossel salva uma capa que ninguém arrasta.
- **Pense no corte do perfil.** A grade do perfil corta num retângulo em pé,
  mais alto que largo, e essa proporção já mudou mais de uma vez. Monte em
  1080x1350, deixe o texto da capa bem no meio, longe dos 120 pixels de cada
  borda, e o corte deixa de importar.
- **Numere os slides** (3/8). A pessoa vai até o fim com mais frequência quando
  enxerga onde ele está.
- **Nenhum slide é parágrafo.** Se não cabe em 25 palavras, divide.
- **O slide de resumo é o que a pessoa printa e manda pros outros.**
  Compartilhamento é o sinal mais forte que você consegue ganhar. Faça esse
  slide se entender sozinho, sem contexto nenhum.
- **Seu @ em todo slide**, pequeno, no canto de baixo. O print circula sem
  você.
- **Texto alternativo pelo menos na capa.** Leitor de tela lê, e o Instagram
  também.

## Gerando os arquivos

O Instagram pede 1080x1350 (4:5), JPEG ou PNG, até 20 itens. Monte em HTML e
imprima cada slide:

```bash
# um <section> por slide, 1080x1350, page-break-after: always
# depois Chrome headless --print-to-pdf, ou qualquer HTML-pra-imagem que você já use
```

Escreva o HTML com `width:1080px; height:1350px`, uma cor de destaque só, e
fonte de no mínimo 32px, porque isso vai ser lido num celular a um terço do
tamanho real. Se o projeto tem uma skill de marca ou um design system, use e
não invente paleta.

## Saída

Primeiro o texto slide por slide, numa lista numerada que o usuário lê em dez
segundos e edita antes de qualquer coisa ser renderizada. Depois a **legenda**,
que no carrossel é a Função B do `/ig-caption`: aqui a legenda trabalha de
verdade, porque a capa já gastou as seis palavras dela.

Passe as duas coisas pelo `/ig-human`. Só gere os arquivos depois que o usuário
aprovar o texto.

```
CARROSSEL  ·  8 slides

1  CAPA    A CLÁUSULA DE R$ 18 MIL
           Uma linha que hoje vai em todo contrato meu.
2  RISCO   Eu aprovei o trabalho. Nove dias depois pediram o dinheiro de volta.
3          O QUE ELA DIZ
           Pagamento na entrega, não na aprovação.
...
7  RESUMO  As quatro linhas, em ordem.
8  CTA     Comenta CONTRATO que eu te mando a cláusula inteira.

Legenda: Função B, gancho na linha 1, um pedido, 3 hashtags.
```

Nada é publicado. Quem posta é o usuário.
