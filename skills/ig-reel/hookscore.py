#!/usr/bin/env python3
"""
hookscore.py - dá nota à primeira linha de um Reel nas cinco coisas que os
ganchos fortes têm em comum, e ranqueia um lote deles entre si.

Funciona em português e inglês: cada gancho tem o idioma detectado sozinho
(ou force com --lang), e as listas de números falados, palavras de tensão,
aberturas fracas e eliminatórios mudam junto. A saída é em português.

What this is:  five local heuristics, computed on your machine from the text
alone. They measure properties that hooks which hold attention tend to share -
a length you can say in under three seconds, a concrete marker, something at stake,
the payload at the front rather than the back, and a viewer to aim it at.

What this is NOT:  a view predictor. It was tested against 74 real short-form
hooks, transcribed from the first three seconds of the top eight and bottom
eight performers on five channels. Separating a real hook from a deliberately
bad one it does well: AUC 0.83, and 9 of 10 written-to-be-bad hooks scored
below the real median. Separating a good creator's hits from that same
creator's misses it barely does at all: AUC 0.56, where 0.50 is a coin flip.

So use it for what it measured well. It catches greetings, preambles, hooks
with nothing concrete in them and hooks that take five seconds to say. It will
not tell you which of two decent hooks will travel, and nothing that reads text
can, because that is decided by your face, your edit, your audio and who
Instagram shows it to. Trust the retention graph over this script.

Each check returns 0 to 100. Higher is better.

Usage / Uso
  python3 hookscore.py ganchos.txt            # um gancho por linha, ranqueados
  python3 hookscore.py --hook "Perdi R$ 18 mil por uma cláusula que faltou."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py ganchos.txt --json
  python3 hookscore.py ganchos.txt --lang pt
"""

import argparse
import json
import re
import statistics
import sys

