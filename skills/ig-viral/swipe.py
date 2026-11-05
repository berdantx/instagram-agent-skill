#!/usr/bin/env python3
"""
swipe.py - rank reels you collected by how far they beat their own account,
name the hook formula each one used, and write the swipe file.

The point of this script is one correction: raw views are not evidence. A
2,000,000-follower account doing 400,000 views had a quiet day. A 4,000-
follower account doing 400,000 views found something. This ranks on the
multiple over the account's own baseline, which is the only version of
"went viral" that tells you anything you can copy.

Input is a tab-separated file you fill in while you browse, one reel per row,
with a header line naming the columns:

    account   followers   median   views    hook
    @someone  48000       11000    412000   nobody tells you your first 30 flop

`median` is that account's typical recent views and is the better baseline.
If you only have `followers`, leave median out and the script says so.
`hook` is the first line of the reel, spoken or on screen, in their words.

Column names can also be in Portuguese (conta, seguidores, mediana, views ou
visualizacoes, gancho), and counts can be written "48k", "1,2 mi" or "12 mil".
Hooks in Portuguese are classified with the `pt.match` regexes in hooks.json
and shown with the Portuguese formula name. Output is in Portuguese.

Usage / Uso
  python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
  python3 swipe.py captured.tsv
  python3 swipe.py captured.tsv --out ~/.claude/instagram/swipe.md
  python3 swipe.py captured.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")
WORD_RE = re.compile(r"(?:R?\$\s?)?\d+(?:[.,]\d+)*(?:%|k\b)?|[^\W\d_]+(?:['’-][^\W\d_]+)*")
UNCLASSIFIED = "não classificado"

try:                                              # optional: score the hooks too
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
    from hookscore import detect_lang             # noqa: E402
except Exception:                                 # ig-viral copied on its own
    score_hook = None

    def detect_lang(text):
        low = text.lower()
        pt = len(re.findall(r"[ãõçáéíóúâêô]|\b(?:que|n[aã]o|voc[eê]|pra|de|um|uma|eu|meu|isso)\b", low))
        en = len(re.findall(r"\b(?:the|and|you|to|of|that|it|is|my|your|i)\b", low))
        return "en" if en > pt else "pt"


def load_formulas(path):
    """{"en": [(id, name, regex)...], "pt": [...]} in classify_order."""
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    out = {"en": [], "pt": []}
    for i in order:
        h = by_id.get(i)
        if not h:
            continue
        out["en"].append((h["id"], h["name"], re.compile(h["match"], re.IGNORECASE)))
        pt = h.get("pt") or {}
        if pt.get("match"):
            out["pt"].append((h["id"], pt.get("name") or h["name"],
                              re.compile(pt["match"], re.IGNORECASE)))
    return out


def classify(hook, formulas, lang="en"):
    if not formulas:
        return None, UNCLASSIFIED
    for fid, name, pattern in formulas.get(lang) or formulas["en"]:
        if pattern.search(hook):
            return fid, name
    return None, UNCLASSIFIED


ALIASES = {"conta": "account", "perfil": "account", "seguidores": "followers",
           "mediana": "median", "visualizacoes": "views", "visualizações": "views",
           "gancho": "hook"}


def parse_count(cell):
    """'48000', '48.000', '48,000', '48k', '1,2 mi', '1.2M', '12 mil' -> int.
    Returns None for an empty cell and raises ValueError for garbage."""
    raw = (cell or "").strip().lower().replace(" ", "")
    if not raw:
        return None
    m = re.fullmatch(r"([\d.,]+)(k|mil|m|mi|mm|milh(?:ão|ao|ões|oes))?", raw)
    if not m:
        raise ValueError(cell)
    num, suffix = m.groups()
    if suffix:
        mult = 1_000 if suffix in ("k", "mil") else 1_000_000
        return int(round(float(num.replace(",", ".")) * mult))
    return int(re.sub(r"[.,]", "", num))


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [ALIASES.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for n, line in enumerate(body, 2 if cols is head else 1):
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        try:
            r["views"] = parse_count(r.get("views", "")) or 0
        except ValueError:
            print(f"aviso: linha {n} ignorada, views ilegível: {r.get('views')!r}", file=sys.stderr)
            continue
        for k in ("followers", "median"):
            try:
                r[k] = parse_count(r.get(k, ""))
            except ValueError:
                print(f"aviso: linha {n}, {k} ilegível ({r.get(k)!r}), tratado como vazio",
                      file=sys.stderr)
                r[k] = None
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    for r in rows:
        if r.get("median"):
            base, kind = r["median"], "median"
        elif r.get("followers"):
            base, kind = r["followers"], "followers"
        else:
            base, kind = 0, None
        r["baseline"], r["baseline_kind"] = base, kind
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["lang"] = detect_lang(r["hook"])
        r["formula_id"], r["formula"] = classify(r["hook"], formulas, r["lang"])
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    kinds = {r["baseline_kind"] for r in rows if r["baseline_kind"]}
    by_followers = sum(1 for r in rows if r["baseline_kind"] == "followers")
    if kinds == {"median"}:
        baseline = "mediana da conta"
    elif kinds == {"followers"}:
        baseline = "seguidores"
    elif kinds:
        # Mixing the two baselines makes the multiples incomparable. Say so.
        baseline = f"misto ({by_followers} de {len(rows)} por seguidores)"
    else:
        baseline = "nenhuma"
    return {
        "baseline": baseline,
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == UNCLASSIFIED),
    }


def br(n):
    """12345 -> '12.345', the Brazilian thousands separator."""
    return f"{n:,}".replace(",", ".")


def render(a, out=sys.stdout):
    head = (f"SWIPE FILE  ·  {a['n']} reels  ·  {a['accounts']} contas  ·  "
            f"base: {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        mark = "*" if r.get("baseline_kind") == "followers" and a["baseline"].startswith("misto") else " "
        print(f"  {mult:>7}{mark} gancho {score:>3}  {fid} {r['formula'][:24]:<24} "
              f"{r.get('account', '')[:16]:<16} {br(r['views']):>9}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("O QUE ESTÁ FUNCIONANDO NESTE LOTE", file=out)
    if a["top_formulas"]:
        print("  terço de cima:     "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  nota do gancho:    em cima {a['top_hook_score']:.0f}  "
              f"vs embaixo {a['bottom_hook_score']:.0f}", file=out)
    print(f"  tamanho do gancho: em cima {a['top_words']} palavras  "
          f"vs embaixo {a['bottom_words']} palavras", file=out)
    print(f"  não classificados: {a['unclassified']} de {a['n']}. Leia esses à mão, "
          "é ali que mora a fórmula que você ainda não tem.", file=out)
    if a["baseline"].startswith("misto"):
        print("  * múltiplo calculado sobre seguidores, não sobre a mediana. Não compare "
              "direto com os outros.", file=out)
    print("\n  Lote coletado à mão é indício, não prova. Doze reels não mostram nada;\n"
          "  quarenta em seis contas mostram alguma coisa. Colete mais antes de acreditar.\n",
          file=out)


def to_markdown(a):
    lines = ["# Swipe file", "",
             f"{a['n']} reels em {a['accounts']} contas. "
             f"Ranqueados pelo múltiplo sobre a base: {a['baseline']}.", ""]
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        kind = {"median": "mediana", "followers": "seguidores"}.get(r["baseline_kind"], "nenhuma")
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- views: {br(r['views'])}  base ({kind}): {br(r['baseline'])}",
                  f"- nota do gancho: {r['hook_score']}  palavras: {r['words']}",
                  f"- gancho: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Ranqueia reels coletados pelo múltiplo fora da curva.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo TSV, ou - para stdin")
    ap.add_argument("--hooks", default=HOOKS, help="caminho do ig-reel/hooks.json")
    ap.add_argument("--out", help="também grava o swipe file em markdown aqui")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("nenhuma linha utilizável. Precisa de um arquivo separado por tab com pelo "
              "menos views e gancho.", file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("nota: hooks.json não encontrado, fórmulas sem nome. Passe --hooks.", file=sys.stderr)
    if score_hook is None:
        print("nota: hookscore.py não importável, notas de gancho puladas.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"gravado em {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
