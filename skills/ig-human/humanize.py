#!/usr/bin/env python3
"""
humanize.py - tira a digital de máquina de um rascunho.

Três passadas, nesta ordem:

  1. INVISÍVEIS  apaga ou normaliza os caracteres que um teclado humano nunca
                 produz: zero-width joiners, word joiners, hífens suaves, BOMs,
                 caracteres de tag Unicode, espaços rígidos e estreitos. Eles
                 sobrevivem ao copiar e colar e são o sinal mais mecânico de
                 texto gerado.
  2. TIPOGRAFIA  travessão (em dash) vira vírgula, meia-risca vira hífen, aspas
                 curvas viram retas, reticências viram três pontos, marcador
                 vira hífen.
  3. LÉXICO      troca os clichês do léxico por palavras simples, mantendo
                 maiúsculas e sem mexer em URLs. Texto em português usa
                 slop.pt.json; texto em inglês usa slop.json. O idioma é
                 detectado sozinho (ou force com --lang).

Padrões estruturais ("não é só X, é Y", trincas, parede de hashtags) são
APONTADOS, nunca reescritos: mudar o formato de uma frase pede julgamento, e
isso é trabalho do modelo, não de regex.

Uso
  python3 humanize.py rascunho.txt
  python3 humanize.py rascunho.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py rascunho.txt --json
  python3 humanize.py rascunho.txt -o limpo.txt
  python3 humanize.py rascunho.txt --lang pt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")


# Palavras-função que denunciam o idioma. Empate ou texto vazio cai em PT,
# porque este fork é português primeiro.
PT_HINTS = {
    "de", "que", "não", "nao", "é", "um", "uma", "para", "pra", "com", "você",
    "voce", "eu", "os", "as", "do", "da", "dos", "das", "no", "na", "em", "por",
    "mais", "mas", "isso", "meu", "minha", "seu", "sua", "está", "tá", "foi",
    "como", "quando", "porque", "ninguém", "também", "muito", "já", "só",
    "a gente", "nós", "vocês", "ele", "ela", "tem", "ser", "sem",
}
EN_HINTS = {
    "the", "and", "is", "you", "to", "of", "that", "it", "for", "with", "this",
    "are", "was", "not", "my", "your", "but", "what", "how", "i", "we", "they",
    "have", "be", "on", "in", "at", "do", "don't", "it's", "i'm", "nobody",
}


def detect_lang(text):
    low = text.lower()
    toks = re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?", low)
    pt = sum(1 for t in toks if t in PT_HINTS)
    pt += 2 * len(re.findall(r"[ãõçáéíóúâêôà]", low)) + 3 * low.count("r$")
    en = sum(1 for t in toks if t in EN_HINTS)
    return "en" if en > pt else "pt"


def load_lexicon(path=LEX, lang="pt"):
    """slop.json traz as tabelas de invisíveis e tipografia (valem para os dois
    idiomas) e o léxico em inglês. Em PT, palavras, frases, padrões e
    conectivos vêm de slop.pt.json, ao lado de slop.json."""
    with open(path, encoding="utf-8") as fh:
        lex = json.load(fh)
    lex["lang"] = "en"
    if lang == "pt":
        pt_path = os.path.join(os.path.dirname(os.path.abspath(path)), "slop.pt.json")
        if os.path.exists(pt_path):
            with open(pt_path, encoding="utf-8") as fh:
                pt = json.load(fh)
            for key in ("words", "phrases", "structures", "splice_connectives"):
                if key in pt:
                    lex[key] = pt[key]
            lex["lang"] = "pt"
    return lex


def term_pattern(find):
    """Regex para um termo do léxico. Só põe \\b na ponta que termina em letra
    ou número: "o que vocês acham?" termina em "?" e um \\b ali nunca casaria."""
    body = re.escape(find).replace(r"\ ", r"\s+")
    left = r"\b" if re.match(r"\w", find) else ""
    right = r"\b" if re.search(r"\w$", find) else ""
    return re.compile(left + body + right, re.IGNORECASE)


def _cp(spec):
    """'U+200B' -> '\\u200b';  'U+E0000-U+E007F' -> (start, end)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Swap URLs for placeholders so no pass rewrites inside a link."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Delete or space-normalise invisible characters. Returns (text, hits)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Any remaining Cf (format) character is invisible by definition.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "outros caracteres invisíveis de formatação", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(espaço)"})
        if ch == "—":
            # " word — word " and "word—word" both collapse to a comma + space.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # used as em dash
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # A comma inserted before existing punctuation reads wrong.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def pass_lexical(text, lex):
    """Replace slop words and phrases. Longest first so phrases win."""
    hits = []
    # Protect real ellipses before anything is deleted. Protecting them after
    # meant two deleted sentences in a row ("Notion. . .") collapsed into a
    # fake "..." that then survived as one.
    text = text.replace("...", "\x00ELL\x00")
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        pattern = term_pattern(find)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(apagado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Clean up after deletions. Deleting a whole clause leaves orphaned
    # punctuation behind ("system. ." or a line that now opens on a comma),
    # and that reads worse than the slop did.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:!?]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # one space left by a deletion.
                                                      # Deeper indents are deliberate.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)      # an em dash became a comma,
                                                      # then the clause after it went
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    # Deleting the closers on both sides of a conjunction leaves it alone in
    # its own sentence ("Follow for more and tag someone!" -> "And!").
    text = re.sub(r"(?im)(^|[.!?]\s+)(?:e|and|ou|or|mas|but)\s*[.!?]+", r"\1", text)
    text = re.sub(r"(?m)[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # An em dash that became a comma, followed by a sentence connective, leaves
    # a splice ("is important, also, it's proof"). Promote it to a full stop.
    conns = lex.get("splice_connectives") or ["also", "so", "still", "basically", "in the end"]
    alt = "|".join(re.escape(c) for c in sorted(conns, key=len, reverse=True))
    text = re.sub(r",\s*(" + alt + r")\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text,
                  flags=re.IGNORECASE)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # Sentence-length uniformity is structural too.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Frases do mesmo tamanho (variação {cv:.2f})",
                "count": len(lens),
                "fix": "Quebra uma frase no meio. Deixa outra correr longa. Máquina escreve tudo igual.",
            })
    return flags