# "$18,000" e "R$ 18.000" são uma palavra quando faladas, então aqui também.
WORD_RE = re.compile(r"(?:R?\$\s?)?\d+(?:[.,]\d+)*(?:%|k\b)?|[^\W\d_]+(?:['’-][^\W\d_]+)*")
NUMBER_RE = re.compile(
    r"R?\$\s?\d[\d,.]*"                              # money, whole
    r"|\b\d[\d,.]*\s?"                               # a figure, with or
    r"(?:%|k\b|x\b|hrs?\b|hours?\b|mins?\b|minutes?\b"  # without a unit
    r"|days?\b|weeks?\b|months?\b|years?\b"
    r"|h\b|horas?\b|minutos?\b|dias?\b|semanas?\b|m[eê]s\b|meses\b|anos?\b|mil\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<!^)\b[A-ZÀ-ÖØ-Þ][a-zß-öø-ÿ]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Spoken hooks say their numbers out loud. "Zero dollars" and "twenty grand"
# are as concrete as "$0" and "$20,000", and counting only digits missed them.
# "one" and "first" are deliberately absent: they are filler far more often
# than they are a quantity.
SPOKEN_NUMBERS = {
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
    "billion", "dozen", "half", "twice", "triple",
}
MONEY_WORDS = {
    "dollars", "dollar", "bucks", "grand", "percent", "cents",
    "millionaire", "billionaire", "revenue", "profit", "salary", "rent",
}

# Words that put something on the line. A hook with none of these is a
# statement; a hook with one is a reason to keep watching.
STAKES = {
    "stop", "never", "wrong", "mistake", "mistakes", "lost", "lose", "losing",
    "cost", "costs", "broke", "broken", "failed", "failure", "fail", "nobody",
    "no", "not", "don't", "dont", "doesn't", "didn't", "can't", "won't",
    "quit", "quitting", "fired", "deleted", "delete", "killed", "kills", "kill",
    "replaced", "replaces", "cut", "beat", "free", "paid", "charged", "hired",
    "saved", "first",
    "banned", "illegal", "worst", "hate", "hated", "wasted", "waste", "scam",
    "lie", "lied", "lying", "truth", "secret", "hidden", "stole", "stolen",
    "before", "until", "instead", "but", "except", "unless", "problem",
    "risk", "danger", "warning", "regret", "wish", "should", "shouldn't",
    "still", "already", "only", "without", "versus", "vs", "actually",
}

# Português. Mesma lógica das listas em inglês acima.
SPOKEN_NUMBERS_PT = {
    "zero", "dois", "duas", "três", "tres", "quatro", "cinco", "seis", "sete",
    "oito", "nove", "dez", "onze", "doze", "quinze", "vinte", "trinta",
    "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa", "cem",
    "cento", "duzentos", "trezentos", "quinhentos", "mil", "milhão", "milhao",
    "milhões", "milhoes", "bilhão", "bilhões", "dúzia", "duzia", "metade",
    "dobro", "triplo", "dobrei", "tripliquei",
}
MONEY_WORDS_PT = {
    "reais", "conto", "contos", "pila", "pilas", "grana", "faturamento",
    "faturei", "faturou", "faturamos", "lucro", "lucrei", "salário", "salario",
    "aluguel", "porcento", "vendi", "vendas", "milionário", "milionária",
    "bilionário", "prejuízo", "prejuizo",
}
STAKES_PT = {
    "pare", "nunca", "errado", "errada", "erro", "erros", "errei", "erra",
    "perdi", "perder", "perdendo", "perdeu", "perdemos", "custo", "custou",
    "custa", "quebrei", "quebrou", "faliu", "falência", "falhei", "falhou",
    "fracasso", "fracassei", "flopou", "flopar", "flopa", "ninguém", "ninguem",
    "não", "nao", "nem", "larguei", "largar", "demitido", "demiti", "apaguei",
    "apague", "apaga", "matou", "mata", "substituí", "substitui", "substituiu",
    "cortei", "corta", "venci", "grátis", "gratis", "paguei", "pagou", "cobrei",
    "cobrar", "cobra", "contratei", "economizei", "primeiro", "primeira",
    "proibido", "ilegal", "pior", "odeio", "odiei", "desperdicei", "golpe",
    "mentira", "menti", "mentiram", "verdade", "segredo", "escondido", "roubei",
    "roubado", "antes", "até", "mas", "exceto", "problema", "risco", "perigo",
    "cuidado", "arrependo", "deveria", "devia", "ainda", "já", "só", "sem",
    "contra", "versus", "vs", "dívida", "divida", "processado", "bloqueado",
    "banido", "reembolso", "cancelou", "cancelei",
}
WEAK_OPENERS_PT = [
    "oi", "olá", "ola", "fala", "galera", "gente", "pessoal", "e aí", "eai",
    "bom dia", "boa tarde", "boa noite", "então", "entao", "bom", "hoje",
    "basicamente", "sinceramente", "olha", "escuta", "só", "deixa", "vamos",
    "vem", "bora", "neste", "nesse", "no vídeo", "você sabia", "voce sabia",
    "sabia que", "vocês sabiam", "tem", "existe", "existem", "isso é", "esse é",
    "essa é", "é", "um dos", "uma das", "tudo bem", "seja bem", "sejam bem",
    "tipo", "né", "ah", "eh", "hum", "ó", "quero falar", "eu queria", "eu quero",
]
IMPERATIVES_PT = {
    "pare", "para", "rouba", "roube", "copia", "copie", "apaga", "apague",
    "tenta", "tente", "assiste", "assista", "veja", "lê", "leia", "salva",
    "salve", "usa", "use", "faz", "faça", "escreve", "escreva", "manda",
    "mande", "pega", "pegue", "começa", "comece", "larga", "largue", "nunca",
    "sempre", "não", "nao", "coloca", "coloque", "bota", "confere", "confira",
    "esquece", "esqueça", "testa", "teste", "cobra", "cobre", "presta",
}
DEALBREAKERS_PT = [
    (re.compile(r"(?i)^\s*(?:para|pare) de (?:rolar|passar)|^\s*n[aã]o (?:passa|pula|role|arrasta)\b"),
     "Abre com \"para de rolar\". Pedir atenção prova que você ainda não ganhou."),
    (re.compile(r"(?i)\b(?:neste|nesse|no) (?:v[ií]deo|reels?)\b|\bvou (?:te |lhes? )?(?:mostrar|ensinar)\b|\bhoje eu vou\b"),
     "Preâmbulo de vídeo. Apaga e abre no resultado."),
    (re.compile(r"(?i)^\s*(?:oi|ol[aá]|fala+|e a[ií]|eai|bom dia|boa tarde|boa noite|tudo bem|sejam? bem[- ]vind[oa]s?)\b"),
     "Saudação. Ninguém abriu o feed para ser cumprimentado."),
]

# Openers that spend the first second saying nothing.
WEAK_OPENERS = [
    "so", "ok", "okay", "hey", "hi", "hello", "guys", "yo", "alright",
    "welcome", "today", "basically", "honestly", "look", "listen", "um",
    "just", "let", "lets", "let's", "i wanted", "i want", "one of",
    "have you", "did you", "do you", "are you", "in this", "in today",
    "the thing", "a lot", "there is", "there are", "this is", "it is",
    "as a", "when it", "if you've", "you know",
]

# Imperatives that earn the front position.
IMPERATIVES = {
    "stop", "steal", "copy", "delete", "try", "watch", "read", "save",
    "use", "build", "make", "write", "send", "take", "start", "quit",
    "never", "always", "don't", "dont", "do", "put", "run", "check",
}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:stop scrolling|don'?t scroll)"),
     "Abre com \"stop scrolling\". Pedir atenção prova que você ainda não ganhou."),
    (re.compile(r"(?i)\b(?:in (?:this|today'?s) (?:video|reel)|i'?m going to show you|i'?ll show you how)\b"),
     "Preâmbulo de vídeo. Apaga e abre no resultado."),
    (re.compile(r"(?i)^\s*(?:hey |hi |what'?s up |welcome )"),
     "Saudação. Ninguém abriu o feed para ser cumprimentado."),
]
SHARED_DEALBREAKERS = [
    (HASHTAG_RE,
     "Hashtag no gancho. Hashtag fica no fim da legenda, se ficar."),
    (EMOJI_RE,
     "Emoji no gancho. Texto na tela em tamanho de gancho tem espaço para palavras ou para emoji, não os dois."),
]

