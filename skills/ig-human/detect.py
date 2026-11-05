#!/usr/bin/env python3
"""
detect.py - painel de cinco checagens que mede o quanto um rascunho parece
escrito por máquina.

O que é:  cinco heurísticas locais, modeladas nos sinais que os detectores
públicos de IA medem: variação no tamanho das frases, concretude, vocabulário
de clichê, digital tipográfica e voz. Tudo é calculado na sua máquina, só a
partir do texto. Nada é enviado.

O que NÃO é:  GPTZero, Originality, Copyleaks, Winston ou Turnitin. Não chama
essas APIs e não promete o veredito delas. Pega o que todos eles olham, e por
isso corrigir costuma mexer nos números deles também. A única promessa
honesta é a desta linha.

Funciona em português e inglês. O idioma é detectado sozinho (ou force com
--lang). Em PT, a checagem de VOZ conta marcas de fala ("tá", "pra", "né",
"a gente") no lugar das contrações do inglês.

Cada checagem devolve uma nota HUMANA de 0 a 100. Mais alto é melhor.

Uso
  python3 detect.py rascunho.txt
  pbpaste | python3 detect.py -
  python3 detect.py rascunho.txt --json
  python3 detect.py antes.txt depois.txt      # compara dois rascunhos
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")
sys.path.insert(0, HERE)
from humanize import detect_lang, load_lexicon, term_pattern  # noqa: E402

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
NUMBERS = re.compile(r"\b\d[\d,.]*%?\b|\$\d")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÀ-ÖØ-Þ][a-zß-öø-ÿ]{2,}\b", re.MULTILINE)

# Contrações no inglês; marcas de fala no português. As duas medem a mesma
# coisa: texto escrito como se fala, e não como redação.
INFORMAL = {
    "en": re.compile(r"\b\w+['’](?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE),
    "pt": re.compile(r"\b(?:t[aá]|t[oô]|tava|tamo|pra|pro|pras|pros|n[eé]|c[eê]|oc[eê]|"
                     r"num|numa|dum|duma|da[ií]|a[ií]|tipo|bora|vamo|cad[eê]|a gente|"
                     r"galera|beleza|valeu|olha|sacou|entendeu)\b", re.IGNORECASE),
}
PRONOUNS = {
    "en": re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE),
    "pt": re.compile(r"\b(?:eu|me|mim|meu|minha|meus|minhas|comigo|n[oó]s|nosso|nossa|"
                     r"nossos|nossas|a gente|voc[eê]s?|c[eê]|te|ti|teu|tua|contigo|"
                     r"seu|sua|seus|suas)\b", re.IGNORECASE),
}


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Map value onto 0-100 where `human` -> 100 and `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """Humans vary sentence length hard. Models write even."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "curto demais para julgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variação {cv:.2f} em {len(lens)} frases (bom: 0.55+)"


def check_specificity(text):
    """Numbers, names and concrete nouns. Slop is abstract."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais para julgar"
    per100 = 100 / len(w)
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} marcas concretas, {density:.1f} a cada 100 palavras (bom: 4+)"


def check_slop(text, lex):
    """Stock vocabulary density against the lexicon."""
    w = words(text)
    if not w:
        return 50.0, "vazio"
    hits, found = 0, []
    # Longest first, and each match is consumed, the same order humanize.py
    # replaces in. Otherwise "delve into" also counted as "delve".
    work = text
    for entry in sorted(lex["words"] + lex["phrases"], key=lambda e: len(e["find"]), reverse=True):
        pattern = term_pattern(entry["find"])
        n = len(pattern.findall(work))
        if n:
            hits += n
            found.append(entry["find"].rstrip(","))
            work = pattern.sub(" \x00 ", work)
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} clichês, {density:.1f} a cada 100 palavras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Characters a phone keyboard does not produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisível, {em} travessão, {curly} aspas curvas, "
              f"{ellip} reticências, {nbsp} espaço rígido")
    return score, detail


def check_voice(text, lex):
    """Contractions, person, and the shapes models default to."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais para julgar"
    lang = lex.get("lang", "en")
    per100 = 100 / len(w)
    contractions = len(INFORMAL[lang].findall(text)) * per100
    person = len(PRONOUNS[lang].findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(contractions, human=3.0, machine=0.0) * 0.35
             + scale(person, human=8.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("uniform-bullets")
    marker = "contrações" if lang == "en" else "marcas de fala"
    detail = (f"{contractions:.1f} {marker}, {person:.1f} pronomes pessoais "
              f"a cada 100 palavras, {tells} padrão(ões) estrutural(is)")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["BURSTINESS", "SPECIFICITY", "SLOP DENSITY", "FINGERPRINT", "VOICE"]
LABELS = {"BURSTINESS": "VARIAÇÃO", "SPECIFICITY": "ESPECIFICIDADE",
          "SLOP DENSITY": "CLICHÊS", "FINGERPRINT": "DIGITAL", "VOICE": "VOZ"}


def run(text, lex):
    results = {}
    results["BURSTINESS"] = check_burstiness(text)
    results["SPECIFICITY"] = check_specificity(text)
    results["SLOP DENSITY"] = check_slop(text, lex)
    results["FINGERPRINT"] = check_fingerprint(text)
    results["VOICE"] = check_voice(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # The weakest check drags the verdict: a detector only needs one signal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "APROVADO" if overall >= 70 and min(scores) >= 55 else (
        "REVISAR" if overall >= 50 else "SINALIZADO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PAINEL DE DETECÇÃO DE IA" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {LABELS[name]:<14} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<14} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA HUMANA':<14} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "APROVADO":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Sinal mais fraco: {LABELS[weakest]}. Corrija esse primeiro.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Mede o quanto um rascunho parece escrito por máquina.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou - para stdin")
    ap.add_argument("compare", nargs="?", help="segundo arquivo, para ver antes/depois")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    ap.add_argument("--lang", choices=["auto", "pt", "en"], default="auto",
                    help="idioma do texto (padrão: detecta sozinho)")
    args = ap.parse_args()

    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    lexes = []
    for name, text in targets:
        lang = detect_lang(text) if args.lang == "auto" else args.lang
        lex = load_lexicon(args.lexicon, lang)
        lexes.append(lex)
        results, overall, verdict = run(text, lex)
        payload.append({
            "lang": lang,
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p, lex in zip(targets, payload, lexes):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "APROVADO" else 1)


if __name__ == "__main__":
    main()
