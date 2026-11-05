---
name: ig-caption
description: >-
  Escreve a legenda do Instagram: a frase que sobrevive ao corte do "... mais",
  o corpo, o pedido único, os termos de busca e as hashtags, e passa um lint
  antes de sair. Use quando o usuário disser "faz a legenda", "escreve a
  legenda", "legenda pra esse reel", "o que eu coloco na descrição", "quantas
  hashtags eu uso", quando tiver um reel ou carrossel pronto e precisar do
  texto, ou perguntar sobre hashtags.
---

# ig-caption

Tem uma ferramenta nesta pasta e ela roda:

```bash
python3 caption.py caption.txt
python3 caption.py caption.txt --keywords "proposta comercial,preço de serviço"
```

Ela entende legenda em português e em inglês sem precisar de opção nenhuma:
reconhece os pedidos e as hashtags genéricas dos dois idiomas.

Ela mostra a legenda do jeito que o feed mostra: os primeiros 125 caracteres
numa caixa ("O QUE O FEED MOSTRA", terminando em "... mais"), e todo o resto
atrás do toque. Leia essa caixa antes de ler qualquer outra coisa que você
escreveu.

## Primeiro, decida qual é o trabalho desta legenda

É a decisão que estraga legendas quando ninguém para pra tomar.

**Caso A: o vídeo já fisgou.** Um Reel carrega o próprio gancho nos dois
primeiros segundos, falado e na tela. A legenda não é um segundo gancho, e
competir com o vídeo é o jeito de perder os dois. O trabalho dela é o pedido,
o contexto que faz o pedido fazer sentido, e as palavras que as pessoas
buscam.

**Caso B: a legenda é o conteúdo.** Uma foto, uma imagem única, a capa de um
carrossel que abre uma curiosidade. Aqui a primeira linha é o gancho e
funciona igualzinho a um gancho de Reel: concreta, curta, e cortada num
precipício, não no meio de uma oração.

Pergunte qual dos dois você está escrevendo. Se o usuário tem um Reel com
gancho forte, escreva o A e diga por quê.

## A estrutura

```
Linha 1     125 caracteres de espaço visível. Caso A: o pedido, direto.
            Caso B: o gancho.
            Nunca um "bom dia", nunca uma hashtag, nunca um emoji como
            primeiro caractere.
Corpo       parágrafos curtos, uma linha em branco entre eles. De dois a seis.
            É aqui que moram os termos de busca.
O pedido    um. Comentar uma palavra, salvar ou chamar na DM. Um.
Hashtags    até cinco, numa linha só delas no final, ou nenhuma.
```

O limite é de 2.200 caracteres e quase nada precisa de 2.200. Uma legenda que
ganha o toque e depois entrega 600 caracteres ganha de uma que entrega 1.800.

## Hashtags, sem rodeio

Hashtag não dá mais alcance, e a plataforma já disse isso com uma
mudança de produto. **O Instagram limitou as hashtags a cinco por post em 18
de dezembro de 2025**, contra trinta antes, dizendo aos criadores que usar
menos hashtags (até 5) e mais direcionadas, em vez de muitas genéricas,
funciona melhor. Adam Mosseri já tinha dito em fevereiro de 2025 que hashtag
não aumenta alcance e é uma etiqueta, não um motor de distribuição.

Então: até cinco, específicas, como etiqueta de assunto. Se o usuário tem um
bloco de vinte salvo no bloco de notas, esse bloco agora é peso morto e o
linter vai reprovar.

`#viral`, `#fyp`, `#explorepage`, `#foryou` não descrevem nada. Corte.

## Termo de busca importa mais que hashtag agora

A busca do Instagram lê o texto da legenda. Então a frase pela qual o usuário
quer ser encontrado entra na legenda como alguém digitaria, numa frase que
soa normal. "Proposta comercial" escrito na linha três, não
"#propostacomercial" num bloco lá embaixo.

Peça dois ou três desses termos e passe pro linter:

```bash
python3 caption.py draft.txt --keywords "proposta comercial,preço de serviço"
```

## Regras

- **Sem link na legenda.** Legenda não é clicável. URL no corpo é texto morto
  que diz "eu não uso essa plataforma". Bio ou DM.
- **Um pedido.** Dois pedidos é o mesmo que nenhum. O `caption.py` conta.
- **O pedido de palavra-chave precisa de uma palavra que dá pra digitar.** Uma
  palavra, sem espaço, sem emoji, e fale ela em voz alta no vídeo também.
  `Comenta CONTRATO` funciona. `Comenta "o guia do contrato"` não.
- **Escreva o primeiro comentário separado** se tiver link. Diga isso no
  resumo.
- **Emoji como pontuação, não como enfeite.** O linter aponta qualquer coisa
  acima de 4 a cada 100 caracteres.
- **Texto alternativo vale 20 segundos.** Em carrossel e foto, escreva. Ele é
  lido por leitores de tela e pelo Instagram.

## O processo

1. Decida Caso A ou Caso B e diga qual.
2. Escreva o rascunho.
3. Passe pelo `/ig-human`. Legenda é curta, então frase de IA grita mais aqui
   do que em qualquer outro lugar do pacote.
4. Rode o `caption.py` com os termos de busca do usuário. Os itens checados
   são TAMANHO, PRIMEIRA LINHA, GANCHO CONCRETO, HASHTAGS, POSIÇÃO DAS TAGS,
   LINKS, UM PEDIDO, EMOJI e TERMOS DE BUSCA, cada um com OK, AVISO ou FALHA.
   Corrija toda FALHA. Decida cada AVISO em voz alta, não em silêncio. A última
   linha é o veredito: `VEREDITO  PRONTA`, `REVISAR` ou `CORRIGIR`.
5. Entregue o bloco pronto pra copiar e depois o resumo:

```
LEGENDA PRONTA
caso:       A, o reel carrega o gancho
visível:    118 de 125 caracteres usados antes do corte
pedido:     um, comenta CONTRATO
hashtags:   3
busca:      "proposta comercial" na linha 3, "preço de serviço" na linha 5
linter:     PRONTA
```

Nada é postado. O usuário cola.