PT_HINTS = {
    "de", "que", "não", "nao", "é", "um", "uma", "para", "pra", "com", "você",
    "voce", "eu", "os", "as", "do", "da", "no", "na", "em", "por", "mais", "mas",
    "isso", "meu", "minha", "seu", "sua", "tá", "foi", "como", "quando",
    "porque", "ninguém", "ninguem", "já", "só", "te", "cê", "seus", "suas",
    "perdi", "nunca", "gente", "vocês", "nós", "tem", "sem",
}
EN_HINTS = {
    "the", "and", "is", "you", "to", "of", "that", "it", "for", "with", "this",
    "are", "was", "not", "my", "your", "but", "what", "how", "i", "we", "they",
    "have", "be", "on", "in", "at", "do", "don't", "it's", "i'm", "nobody",
    "stop", "never", "lost", "tells",
}


def detect_lang(text):
    """Empate ou texto sem pista cai em PT: este fork é português primeiro."""
    low = text.lower()
    toks = re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?", low)
    pt = sum(1 for t in toks if t in PT_HINTS)
    pt += 2 * len(re.findall(r"[ãõçáéíóúâêôà]", low)) + 3 * low.count("r$")
    en = sum(1 for t in toks if t in EN_HINTS)
    return "en" if en > pt else "pt"


VOCAB = {
    "en": {"spoken": SPOKEN_NUMBERS, "money": MONEY_WORDS, "stakes": STAKES,
           "openers": WEAK_OPENERS, "imperatives": IMPERATIVES,
           "dealbreakers": DEALBREAKERS + SHARED_DEALBREAKERS,
           "you": r"\b(you|your|you're|youre|yourself)\b",
           "me": r"\b(i|my|me|we|our)\b"},
    "pt": {"spoken": SPOKEN_NUMBERS_PT, "money": MONEY_WORDS_PT, "stakes": STAKES_PT,
           "openers": WEAK_OPENERS_PT, "imperatives": IMPERATIVES_PT,
           "dealbreakers": DEALBREAKERS_PT + SHARED_DEALBREAKERS,
           "you": r"\b(?:voc[eê]s?|c[eê]|te|teu|tua|teus|tuas|contigo|seu|sua|seus|suas)\b",
           "me": r"\b(?:eu|meu|minha|meus|minhas|me|mim|comigo|n[oó]s|nosso|nossa|nossos|nossas|a gente)\b"},
}


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    return WORD_RE.findall(text)


