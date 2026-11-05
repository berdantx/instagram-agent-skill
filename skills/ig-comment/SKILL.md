---
name: ig-comment
description: >-
  Escreve comentários nos posts e reels dos outros no Instagram que soam como
  uma pessoa com opinião, não como robô. Use quando o usuário colar um post ou
  um reel e quiser um comentário, disser "comenta nisso", "o que eu comento
  aqui", "escreve um comentário pra esse reel", "engaja nesse post", ou quiser
  um lote pra rodada diária de engajamento.
---

# ig-comment

Comentar é o tempo mais bem gasto do dia no Instagram, e o mais fácil de fazer
mal. Um comentário lá em cima num reel com 40 mil visualizações é visto por
mais gente que a maioria dos posts da própria conta, e é o único lugar onde um
estranho toca e cai direto no seu perfil.

Comentário genérico é pior que nenhum. Gasta um toque que não leva a lugar
nenhum e marca a conta como conta de grupo de engajamento pra única pessoa cuja
opinião importava ali, que é o criador do post.

## Entrada

O usuário cola o texto do post ou do reel, ou um print, com o nome do perfil.
Se ele mandar um link que você não consegue abrir, peça pra colar. Não use
ferramenta de navegador pra raspar o feed e não publique nada.

## Os nove tipos de comentário

Escolha pelo que o post realmente é. Nunca vá no tipo 1 por padrão.

| # | tipo | quando | formato |
| --- | --- | --- | --- |
| 1 | **Somar um dado** | o post faz uma afirmação que você consegue sustentar com um número | "Aqui foi igual: 40% de..." |
| 2 | **Somar o caso que faltou** | o post está certo, mas incompleto | "Isso vale até {condição}." |
| 3 | **Discordar com respeito** | você acha de verdade que está errado | diga primeiro onde concorda, depois onde diverge |
| 4 | **Estender uma frase** | uma frase do post é a boa | cite ela e construa em cima |
| 5 | **Fazer a pergunta de verdade** | o post pulou a parte difícil | uma pergunta, específica |
| 6 | **O recibo** | você já fez o que ele descreveu | o que aconteceu, em duas frases |
| 7 | **A correção** | tem um erro de fato | esteja certo, seja breve, seja gentil, tenha certeza |
| 8 | **A outra leitura** | fatos certos, enquadramento errado | "Dá pra ler isso de outro jeito:" |
| 9 | **A frase curta** | o post não precisa de nada, você quer marcar presença | menos de 10 palavras, tem que ser engraçada ou verdadeira |

## Regras

- **Uma a três frases.** Comentário no Instagram é lido numa coluna estreita
  embaixo de um vídeo. Parágrafo fica escondido atrás do "mais" e ninguém toca.
- **Nunca abra com** "Que post incrível", "Amei", "Verdade demais", "Isso 👏",
  "Precisava ouvir isso hoje", ou o primeiro nome do criador com ponto de
  exclamação. Todos esses são invisíveis.
- **Nada de comentário só com emoji**, e nada de emoji como primeiro caractere.
- **Nunca repita o reel.** Todo mundo que está ali acabou de assistir.
- **Uma ideia.** Comentário com dois pontos parece sequestro da conversa.
- **Diga a coisa específica.** Se o comentário serviria embaixo de qualquer
  post sobre o tema, não é comentário, é ruído.
- **Nunca venda, em hipótese nenhuma.** Nem a oferta, nem o link, nem "dá uma
  olhada no meu perfil". É o jeito mais rápido de ser bloqueado justamente pela
  pessoa que você queria alcançar.
- **Chegar cedo pesa mais aqui que em qualquer outro lugar.** Um comentário na
  primeira hora de um reel que depois viraliza viaja junto com ele.

## Saída

Entregue **duas opções de tipos diferentes**, identificadas, mais uma linha
dizendo qual você postaria e por quê. Passe as duas pelo `/ig-human` antes:
comentário é curto, então um travessão ou uma frase pronta chama muito mais
atenção do que numa legenda.

```
OPÇÕES DE COMENTÁRIO  (no reel do @acct sobre preço)

[6 · Recibo]
A gente subiu 40% em março do ano passado e perdeu exatamente um cliente, o
que ocupava metade da caixa de entrada. Levei oito meses pra parar de ter medo.

[3 · Discordar com respeito]
Concordo na parte da ancoragem. O que eu questionaria é fazer isso no meio do
projeto. A gente tentou e custou uma renovação que estava tudo certo.

Posta a primeira. Ela admite uma coisa e tem um número.
```

## Modo lote

Pra uma rodada de engajamento, peça os 5 a 10 posts como texto colado numa
mensagem só, devolva um comentário pra cada num bloco único, e mantenha uma
anotação em `~/.claude/instagram/log.md` de quem já recebeu comentário na
semana. Comentar nos mesmos três perfis todo dia dá na vista e parece
exatamente o que é.

## Nunca

Não publique automaticamente, não automatize comentários e não use ferramenta
de navegador pra publicar no lugar do usuário. Engajamento automatizado viola
os Termos de Uso do Instagram e faz a conta levar bloqueio de ação. Esta skill
escreve o comentário. Quem posta é o usuário.
