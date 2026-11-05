"""
Testes de regressão das cinco ferramentas. Só biblioteca padrão.

    python3 -m unittest discover -s tests -v

Cobrem os dois idiomas: os números em inglês são os do README original (para
garantir que a adaptação não mudou o comportamento em EN) e os casos em
português pegam os bugs que motivaram a adaptação (léxico inglês aplicado em
texto PT, regex só ASCII, aberturas fracas não reconhecidas).
"""

import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
for sub in ("ig-reel", "ig-human", "ig-caption", "ig-viral"):
    sys.path.insert(0, os.path.join(SKILLS, sub))

import beats      # noqa: E402
import caption    # noqa: E402
import detect     # noqa: E402
import hookscore  # noqa: E402
import humanize   # noqa: E402
import swipe      # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hook_cases_pt import CASES  # noqa: E402

LEX = os.path.join(SKILLS, "ig-human", "slop.json")
HOOKS = os.path.join(SKILLS, "ig-reel", "hooks.json")


def clean(text, lang="auto"):
    lang = humanize.detect_lang(text) if lang == "auto" else lang
    return humanize.humanize(text, humanize.load_lexicon(LEX, lang))


class TestLanguage(unittest.TestCase):
    def test_detect(self):
        self.assertEqual(humanize.detect_lang("Ninguém te conta isso"), "pt")
        self.assertEqual(humanize.detect_lang("Perdi R$ 18 mil"), "pt")
        self.assertEqual(humanize.detect_lang("Nobody tells you that your first reels flop"), "en")
        self.assertEqual(hookscore.detect_lang("I lost $18,000 because of one missing contract."), "en")


class TestHookscore(unittest.TestCase):
    def score(self, hook):
        _, overall, verdict, flags = hookscore.run(hook)
        return round(overall, 1), verdict, flags

    def test_english_unchanged(self):
        # The numbers printed in the original README.
        self.assertEqual(self.score("Nobody tells you that your first 30 reels are supposed to flop")[0], 85.6)
        self.assertEqual(self.score("I lost $18,000 because of one missing contract.")[0], 81.4)
        self.assertEqual(self.score("Stop scrolling if you want to grow on Instagram in 2026 🔥")[0], 54.4)
        self.assertEqual(self.score("Hey guys, today I wanted to talk about content strategy")[0], 9.6)

    def test_portuguese(self):
        s, v, _ = self.score("Ninguém te conta que seus primeiros 30 reels vão flopar")
        self.assertEqual(v, "FORTE")
        s, v, flags = self.score("Oi gente, hoje eu quero falar sobre estratégia de conteúdo")
        self.assertEqual(v, "FRACO")
        self.assertTrue(any("Saudação" in f for f in flags))
        _, _, flags = self.score("Neste vídeo eu vou te mostrar como vender mais")
        self.assertTrue(any("Preâmbulo" in f for f in flags))

    def test_spoken_numbers_pt(self):
        results, _, _, _ = hookscore.run("Faturei dezoito mil reais num fim de semana")
        self.assertGreater(results["SPECIFICITY"][0], 15)

    def test_weak_opener_is_whole_word(self):
        # "so" used to match "some", "só" would match "sócio".
        _, detail = hookscore.check_frontload("Someone lost $18,000 on this", hookscore.VOCAB["en"])
        self.assertNotIn("abertura fraca", detail)
        _, detail = hookscore.check_frontload("Sócio que some custa caro", hookscore.VOCAB["pt"])
        self.assertNotIn("abertura fraca", detail)


class TestHumanize(unittest.TestCase):
    def test_pt_uses_pt_lexicon(self):
        out, rep = clean("É crucial entender isso antes de alavancar o lançamento.")
        self.assertEqual(rep["lang"], "pt")
        self.assertNotIn("important ", out)          # English replacement leaking in
        self.assertIn("importante", out)
        self.assertIn("aumentar", out)

    def test_em_dash_and_structures_pt(self):
        out, rep = clean("Não é só sobre vender, é sobre transformar — de verdade.")
        self.assertNotIn("—", out)
        self.assertTrue(any("Não é só" in s["name"] for s in rep["structures"]))

    def test_no_orphan_punctuation(self):
        out, _ = clean("Para de rolar o feed! Faturei 40 mil. Segue pra mais conteúdo e marca alguém que precisa ver isso!")
        self.assertEqual(out.strip(), "Faturei 40 mil.")

    def test_fake_ellipsis_en(self):
        out, _ = clean("We grew 40% in March. Don't sleep on this. Follow for more.", "en")
        self.assertEqual(out.strip(), "We grew 40% in March.")

    def test_real_ellipsis_kept(self):
        out, _ = clean("Espera... deu certo.")
        self.assertIn("...", out)

    def test_english_still_works(self):
        out, rep = clean("In today's fast-paced world, it's crucial to leverage every tool.")
        self.assertEqual(rep["lang"], "en")
        self.assertIn("important", out)
        self.assertIn("use", out)