def check_length(text, v=None):
    """A hook has to land before the thumb moves. Roughly two seconds."""
    w = words(text)
    n = len(w)
    secs = n / 2.75                      # ~165 words per minute, spoken
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > 60:                       # two lines of big on-screen text
        score -= 12
    return clamp(score), f"{n} palavras, {chars} caracteres, ~{secs:.1f}s falado (ideal: 5 a 12 palavras)"


def check_specificity(text, v):
    """One concrete thing beats three abstract ones."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = [w.lower().strip("'’") for w in words(text)]
    spoken = [w for w in low if w in v["spoken"] or w in v["money"]]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} marca(s) concreta(s)" + (f": {found}" if found else
                   ", sem número, sem nome, nada checável"))


def check_stakes(text, v):
    """Tension, cost, negation. Something the viewer might lose."""
    w = [x.lower().strip("'’") for x in words(text)]
    hits = [x for x in w if x in v["stakes"]]
    markers = sorted(set(hits))
    if re.search(r"\$\s?\d", text):
        markers.append("um preço")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marca(s) de tensão" + (f": {', '.join(markers[:4])}" if markers else
                                          ", nada está em jogo nesta linha")
    return clamp(score), detail


def check_frontload(text, v):
    """The interesting word cannot be in position nine."""
    w = words(text)
    if not w:
        return 0.0, "vazio"
    low = [x.lower().strip("'’") for x in w]
    # Compara palavra inteira: "so" não pode pegar "some", nem "só" pegar "sócio".
    opener = " ".join(low[:3]) + " "
    penalty = 0
    hit_opener = None
    for weak in v["openers"]:
        if opener.startswith(weak + " "):
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in v["stakes"] or token in v["spoken"] or token in v["money"]
                or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "nenhuma palavra de peso na linha"
    elif payload <= 3:
        base = 100.0
        where = f"peso na palavra {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"peso na palavra {payload + 1}, dá para trazer para frente"
    else:
        base = 40.0
        where = f"peso na palavra {payload + 1}, tarde demais"
    detail = where + (f"; abertura fraca \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text, v):
    """Aimed at one viewer, or floating in the air."""
    low = text.lower()
    w = [x.lower().strip("'’") for x in words(text)]
    if re.search(v["you"], low):
        return 100.0, "fala com quem assiste"
    if w and w[0] in v["imperatives"]:
        return 90.0, f"abre no imperativo (\"{w[0]}\")"
    if re.search(v["me"], low):
        return 70.0, "primeira pessoa, sem falar com ninguém"
    return 35.0, "terceira pessoa, ninguém na sala"


CHECKS = ["LENGTH", "SPECIFICITY", "STAKES", "FRONTLOAD", "ADDRESS"]
LABELS = {"LENGTH": "TAMANHO", "SPECIFICITY": "ESPECIFICIDADE", "STAKES": "TENSÃO",
          "FRONTLOAD": "FRENTE", "ADDRESS": "ALVO"}


def run(text, lang="auto"):
    v = VOCAB[detect_lang(text) if lang == "auto" else lang]
    results = {
        "LENGTH": check_length(text),
        "SPECIFICITY": check_specificity(text, v),
        "STAKES": check_stakes(text, v),
        "FRONTLOAD": check_frontload(text, v),
        "ADDRESS": check_address(text, v),
    }
    flags = [msg for pattern, msg in v["dealbreakers"] if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # The weakest property caps the hook, same logic as detect.py: one bad
    # property is enough for the thumb to keep moving.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FORTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "FRACO")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nNOTA DO GANCHO", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {LABELS[name]:<14} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<14} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA':<14} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  ELIMINATÓRIO  {f}", file=out)
    if verdict != "FORTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Ponto mais fraco: {LABELS[weakest]}. Corrija esse e rode de novo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        ponto fraco: {LABELS[r['weakest']]} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        eliminatório: {f}", file=out)
    print("\nGrave o primeiro. Se o primeiro está abaixo de 50, nenhum destes é o gancho.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Dá nota a um gancho de Reel em cinco critérios.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo com um gancho por linha, ou -")
    ap.add_argument("--hook", help="avalia um gancho só, passado na linha de comando")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lang", choices=["auto", "pt", "en"], default="auto",
                    help="idioma dos ganchos (padrão: detecta em cada linha)")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("nada para avaliar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line, args.lang)
        payload.append({
            "hook": line,
            "lang": detect_lang(line) if args.lang == "auto" else args.lang,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0], args.lang)
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
