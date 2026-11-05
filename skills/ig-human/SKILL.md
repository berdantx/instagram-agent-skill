---
name: ig-human
description: >-
  Tira a digital de máquina de qualquer rascunho (travessão, palavras típicas
  de IA, caracteres invisíveis de marca d'água) e dá nota num painel de
  detecção com cinco checagens antes de sair. Use sempre que um texto precisar
  soar humano, quando o usuário disser "humaniza esse texto", "isso tá com
  cara de IA", "parece ChatGPT", "tira os travessões", "deixa mais natural",
  "tá muito robótico", ou antes de mostrar ao usuário qualquer legenda,
  roteiro, comentário, resposta ou DM.
---

# ig-human

Tem duas ferramentas nesta pasta e as duas rodam de verdade. Use. Não avalie
isso no olho.

```bash
python3 humanize.py draft.txt --report        # limpa e mostra o que mudou
python3 detect.py draft.txt                    # dá nota, cinco checagens
python3 detect.py before.txt after.txt         # prova a diferença
```

As duas detectam o idioma do texto (`--lang auto`, o padrão) e escolhem o
léxico certo. Pra forçar, use `--lang pt` ou `--lang en`.

O `slop.json` guarda as 18 classes de caracteres invisíveis, as 11
substituições tipográficas e o léxico em inglês. O léxico em português
(`slop.pt.json`) fica do lado dele: palavras e expressões de prateleira com
substituições em português simples, mais os padrões estruturais. O último
bloco de cada lista é específico de Instagram, o vocabulário que só aparece
em legenda e narração. Os arquivos foram feitos pra ser editados. Se o
usuário tem uma palavra que ele sempre usa e o léxico remove, tire ela do
arquivo.

## Por que isso pesa mais no Instagram do que parece

Legenda é curta e roteiro é falado em voz alta. Uma frase com cara de texto
escrito numa legenda de 600 caracteres ocupa uma fatia maior do texto do que a
mesma frase num artigo, e uma narração que ninguém falaria naturalmente fica
óbvia já no primeiro take. O problema aqui não é um detector marcar o post. O
problema é uma pessoa passando direto por algo que soa como marca, ou um
criador tropeçando no próprio roteiro.

## O que é corrigido automaticamente

**1. Caracteres invisíveis.** Espaços e junções de largura zero, word joiners,
hífens condicionais, marcas de ordem de byte, caracteres de tag Unicode,
separadores invisíveis, espaços inquebráveis e estreitos. Teclado nenhum
produz isso. Eles sobrevivem ao copiar e colar, são invisíveis em qualquer
editor e são a coisa mais mecânica de um texto gerado. O `humanize.py` apaga
todos, inclusive qualquer caractere de formatação Unicode que sobrar e que
ele não conheça pelo nome.

**2. Tipografia.** Travessão vira vírgula, meia-risca vira hífen, aspas
curvas viram retas, reticências de um caractere viram três pontos, marcador
de lista vira hífen. A passada do travessão é a que importa: ela troca o
travessão por vírgula e depois limpa a pontuação dobrada e os pontos soltos
que sobram.

**3. O léxico de clichês.** Em português, é o tipo de coisa como alavancar,
potencializar, robusto, crucial, jornada, mergulhar, "no cenário atual",
"vale ressaltar", mais o bloco de Instagram: "para de rolar o feed", "no
vídeo de hoje", "me segue pra mais", "marca alguém que precisa ver isso", "o
algoritmo ama". Em inglês, delve, leverage, seamless, "in today's fast-paced
world" e companhia. Cada um é trocado por uma palavra simples ou apagado,
mantendo maiúsculas e sem mexer em URLs.

## O que NÃO é corrigido automaticamente

Padrões estruturais são **apontados, não reescritos**, porque mudar o formato
de uma frase exige julgamento:

- "Não é só X, é Y" e "não apenas X, mas também Y"
- Trincas de três itens por reflexo
- Pergunta retórica de uma palavra numa linha: "O resultado?"
- O preâmbulo de vídeo: "nesse vídeo eu vou te mostrar"
- Lista com emoji no lugar de marcador
- Três ou mais palavras gritadas em maiúscula seguidas
- Muro de hashtags
- Isca automática: "me segue pra mais", "marca alguém que", "dá dois toques se"

Essa lista é trabalho seu. Reescreva cada linha apontada à mão, mantendo o
sentido, e rode o `detect.py` de novo. É essa parte que leva a nota de REVISAR
pra APROVADO, e é a parte que script nenhum faz.

O relatório do `humanize.py --report` sai com o título "RELATÓRIO DO
HUMANIZADOR" e quatro seções: "1. CARACTERES INVISÍVEIS", "2. TIPOGRAFIA", "3.
LÉXICO DE CLICHÊS" e "4. PADRÕES ESTRUTURAIS". As três primeiras mostram o que
foi trocado. A quarta é a sua lista de tarefas.

## As cinco checagens

O `detect.py` mostra o "PAINEL DE DETECÇÃO DE IA" com cinco sinais de 0 a 100.
Quanto maior, mais humano:

| checagem | o que mede | cara de máquina |
| --- | --- | --- |
| VARIAÇÃO | variação no tamanho das frases | toda frase do mesmo tamanho |
| ESPECIFICIDADE | números, nomes e marcas concretas a cada 100 palavras | substantivo abstrato, nenhum número |
| CLICHÊS | ocorrências do léxico a cada 100 palavras | vocabulário de prateleira |
| DIGITAL | caracteres invisíveis, travessões e aspas curvas a cada 1.000 caracteres | tipografia perfeita demais |
| VOZ | marcas de informalidade, pessoa do discurso, padrões estruturais | nenhuma marca de fala, revelações encenadas |

Em português, a VOZ conta formas coloquiais como "tá", "pra", "né", "a gente".
Em inglês, conta as contrações.

O veredito pesa a média em 60% e a **checagem mais fraca** em 40%, porque um
sinal só já basta. A linha "NOTA HUMANA" traz o total. APROVADO exige 70 ou
mais no geral e nenhuma checagem abaixo de 55. Fora isso, sai REVISAR ou
SINALIZADO.

## Diga isso com honestidade

São cinco heurísticas locais, inspiradas nos sinais que os detectores
públicos observam. Elas rodam inteiras na máquina do usuário e nada é
enviado. Elas **não** são GPTZero, Originality, Copyleaks, Winston nem
Turnitin, não chamam essas APIs e não podem prometer o veredito delas.
Corrigir o que elas medem costuma mexer nesses números, porque elas estão
medindo as mesmas coisas por baixo. A afirmação é essa. Não faça uma maior em
nome do usuário, e não diga a ninguém que o texto é indetectável.

## Ordem das operações

1. `humanize.py draft.txt -o clean.txt --report`
2. Leia os padrões estruturais apontados. Reescreva essas linhas você mesmo.
3. `detect.py draft.txt clean.txt` pra mostrar o antes e o depois.
4. Se o veredito não for APROVADO, corrija a checagem mais fraca que aparece
   na saída e rode de novo. Duas rodadas é normal. Cinco quer dizer que o
   rascunho foi escrito por fórmula, e a solução é outro rascunho, não mais
   passadas.
5. Mostre ao usuário o texto limpo e a nota. Nunca só a nota.