def restore_capitals(original, text):
    """Deleting an opener leaves the next word lower case.

    Only fix it for writers who capitalise their sentences in the first place:
    a deliberately lower-case voice is a style, not an artefact, and shouting
    over it would be exactly the kind of thing this script exists to stop.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*([^\W\d_])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))\s*([^\W\d_A-ZÀ-Þ])",
                  lambda m: m.group(0)[:-1] + m.group(1).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex),
        "lang": lex.get("lang", "en"),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("RELATÓRIO DO HUMANIZADOR")
    print(f"idioma: {report.get('lang', '?')}  ·  {total} marcas de máquina removidas, "
          f"{len(report['structures'])} padrões estruturais para reescrever", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISÍVEIS")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFIA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LÉXICO DE CLICHÊS")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. PADRÕES ESTRUTURAIS  (não corrigidos sozinhos, reescreva à mão)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report[k] for k in ("invisible", "typographic", "lexical", "structures")):
        head("LIMPO")
        print("  Nada para tirar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Tira a digital de máquina de um rascunho.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou - para stdin")
    ap.add_argument("-o", "--out", help="grava o texto limpo aqui em vez do stdout")
    ap.add_argument("--report", action="store_true", help="mostra o que mudou, no stderr")
    ap.add_argument("--json", action="store_true", help="emite {text, report} em JSON")
    ap.add_argument("--lexicon", default=LEX, help="caminho do slop.json")
    ap.add_argument("--lang", choices=["auto", "pt", "en"], default="auto",
                    help="idioma do texto (padrão: detecta sozinho)")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lang = detect_lang(raw) if args.lang == "auto" else args.lang
    lex = load_lexicon(args.lexicon, lang)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"gravado em {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