class TestDetect(unittest.TestCase):
    def test_voice_pt_counts_spoken_markers(self):
        text = ("Cê tá ligado que a gente perdeu 18 mil num lançamento? Pois é. "
                "Eu fiquei três dias sem dormir pra entender o que deu errado, e no fim era "
                "uma cláusula de contrato que nem eu tinha lido direito.")
        lex = humanize.load_lexicon(LEX, "pt")
        results, _, _ = detect.run(text, lex)
        self.assertGreater(results["VOICE"][0], 55)

    def test_accented_words_are_one_word(self):
        self.assertEqual(detect.words("lançamento ação"), ["lançamento", "ação"])


class TestCaption(unittest.TestCase):
    def test_keyword_ask_pt(self):
        a = caption.analyse("Perdi R$ 18 mil por uma cláusula.\n\nComenta CONTRATO que eu te mando.")
        self.assertEqual(a["asks"], ["comentar palavra-chave"])

    def test_lowercase_is_not_a_keyword(self):
        self.assertEqual(caption.analyse("comenta aqui embaixo o que achou")["asks"], [])
        self.assertEqual(caption.analyse("comment below what you think")["asks"], [])

    def test_hashtag_cap_and_accents(self):
        a = caption.analyse("Texto.\n\n#um #dois #três #quatro #cinco #seis")
        self.assertIn("#três", a["hashtags"])
        self.assertEqual(a["verdict"], "CORRIGIR")


class TestBeats(unittest.TestCase):
    def test_pt_loop_ignores_stopwords(self):
        a = beats.analyse("Eu te mostro o contrato.\nNo fim eu te mando.")
        self.assertTrue(any(n.startswith("Sem loop") for n in a["notes"]))

    def test_money_is_one_word(self):
        self.assertEqual(beats.words("Perdi R$ 18.000 ontem"), ["Perdi", "R$ 18.000", "ontem"])


class TestSwipe(unittest.TestCase):
    def setUp(self):
        self.formulas = swipe.load_formulas(HOOKS)

    def test_pt_cases(self):
        wrong = [(h, exp, swipe.classify(h, self.formulas, "pt")[0]) for h, exp in CASES
                 if swipe.classify(h, self.formulas, "pt")[0] != exp]
        self.assertLessEqual(len(wrong), len(CASES) // 10, wrong)

    def test_pt_examples_classify_to_themselves(self):
        with open(HOOKS, encoding="utf-8") as fh:
            d = json.load(fh)
        for h in d["hooks"]:
            self.assertEqual(swipe.classify(h["pt"]["example"], self.formulas, "pt")[0], h["id"],
                             h["pt"]["example"])

    def test_parse_count(self):
        self.assertEqual(swipe.parse_count("48k"), 48000)
        self.assertEqual(swipe.parse_count("1,2 mi"), 1200000)
        self.assertEqual(swipe.parse_count("12 mil"), 12000)
        self.assertEqual(swipe.parse_count("412.000"), 412000)
        self.assertIsNone(swipe.parse_count(""))
        with self.assertRaises(ValueError):
            swipe.parse_count("x")

    def test_mixed_baseline_is_labelled(self):
        rows = [{"account": "@a", "views": 1000, "median": 100, "followers": None, "hook": "oi"},
                {"account": "@b", "views": 1000, "median": None, "followers": 500, "hook": "oi"}]
        a = swipe.analyse(rows, self.formulas)
        self.assertTrue(a["baseline"].startswith("misto"))


class TestCli(unittest.TestCase):
    def test_scripts_run(self):
        for script, args in [("ig-reel/hookscore.py", ["--hook", "Perdi R$ 18 mil numa cláusula"]),
                             ("ig-human/detect.py", ["-"]),
                             ("ig-human/humanize.py", ["-"]),
                             ("ig-caption/caption.py", ["-"]),
                             ("ig-reel/beats.py", ["-"])]:
            p = subprocess.run([sys.executable, "-I", os.path.join(SKILLS, script)] + args,
                               input="Perdi R$ 18 mil por uma cláusula que faltou no contrato.\n",
                               capture_output=True, text=True)
            self.assertIn(p.returncode, (0, 1), (script, p.stderr))
            self.assertEqual(p.stderr.count("Traceback"), 0, (script, p.stderr))


if __name__ == "__main__":
    unittest.main()
