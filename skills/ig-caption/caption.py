#!/usr/bin/env python3
"""
caption.py - lint an Instagram caption and show exactly what the feed shows
before the "... more".

Instagram gives a caption about 125 characters in the feed and hides the rest
behind a tap. Almost every caption that fails, fails there: the hook is in
sentence three, or the first line is a greeting, or the whole thing opens on a
hashtag. This prints the visible window as a box so you can read it the way a
scrolling stranger does, then checks the eight things that are worth checking.

The 125-character cut is an approximation. The real number moves with the
device, the font size and where your line breaks fall, which is exactly why
you want a margin rather than a caption engineered to end at 125. Change it
with --truncate if you want to test a tighter one.

Funciona com legenda em português ou inglês (os pedidos e as tags genéricas
dos dois idiomas são reconhecidos). A saída é em português.

Usage / Uso
  python3 caption.py legenda.txt --keywords "contrato de cliente,precificação"
  python3 caption.py caption.txt
  python3 caption.py caption.txt --keywords "proposal software,client contract"
  pbpaste | python3 caption.py -
  python3 caption.py caption.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # Instagram's hard caption limit.
TRUNCATE = 125           # Roughly where the feed cuts to "... more".
HASHTAG_LIMIT = 5        # Instagram's cap per post or reel since 18 Dec 2025,
                         # down from 30. Announced by the @Creators account:
                         # "using fewer (up to 5) more targeted hashtags,
                         # rather than many generic ones, can improve both your
                         # content's performance and people's experience".

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[A-Za-z0-9_.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app)(?:\.br)?/\S*"
                     r"|\b[a-z0-9-]+\.com\.br\b",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(r"R?\$\s?\d|\b\d[\d,.]*\b|(?<!^)\b[A-ZÀ-ÖØ-Þ][a-zß-öø-ÿ]{2,}\b",
                         re.MULTILINE)

# The keyword has to be in caps ("comment CONTRACT", "comenta QUERO"), so the
# verb is case-insensitive by hand and the keyword is not: with a blanket
# (?i), "comment below" and "comenta aqui" counted as a keyword ask.
ASKS = [
    (re.compile(r"\b(?:[Cc]omment|COMMENT) (?:the word |\"|“)?[A-Z0-9]{2,}\b"
                r"|\b(?:[Cc]oment[ae]|COMENT[AE])(?: (?:a palavra|aqui|a[ií]|s[oó]))? (?:\"|“)?[A-ZÀ-Ý0-9]{2,}\b"),
     "comentar palavra-chave"),
    (re.compile(r"(?i)\b(?:dm|message) me\b|\b(?:me )?chama no (?:direct|dm|privado|pv)\b"
                r"|\b(?:me )?manda (?:uma )?(?:dm|mensagem|direct)\b"), "DM"),
    (re.compile(r"(?i)\bsave (?:this|it)\b|\bsalv[ae] (?:esse|este|essa|esta|isso|o post|pra depois)\b"),
     "salvar"),
    (re.compile(r"(?i)\bshare (?:this|it)\b|\bcompartilh[ae] (?:esse|este|essa|isso|com)\b"
                r"|\bmanda (?:isso |esse (?:post|v[ií]deo) )?pra (?:algu[eé]m|quem|aquele|aquela)\b"),
     "compartilhar"),
    (re.compile(r"(?i)\bfollow (?:me|for)\b|\bme segue\b|\bsegue (?:o perfil|pra mais|para mais)\b"
                r"|\bsiga (?:o perfil|para mais|@)"), "seguir"),
    (re.compile(r"(?i)\blink in (?:my )?bio\b|\blink na (?:minha )?bio\b"), "link na bio"),
    (re.compile(r"(?i)\b(?:swipe|tap) (?:through|left|right|for|to)\b"
                r"|\b(?:arrast[ae]|desliz[ae]) (?:pro|pra|para o) lado\b"), "arrastar ou tocar"),
    (re.compile(r"(?i)\btell me\b|\bwhat would you\b|\bwhich one\b"
                r"|\bme (?:conta|conte|diz|diga|fala)\b|\bqual (?:voc[eê]|delas|deles)\b"
                r"|\bo que voc[eê] (?:faria|acha)\b"), "responder pergunta"),
]

FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
               "#trending", "#instagood", "#love", "#follow", "#like4like", "#reels",
               "#reelsinstagram", "#viralreels", "#instadaily",
               "#explorar", "#paravoce", "#paravocê", "#pravoce", "#pravocê", "#viralizou",
               "#reelsbrasil", "#instabrasil", "#seguidores", "#sigoback", "#sdv",
               "#curtidas", "#viralizar", "#tbt", "#amor"}


def visible_window(text, cut):
    """What the feed shows. Instagram cuts mid-word, so this does too."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  O QUE O FEED MOSTRA", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... mais" if truncated else "(cabe inteira)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LENGTH", "FAIL" if chars > LIMIT else "PASS",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} acima do limite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("FIRST LINE", "FAIL", "a legenda abre com uma linha em branco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("FIRST LINE", "FAIL",
            "abre com hashtag ou menção, na única posição que vale uma frase")
    elif len(first_line) > cut:
        add("FIRST LINE", "WARN",
            f"{len(first_line)} caracteres, então é cortada em {cut} no meio da ideia. "
            "Tudo bem se o corte é um gancho, ruim se cai no meio de uma oração")
    else:
        add("FIRST LINE", "PASS", f"{len(first_line)} caracteres, aparece inteira")

    add("HOOK IS CONCRETE", "PASS" if CONCRETE_RE.search(window) else "WARN",
        f"{len(CONCRETE_RE.findall(window))} número(s) ou nome(s) no trecho visível"
        + ("" if CONCRETE_RE.search(window) else ", nada checável antes do toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FAIL", f"{len(tags)} tags, acima do limite de {HASHTAG_LIMIT} do Instagram. "
                                "Tag depois da quinta não conta e o bloco parece velho")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "WARN", f"{len(tags)} tags, no limite, e "
                                f"{len(filler)} delas genéricas. Gaste as cinco em temas")
    elif filler:
        add("HASHTAGS", "WARN", f"{len(tags)} tags, {len(filler)} delas genéricas "
                                f"({', '.join(filler[:3])}). Essas não descrevem nada")
    else:
        add("HASHTAGS", "PASS", f"{len(tags)} tag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("TAG PLACEMENT", "PASS", "sem tags para posicionar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("TAG PLACEMENT", "WARN", "tem hashtag no trecho visível, "
                                     "gastando espaço do feed com uma etiqueta")
    else:
        add("TAG PLACEMENT", "PASS", "as tags ficam depois do corte")

    add("LINKS", "WARN" if links else "PASS",
        f"{len(links)} link(s) na legenda, e legenda não é clicável. "
        f"Leva para a bio ou para a DM" if links else "nenhum link morto no texto")

    if len(asks) == 1:
        add("ONE ASK", "PASS", f"um pedido: {asks[0]}")
    elif not asks:
        add("ONE ASK", "WARN", "nenhum pedido. Decida para que serve esse post")
    else:
        add("ONE ASK", "WARN", f"{len(asks)} pedidos ({', '.join(asks)}). "
                               "Dois pedidos é o mesmo que nenhum")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "WARN" if density > 4 else "PASS",
        f"{len(emoji)} emoji, {density:.1f} a cada 100 caracteres"
        + (", parece enfeite" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "PASS" if not missing else ("WARN" if found else "FAIL")
        add("SEARCH TERMS", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} no trecho visível" if found else "")
            + (f". Faltando: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FAIL")
    warns = sum(1 for c in checks if c["status"] == "WARN")
    verdict = "CORRIGIR" if fails else ("REVISAR" if warns else "PRONTA")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


STATUS = {"PASS": "OK", "WARN": "AVISO", "FAIL": "FALHA"}
CHECK_LABELS = {"LENGTH": "TAMANHO", "FIRST LINE": "PRIMEIRA LINHA",
                "HOOK IS CONCRETE": "GANCHO CONCRETO", "HASHTAGS": "HASHTAGS",
                "TAG PLACEMENT": "POSIÇÃO DAS TAGS", "LINKS": "LINKS", "ONE ASK": "UM PEDIDO",
                "EMOJI": "EMOJI", "SEARCH TERMS": "TERMOS DE BUSCA"}


def render(a, out=sys.stdout):
    head = (f"LINT DE LEGENDA  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} pedido(s)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {STATUS[c['status']]:<5} {CHECK_LABELS[c['check']]:<17} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDITO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa uma legenda de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo da legenda, ou - para stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caracteres mostrados antes do '... mais' (padrão {TRUNCATE})")
    ap.add_argument("--keywords", default="", help="termos de busca separados por vírgula")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "PRONTA" else 1)


if __name__ == "__main__":
    main()
