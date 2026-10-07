#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import time
from collections import OrderedDict

# Standalone build-local Shape-of-Sound map copied into the keyboard package.
# No runtime dependency on translated bodies/, Markdown, or project source files.
SHAPE_PHONETICS = OrderedDict([('♈', 'ash'),
 ('♉', 'us'),
 ('♊', 'eri'),
 ('♋', 'en'),
 ('♑', 'on'),
 ('♍', 'yam'),
 ('♎', 'me'),
 ('♏', 'da'),
 ('♐', 'ka'),
 ('♌', 'myr'),
 ('♒', 'nyx'),
 ('♓', 'ai'),
 ('⏣', 'fe'),
 ('⬡', 'al'),
 ('✡', 'abd'),
 ('⚝', 'ahn'),
 ('❂', 'el'),
 ('ꙮ', 'so'),
 ('❈', 'ot'),
 ('⧗', 'dr'),
 ('⊛', 'ri'),
 ('❄', 'ek'),
 ('⚛', 'av'),
 ('⌬', 'ig'),
 ('އ', 'ahl'),
 ('ށ', 'uhh'),
 ('ނ', 'ehr'),
 ('ރ', 'ish'),
 ('ޱ', 'ora'),
 ('ޅ', 'ahm'),
 ('ކ', 'ke'),
 ('ވ', 'ehm'),
 ('މ', 'ahd'),
 ('ފ', 'fur'),
 ('ދ', 'a'),
 ('ތ', 'era'),
 ('ᛁ', 'kur'),
 ('ᛂ', 'lur'),
 ('⌑', 'ahr'),
 ('ᛄ', 'in'),
 ('ᛇ', 'na'),
 ('ᛉ', 'fel'),
 ('ᛊ', 'har'),
 ('ᛋ', 'mer'),
 ('ᛌ', 'o'),
 ('ᛍ', 'pe'),
 ('ᛎ', 'zhi'),
 ('ᛏ', 'cl'),
 ('ᚠ', 'hr'),
 ('ᚢ', 'kr'),
 ('ᚦ', 'vr'),
 ('ᚨ', 'py'),
 ('ᚱ', 'oa'),
 ('ᚲ', 'lc'),
 ('ᚷ', 'nu'),
 ('ᚹ', 'st'),
 ('ᚺ', 'or'),
 ('ᚾ', 'bon'),
 ('ᚿ', 'ti'),
 ('ᛃ', 'fa'),
 ('≾', 'abd'),
 ('᭨', 'ym'),
 ('᭡', 'oh'),
 ('⛧', 'zhi'),
 ('𝀖', 'ol'),
 ('༺', 'i'),
 ('᭢', 're'),
 ('⦾', 'se'),
 ('⦽', 'u'),
 ('𝀵', 'fay'),
 ('𝀟', 'ha'),
 ('༻', 'ps'),
 ('ⴰ', 'era'),
 ('ⴱ', 'tar'),
 ('ⴳ', 'ghe'),
 ('ⴷ', 'rel'),
 ('ⴼ', 'ful'),
 ('ⴽ', 'ker'),
 ('ⵀ', 'hoh'),
 ('ⵃ', 'hr'),
 ('ⵄ', 'ar'),
 ('ⵇ', 'ay'),
 ('ⵉ', 'urn'),
 ('ⵊ', 'je'),
 ('ꠇ', 'fi'),
 ('ꠈ', 'lun'),
 ('ꠉ', 'aru'),
 ('ꠊ', 'es'),
 ('⎉', 'os'),
 ('ꠌ', 'ahm'),
 ('ꠍ', 'ti'),
 ('ꠎ', 'ey'),
 ('ꠏ', 'sih'),
 ('ꠐ', 'hri'),
 ('ꠑ', 'yo'),
 ('ꠒ', 'thal'),
 ('🝏', 'e'),
 ('🜁', 'se'),
 ('🜃', 'lin'),
 ('🜄', 'bri'),
 ('🜅', 'inn'),
 ('🜆', 'subh'),
 ('🜇', 'wel'),
 ('🜈', 'm'),
 ('🜉', 'esh'),
 ('🜊', 'so'),
 ('🜋', 'rhu'),
 ('🜌', 'del'),
 ('𒀀', 'na'),
 ('𒀭', 'ur'),
 ('𒁀', 'nih'),
 ('𒂊', 'azh'),
 ('𒄑', 'hol'),
 ('𒅆', 'gur'),
 ('𒆠', 'ves'),
 ('𒇽', 'rim'),
 ('𒉌', 'dem'),
 ('𒊕', 'oth'),
 ('𒋗', 'izh'),
 ('𒌋', 'shu'),
 ('ⶀ', 'ia'),
 ('ⶁ', 'zoh'),
 ('ⶂ', 'her'),
 ('ⶃ', 'druh'),
 ('ⶄ', 'fhel'),
 ('ⶅ', 'ral'),
 ('ⶆ', 'kra'),
 ('ⶇ', 'and'),
 ('ⶈ', 'deb'),
 ('ⶉ', 'kol'),
 ('ⶊ', 'fra'),
 ('ⶋ', 'us'),
 ('𐤠', 'hin'),
 ('𐤡', 'ser'),
 ('𐤢', 'ama'),
 ('𐤣', 'tohr'),
 ('𐤤', 'pel'),
 ('𐤥', 'khi'),
 ('𐤦', 'yth'),
 ('𐤧', 'mel'),
 ('𐤨', 'pha'),
 ('𐤩', 'okh'),
 ('𐤪', 'od'),
 ('𐤫', 'ume'),
 ('𐠀', 'ohm'),
 ('𐠁', 'is'),
 ('𐠂', 'ta'),
 ('𐠃', 'koh'),
 ('𐠄', 'yh'),
 ('𐠅', 'st'),
 ('𐠝', 'os'),
 ('𐠞', 'poru'),
 ('𐠈', 'orm'),
 ('𐠜', 'rev'),
 ('𐠋', 'imh'),
 ('𐠌', 'ihnj'),
 ('𐔀', 'ig'),
 ('𐔁', 'pe'),
 ('𐔂', 'du'),
 ('𐔃', 'oma'),
 ('𐔄', 'eru'),
 ('𐔅', 'ta'),
 ('𐔆', 'opa'),
 ('𐔇', 'tin'),
 ('𐔈', 'rest'),
 ('𐔉', 'sil'),
 ('𐔊', 'slun'),
 ('𐔋', 'ete'),
 ('⛎', 'zen'),
 ('☿', 'pon'),
 ('♀', 'ael'),
 ('᳀', 'gaya'),
 ('♂', 'wil'),
 ('♃', 'pay'),
 ('♄', 'ehveh'),
 ('⛢', 'ahc'),
 ('♆', 'no'),
 ('♇', 'noo'),
 ('☽', 'av'),
 ('☾', 'veh'),
 ('߷', 'th'),
 ('ཪ', 'he'),
 ('⚶', 'de'),
 ('🜚', 'pa'),
 ('🜛', 'ma'),
 ('🜗', 'in'),
 ('🜖', 'er'),
 ('🜕', 'at'),
 ('🜔', 'oo'),
 ('☽☉☾', 'regia'),
 ('𑁦', ' ')])

