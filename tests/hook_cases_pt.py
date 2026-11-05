"""Ganchos PT de referência e a fórmula esperada (None = não classificar).
Escritos à mão; servem para pegar regressão nos regex pt.match do hooks.json."""

CASES = [
    # 1 Confissão de Custo
    ("esse erro me custou dezoito mil reais", 1),
    ("perdi 40 mil num lançamento por causa de uma planilha", 1),
    ("R$ 12 mil foi o que eu joguei no lixo contratando agência errada", 1),
    # 2 Comando Negativo
    ("para de postar todo dia pelo amor de deus", 2),
    ("não compre curso de tráfego antes de ver isso", 2),
    ("gente para de responder direct com áudio de cinco minutos", 2),
    # 3 Ninguém Te Conta
    ("ninguém te conta que o primeiro lançamento quase sempre dá prejuízo", 3),
    ("o que ninguém fala sobre ter mil seguidores", 3),
    ("ninguem fala isso mas engajamento não paga boleto", 3),
    # 4 Substituição
    ("essa ia de vinte reais substituiu minha social media", 4),
    ("parei de pagar editor depois que descobri esse app", 4),
    # 5 Tempo Encolhido
    ("eu levava três horas pra editar um reels hoje eu levo quinze minutos", 5),
    ("isso demorava uma semana inteira agora leva uma tarde", 5),
    # 6 Recibo
    ("postei stories todo dia durante trinta dias e olha o que aconteceu", 6),
    ("aqui estão os números do meu último lançamento", 6),
    # 7 Jeito Errado
    ("você tá fazendo gancho errado e a culpa não é sua", 7),
    ("o maior erro de quem tá começando no instagram", 7),
    ("cê tá usando hashtag errado", 7),
    # 8 Bastidor
    ("trabalhei oito anos em agência e vou te contar o que a gente nunca falava pro cliente", 8),
    ("fui gerente de banco por 10 anos e isso aqui eles não te mostram", 8),
    # 9 Rouba Isso
    ("rouba esse roteiro de vendas que eu uso", 9),
    ("pode copiar essa mensagem que funciona", 9),
    # 10 Se Isso
    ("se você tem menos de mil seguidores assiste até o final", 10),
    ("se o seu reels trava nas 200 views o problema é esse", 10),
    # 11 Lista
    ("três ferramentas que eu uso todo dia e a número dois é de graça", 11),
    ("cinco dicas pra gravar sozinha em casa", 11),
    # 12 Objeção
    ("ah mas eu não tenho tempo de gravar todo dia", 12),
    ('"é caro demais pra mim" beleza então vamos fazer a conta', 12),
    # 13 Antes e Depois
    ("esse era o meu feed ano passado e esse é ele hoje", 13),
    ("antes da mentoria eu faturava dois mil depois passei pra vinte", 13),
    # 14 Chamado
    ("você que é nutricionista e não consegue cliente presta atenção", 14),
    ("esse vídeo é pra quem vende serviço no direct", 14),
    ("dentista que ainda cobra barato escuta isso", 14),
    # 15 Fracasso
    ("meus primeiros cinquenta vídeos não passaram de cem views", 15),
    ("postei por seis meses e nenhum vídeo viralizou", 15),
    # 16 Pergunta
    ("como eu cobro mais caro sem perder cliente? me perguntam isso toda semana", 16),
    ("todo dia me perguntam qual câmera eu uso", 16),
    # 17 Frente a Frente
    ("carrossel vs reels qual dá mais alcance", 17),
    ("qual é melhor iphone ou android pra gravar", 17),
    # 18 Demo
    ("olha o que acontece quando eu jogo esse prompt no chat gpt", 18),
    ("deixa eu te mostrar uma coisa", 18),
    # 19 Prazo
    ("o instagram muda isso na semana que vem então faz agora", 19),
    ("as inscrições fecham dia 30 e depois só ano que vem", 19),
    # 20 Permissão
    ("você não precisa de um nicho pra crescer", 20),
    ("cê não precisa aparecer pra vender", 20),
    # 21 Meio da frase
    ("e foi aí que ela pediu o dinheiro de volta", 21),
    ("aí o cliente virou e falou que não ia pagar", 21),
    # 22 Virada
    ("quem espera nunca alcança", 22),
    ("constância é superestimada", 22),
    ("o cliente nem sempre tem razão", 22),
    # 23 Estatística
    ("noventa por cento dos infoprodutores desistem no primeiro ano", 23),
    ("73% das pessoas nunca passam do terceiro segundo do seu vídeo", 23),
    ("oito em cada dez lançamentos não paga nem o tráfego", 23),
    # 24 Revelação
    ("esse é o novo microfone da dji e ele mudou meu jogo", 24),
    ("chegou o novo iphone e eu já testei tudo", 24),
    # 25 Outra pessoa
    ("uma aluna minha faturou cem mil no primeiro lançamento", 25),
    ("tem um cliente meu que saiu do zero pra trinta mil seguidores em dois meses", 25),
    # 26 Superlativo
    ("o jeito mais rápido de ganhar seguidor em 2026", 26),
    ("a melhor estratégia pra vender no direct é essa", 26),
    # should be unclassified
    ("oi gente tudo bem com vocês", None),
    ("e aí galera bem vindos a mais um vídeo", None),
    ("bom dia pessoal hoje eu vou falar sobre organização", None),
    ("a gente tava conversando sobre isso no último episódio", None),
    ("cara eu acho que o mercado mudou muito nos últimos anos", None),
    ("então pessoal o tema de hoje é bem polêmico", None),
    ("eu sempre fui muito tímida pra falar em público", None),
    ("vem comigo fazer o café da manhã", None),
    ("mano sinceramente eu não sei o que dizer sobre isso", None),
    ("olha gente que dia lindo aqui na praia", None),
    ("lembrando que o link tá na bio", None),
    ("ele falou uma coisa muito interessante na entrevista", None),
    ("se liga nessa que é rapidinho", None),
    ("para tudo que eu preciso contar uma fofoca", None),
    ("o que eu comi hoje sendo nutricionista", None),
    ("tava aqui pensando na vida", None),
    ("minha mãe sempre dizia que dinheiro não aceita desaforo", None),
    ("quanto custa morar em lisboa sendo brasileiro?", 16),
    ("larguei meu emprego de quinze mil e não me arrependo", None),
    ("a primeira vez que eu vendi cem mil numa live eu chorei", None),
]