# First Spells retain their utterance through every lawful written transformation.
FIRST_SPELL_PHONETICS = OrderedDict([('⏣⚛⚝❂', 'eloi'),
 ('ދ𝀖', 'eloi'),
 ('❈✡☽✡⌬⧗⬡✡ꙮ♐', 'sabachtany'),
 ('🜃☽ᛃ𒀭ᚲ♐', 'sabachtany'),
 ('✡ꙮ❂♏✡', 'anima'),
 ('ᚲ❂♏✡', 'anima'),
 ('⌬♍⚛♑✡', 'culpa'),
 ('❄⏣⌬❂⊛⏣', 'decire'),
 ('𐤠𐔄ⶀ', 'decire'),
 ('⏣ꙮ⬡⏣⊛✡', 'entera'),
 ('ޅᛁⶂ', 'entera')])

# Aksharam grammar/constellations return to ordinary textual grammar for phonetic output.
# ∷ has two physical-source uses (period and colon); once written as one constellation,
# source punctuation is not recoverable, so its canonical textual return here is period.
GRAMMAR = OrderedDict([('⁛∷', '\n\n'),
 ('∷⁛', '\n\n'),
 ('༿', '['),
 ('༾', ']'),
 ('᚛', '('),
 ('᚜', ')'),
 ('꧁', '{'),
 ('꧂', '}'),
 ('∷', '.'),
 ('⧟', '='),
 ('𝇍', "'"),
 ('𝇎', '"'),
 ('჻', '>'),
 ('⁖', '<'),
 ('⊹', ','),
 ('⁛', ';'),
 ('⁙', '?'),
 ('⸭', '!'),
 ('⋱', '\\'),
 ('⋰', '/'),
 ('…', '_'),
 ('⋯', '-'),
 ('ॐ', '&'),
 ('⁞', '|'),
 ('⟠', '`'),
 ('࿂', '~'),
 ('𑁦', ' '),
 ('🡡', '↑'),
 ('🡣', '↓'),
 ('🡢', '→'),
 ('🡠', '←')])

VARIATION_SELECTORS = {chr(0xfe0e), chr(0xfe0f)}
TOKENS = sorted(
    list(FIRST_SPELL_PHONETICS.items()) + list(GRAMMAR.items()) + list(SHAPE_PHONETICS.items()),
    key=lambda kv: len(kv[0]),
    reverse=True,
)

def transform(text: str) -> str:
    clean = ''.join(ch for ch in text if ch not in VARIATION_SELECTORS)
    out=[]; i=0
    while i < len(clean):
        for token,repl in TOKENS:
            if clean.startswith(token,i):
                out.append(repl); i += len(token); break
        else:
            out.append(clean[i]); i += 1
    return ''.join(out)

def _linux_selection() -> int:
    subprocess.run(['xclip','-i','-selection','clipboard'], input='', text=True, check=False)
    subprocess.run(['xdotool','key','--clearmodifiers','ctrl+c'], check=False)
    time.sleep(0.06)
    try:
        selected=subprocess.check_output(['xclip','-o','-selection','clipboard'], text=True)
    except Exception:
        return 2
    if not selected:
        return 0
    rendered=transform(selected)
    p=subprocess.Popen(['xclip','-i','-selection','clipboard'], stdin=subprocess.PIPE, text=True)
    p.communicate(rendered)
    time.sleep(0.04)
    subprocess.run(['xdotool','key','--clearmodifiers','ctrl+v'], check=False)
    return 0

def main() -> int:
    if sys.platform.startswith('linux'):
        return _linux_selection()
    # The transformation engine itself is portable. Selection capture/replacement must be
    # installed through the host platform's Keyman integration layer on Windows/macOS.
    return 3

if __name__=='__main__':
    raise SystemExit(main())
