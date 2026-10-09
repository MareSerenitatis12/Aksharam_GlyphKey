#!/usr/bin/env python3
from pathlib import Path
from collections import OrderedDict
from collections import defaultdict
import json, unicodedata
from aksharam_keyboard_data import BASE, GOETICS, COURTS, THIRD, TRANSFORMATIONS, FIRST_SPELLS, BRAILLE

BUILD=Path(__file__).resolve().parents[1]
ROOT=BUILD.parent
SRC=BUILD/'src'
PACKAGE=BUILD/'package'
GENERATED=BUILD/'generated'
KMN=GENERATED/'aksharam_glyphkey.kmn'
KPS=PACKAGE/'aksharam_glyphkey.kps'
REPORT=GENERATED/'registry_report.json'
SELMAP=PACKAGE/'selection_math_map.json'
GENERATED.mkdir(parents=True,exist_ok=True)
PACKAGE.mkdir(parents=True,exist_ok=True)
VS={'\ufe0e','\ufe0f'}
TEXT_PRESENTATION=set('♀♂♈♉♊♋♌♍♎♏♐♑♒♓⚛⛎✡❄')

def norm(s):
    s=unicodedata.normalize('NFC',s.strip().replace('`',''))
    return ''.join(c for c in s if c not in VS).replace(' ','')

def text_presentation(s):
    return ''.join(c+'\ufe0e' if c in TEXT_PRESENTATION else c for c in s)

def Q(s):
    s=text_presentation(s)
    if "'" not in s:return "'"+s+"'"
    return ' '.join('U+0027' if c=="'" else "'"+c+"'" for c in s)

# Executable keyboard law is loaded only from static Python data in build/src/.
base=OrderedDict((k,norm(v)) for k,v in BASE.items())
assert len(base)==26
goetic_set={'⏣','⬡','✡','⚝','❂','ꙮ','❈','⧗','⊛','❄','⚛','⌬'}
goetics=[(norm(g),n,p,norm(m)) for g,n,p,m in GOETICS]
assert len(goetics)==12
goetic_math={g:m for g,_,_,m in goetics if m}
courts=[(norm(g),norm(pair),ph,norm(m)) for g,pair,ph,m in COURTS]
assert len(courts)==144
assert all(len(pair)==2 and all(x in goetic_set for x in pair) for _,pair,_,_ in courts)
court_by_pair=OrderedDict((pair,g) for g,pair,_,_ in courts)
court_reverse=OrderedDict((g,pair) for g,pair,_,_ in courts)
court_math={g:m for g,_,_,m in courts if m}
third=[(norm(pair),norm(result),ph) for pair,result,ph in THIRD]
assert len(third)==24
third_map=OrderedDict((pair,result) for pair,result,_ in third)
third_reverse=OrderedDict()
for pair,result,_ in third: third_reverse.setdefault(result,pair)
raw=[dict(r) for r in TRANSFORMATIONS]

canon=[]; exact=set()
for r in raw:
    k=(r['english'],r['first'],r['second'],r['third'],r['whole'])
    if k not in exact:exact.add(k);canon.append(r)

# Duplicate input rows compile once. Ambiguous same-input/different-output rows are reported,
# not multiplied into contradictory Keyman rules.
trigger_dest=OrderedDict(); trigger_conflicts=[]
for r in canon:
    e,d=r['english'],r['whole']
    if e not in trigger_dest:trigger_dest[e]=d
    elif trigger_dest[e]!=d:trigger_conflicts.append(dict(english=e,existing=trigger_dest[e],alternate=d,line=r['line']))
row_by_english=OrderedDict()
for r in canon: row_by_english.setdefault(r['english'],r)
whole_from_third=OrderedDict(); source_conflicts=[]
for r in canon:
    p,d=r['third'],r['whole']
    if not p or p==d:continue
    if p not in whole_from_third:whole_from_third[p]=d
    elif whole_from_third[p]!=d:source_conflicts.append(dict(source=p,existing=whole_from_third[p],alternate=d,english=r['english'],line=r['line']))

# One typed event traverses Second -> Third -> registered Whole exactly once.
def suffix_once(s,m):
    for p,d in sorted(m.items(),key=lambda kv:(-len(kv[0]),kv[0])):
        if s.endswith(p):return s[:-len(p)]+d
    return s
def stages(s):
    # Structural writing performs Second then Third only. Whole is lexical and
    # is emitted only when a registered access sequence reaches its terminal.
    return suffix_once(suffix_once(s,court_by_pair),third_map)

char_out={c:base[c.upper()] for c in 'abcdefghijklmnopqrstuvwxyz'}
char_out.update({':':'∷','→':'🡢',' ':'𑁦','𑁦':'𑁦','-':'⋯','_':'…',"'":'𝇍'})
key_of={c:f'K_{c.upper()}' for c in 'abcdefghijklmnopqrstuvwxyz'}
key_of.update({':':'SHIFT K_COLON','→':'ALT SHIFT K_4',' ':'K_SPACE','𑁦':'K_SPACE','-':'K_HYPHEN','_':'SHIFT K_HYPHEN',"'":'K_QUOTE'})

# Prefix-state compiler. Visible Aksharam follows ordinary structural writing while
# letters are still being typed. A registered Whole (or First-Spell stopping body)
# is committed only when a non-letter boundary is typed.
supported={e:d for e,d in trigger_dest.items() if e and all(c in char_out for c in e)}
first_spells=OrderedDict((e,dict(v)) for e,v in FIRST_SPELLS.items())
for e,v in first_spells.items():
    direct=''.join(char_out[c] for c in e)
    assert direct==norm(v['first']), (e,direct,v['first'])
    natural=''
    for c in e: natural=stages(natural+char_out[c])
    assert natural==norm(v['stop']), (e,natural,v['stop'])
lexical_targets=OrderedDict(supported)
for e,v in first_spells.items(): lexical_targets[e]=norm(v['stop'])
word_states={e:(f'rw{i}',f'rw{i}d1',f'rw{i}d2',f'rw{i}d3') for i,e in enumerate(supported)}
prefixes={''}
for e in lexical_targets:
    for i in range(1,len(e)+1):prefixes.add(e[:i])
prefixes=sorted(prefixes,key=lambda x:(len(x),x))
terminal=lexical_targets
tracked={p for p in prefixes if p and (p in terminal or any(e.startswith(p) and len(e)>len(p) for e in lexical_targets))}
visible={'':''}
for p in prefixes[1:]:
    parent=p[:-1]; c=p[-1]
    visible[p]=stages(visible[parent]+char_out[c])
by_visible=defaultdict(list)
for p0 in sorted(tracked,key=lambda x:(visible[x],len(x),x)):
    by_visible[visible[p0]].append(p0)
sid={}; max_rank=0
for same in by_visible.values():
    for rank,p0 in enumerate(same): sid[p0]=f's{rank}'
    max_rank=max(max_rank,len(same))
NON='§NONE§'; sid[NON]=f's{max_rank}'
state_ids=[f's{i}' for i in range(max_rank+1)]
states=[NON]+sorted(tracked,key=lambda x:(len(x),x))

transitions=[]
for p in prefixes:
    for c in char_out:
        q=p+c
        if q in prefixes:transitions.append((p,c,q))

# Native name is itself rendered through the same lawful word-prefix mechanism where available.
def render_plain(text):
    out=''
    for word_i,w in enumerate(text.lower().split(' ')):
        if word_i:out+='𑁦'
        if w in terminal:out+=terminal[w];continue
        s=''
        for c in w:
            if c in char_out:s=stages(s+char_out[c])
        out+=s
    return out
NATIVE_NAME=render_plain('aksharam glyphkey')

L=["c Aksharam GlyphKey — generated from the two keyboard authorities only",f"store(&name) {Q(NATIVE_NAME)}","store(&keyboardversion) '3.0'","store(&targets) 'desktop'","store(&mnemoniclayout) '0'","begin Unicode > use(main)",""]
basekeys=' '.join(f'[NCAPS K_{k}]' for k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'); shiftkeys=' '.join(f'[SHIFT NCAPS K_{k}]' for k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'); capskeys=' '.join(f'[CAPS K_{k}]' for k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'); shiftcaps=' '.join(f'[SHIFT CAPS K_{k}]' for k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'); glyph_items=' '.join(Q(base[k]) for k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
L += [f"store(basekeys) {basekeys}",f"store(shiftkeys) {shiftkeys}",f"store(capskeys) {capskeys}",f"store(shiftcaps) {shiftcaps}",f"store(baseglyphs) {glyph_items}",f"store(states) {' '.join('dk('+x+')' for x in state_ids)}",""]
L += ["group(main) using keys"]

# Stateful valid transitions first. Terminal transitions replace the current visible
# registered prefix with its one-glyph Whole body; nonterminal transitions append normally.
for p,c,q0 in sorted(transitions,key=lambda x:(-len(visible[x[0]]),x[1],x[0])):
    kt=key_of[c]; kt=('NCAPS '+kt) if c in 'abcdefghijklmnopqrstuvwxyz' else kt
    tail=(f" dk({sid[q0]})" if q0 in tracked else "")
    if not p:
        L.append(f"+ [{kt}] > {Q(visible[q0])}{tail}")
    else:
        L.append(f"{Q(visible[p])} dk({sid[p]}) + [{kt}] > {Q(visible[q0])}{tail}")

# Commit complete registered words only at a non-letter boundary.
# Ordinary Backspace is deliberately excluded: it remains native deletion and never unfolds.
word_boundaries=[
    ('K_SPACE','𑁦',False),('K_TAB','⁛∷',False),('NCAPS K_ENTER','',True),('SHIFT NCAPS K_ENTER','∷⁛',True),
    ('K_0','⛎',False),('K_1','☿',False),('K_2','♀',False),('K_3','∮',False),('K_4','♂',False),
    ('K_5','♃',False),('K_6','♄',False),('K_7','⛢',False),('K_8','♆',False),('K_9','♇',False),
    ('K_NP0','⛎',False),('K_NP1','☿',False),('K_NP2','♀',False),('K_NP3','∮',False),('K_NP4','♂',False),
    ('K_NP5','♃',False),('K_NP6','♄',False),('K_NP7','⛢',False),('K_NP8','♆',False),('K_NP9','♇',False),
    ('K_NPSTAR','⨳',False),('K_NPPLUS','ॐ',False),('K_NPMINUS','⋯',False),('K_NPDOT','∷',False),('K_NPSLASH','⋇',False),
    ('K_LBRKT','༿',False),('K_RBRKT','༾',False),('SHIFT K_9','᚛',False),('SHIFT K_0','᚜',False),
    ('SHIFT K_LBRKT','꧁',False),('SHIFT K_RBRKT','꧂',False),('K_HYPHEN','⋯',False),('K_PERIOD','∷',False),
    ('SHIFT K_COLON','∷',False),('K_EQUAL','⧟',False),('K_COMMA','⊹',False),('SHIFT K_COMMA','⁖',False),
    ('SHIFT K_PERIOD','჻',False),('K_COLON','⁛',False),('K_QUOTE','𝇍',False),('SHIFT K_QUOTE','𝇎',False),
    ('K_BKSLASH','⋱',False),('SHIFT K_BKSLASH','⁞',False),('K_SLASH','⋰',False),('SHIFT K_SLASH','⁙',False),
    ('SHIFT K_1','⸭',False),('SHIFT K_HYPHEN','…',False),('SHIFT K_7','ॐ',False),('SHIFT K_8','⨳',False),
    ('SHIFT K_2','🜔',False),('SHIFT K_3','🜕',False),('SHIFT K_4','🜖',False),('SHIFT K_5','🜗',False),
    ('ALT SHIFT K_4','🡢',False),('CTRL SHIFT K_6','∵',False),('SHIFT K_6','∴',False),('K_BKQUOTE','⟠',False),('SHIFT K_BKQUOTE','࿂',False),
]
boundary_access_char={'SHIFT K_COLON':':','ALT SHIFT K_4':'→','K_SPACE':' ','K_HYPHEN':'-','SHIFT K_HYPHEN':'_','K_QUOTE':"'"}
for p0 in sorted(terminal,key=lambda x:(-len(visible[x]),-len(x),x)):
    dest=terminal[p0]
    for kt,out,emit in word_boundaries:
        access_c=boundary_access_char.get(kt)
        # Longest registered continuation wins when the apparent boundary is itself
        # part of a longer registered access trigger. K_SPACE can represent either
        # an ordinary access space or the Aksharam-space alias in a registered trigger.
        if kt=='K_SPACE' and (p0+' ' in prefixes or p0+'𑁦' in prefixes):
            continue
        if access_c and p0+access_c in prefixes:
            continue
        if p0 in supported:
            ws=word_states[p0][0]
            rhs=Q(dest)+f" dk({ws})"+(Q(out) if out else "")+(" use(emit)" if emit else "")
        else:
            rhs=Q(dest+out)+(" use(emit)" if emit else "")
        L.append(f"{Q(visible[p0])} dk({sid[p0]}) + [{kt}] > {rhs}")
# Ordinary Backspace is intentionally not mapped. Native deletion remains native deletion.
# Direct Goetic mathematical forms; any active lexical state is intentionally closed.
key_for_glyph={g:k for k,g in base.items()}
for g,_,_,m in goetics:
    if not m:continue
    k=key_for_glyph[g]
    L.append(f"any(states) + [ALT SHIFT NCAPS K_{k}] > {Q(m)}")
    L.append(f"+ [ALT SHIFT NCAPS K_{k}] > {Q(m)}")
# Primordial unfolding changes only the access office of the targeted base coordinate.
for physical, glyph in base.items():
    cell=BRAILLE[physical]
    L.append(f"{Q(glyph)} any(states) + [ALT SHIFT K_BKSP] > {Q(cell)}")
    L.append(f"{Q(glyph)} + [ALT SHIFT K_BKSP] > {Q(cell)}")
# The invariant Braille SeeD form is held on further per-glyph unfolding.
for cell in BRAILLE.values():
    L.append(f"{Q(cell)} any(states) + [ALT SHIFT K_BKSP] > {Q(cell)}")
    L.append(f"{Q(cell)} + [ALT SHIFT K_BKSP] > {Q(cell)}")
# Current-glyph unfolding. Ahead-of-cursor and arbitrary body operations use the host bridge.
for glyph, parents in list(court_reverse.items()) + list(third_reverse.items()):
    L.append(f"{Q(glyph)} any(states) + [ALT SHIFT K_BKSP] > {Q(parents)}")
    L.append(f"{Q(glyph)} + [ALT SHIFT K_BKSP] > {Q(parents)}")
# Exact registered-word unfolding. The post-fold deadkey preserves which lexical
# registration produced a shared Whole, so Alt+Backspace follows that row exactly:
# Whole -> Third -> Second -> First. Ordinary Backspace remains deletion.
single_boundary_outputs=sorted({out for _,out,_ in word_boundaries if len(out)==1})
for e in supported:
    r=row_by_english[e]
    ws,d1,d2,d3=word_states[e]
    whole,third_body,second_body,first_body=r['whole'],r['third'],r['second'],r['first']
    L.append(f"{Q(whole)} dk({ws}) + [ALT K_BKSP] > {Q(third_body)} dk({d1})")
    L.append(f"{Q(third_body)} dk({d1}) + [ALT K_BKSP] > {Q(second_body)} dk({d2})")
    L.append(f"{Q(second_body)} dk({d2}) + [ALT K_BKSP] > {Q(first_body)} dk({d3})")
    L.append(f"{Q(first_body)} dk({d3}) + [ALT K_BKSP] > {Q(first_body)} dk({d3})")
    # Alt+Space explicitly refolds from any retained depth; ordinary Space preserves depth.
    for body,state in ((whole,ws),(third_body,d1),(second_body,d2),(first_body,d3)):
        L.append(f"{Q(body)} dk({state}) + [ALT K_SPACE] > {Q(whole)} dk({ws}) '𑁦'")
    for body,state in ((third_body,d1),(second_body,d2),(first_body,d3)):
        L.append(f"{Q(body)} dk({state}) + [K_SPACE] > {Q(body)} dk({state}) '𑁦'")
    # If the user deletes a one-glyph boundary with ordinary Backspace, preserve the
    # hidden lexical-depth marker while deleting only that boundary glyph. This is deletion,
    # not unfolding; Alt+Backspace remains the sole unfolding control.
    for state in (ws,d1,d2,d3):
        for out in single_boundary_outputs:
            L.append(f"dk({state}) {Q(out)} + [K_BKSP] > dk({state})")
L += [
    "dk(ud1) + [ALT K_BKSP] > use(unfold2)",
    "dk(ud2) + [ALT K_BKSP] > use(unfold3)",
    "dk(ud3) + [ALT K_BKSP] > dk(ud3)",
    "any(states) + [ALT K_BKSP] > use(unfold1)",
    "+ [ALT K_BKSP] > use(unfold1)",
    "dk(ud1) + [ALT K_SPACE] > use(refold_space)",
    "dk(ud2) + [ALT K_SPACE] > use(refold_space)",
    "dk(ud3) + [ALT K_SPACE] > use(refold_space)",
    "any(states) + [ALT K_SPACE] > use(refold_space)",
    "+ [ALT K_SPACE] > use(refold_space)",
]

# Shift/Caps explicitly suppress folding and close current prefix state.
for k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    g=base[k]
    L += [f"any(states) + [SHIFT NCAPS K_{k}] > {Q(g)}",f"+ [SHIFT NCAPS K_{k}] > {Q(g)}",
          f"any(states) + [CAPS K_{k}] > {Q(g)}",f"+ [CAPS K_{k}] > {Q(g)}",
          f"any(states) + [SHIFT CAPS K_{k}] > {Q(g)}",f"+ [SHIFT CAPS K_{k}] > {Q(g)}"]
# Unregistered continuation: keep structural writing active but leave lexical trie until Space.
for k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    g=base[k]
    L.append(f"any(states) + [NCAPS K_{k}] > {Q(g)} dk({sid[NON]}) use(fold2m)")
# NONE continues structurally.
# Start outside any registered prefix.

# Controls, digits, keypad, punctuation. Marker-aware versions consume/reset state where needed.
L += ["any(states) + [K_TAB] > '⁛∷'","+ [K_TAB] > '⁛∷'","any(states) + [SHIFT NCAPS K_ENTER] > '∷⁛' use(emit)","+ [SHIFT NCAPS K_ENTER] > '∷⁛' use(emit)","any(states) + [ALT SHIFT K_2] > '🡡'","+ [ALT SHIFT K_2] > '🡡'","any(states) + [ALT SHIFT K_3] > '🡣'","+ [ALT SHIFT K_3] > '🡣'","any(states) + [ALT SHIFT K_4] > '🡢'","+ [ALT SHIFT K_4] > '🡢'","any(states) + [ALT SHIFT K_5] > '🡠'","+ [ALT SHIFT K_5] > '🡠'",
      "any(states) + [SHIFT K_2] > '🜔'","+ [SHIFT K_2] > '🜔'","any(states) + [SHIFT K_3] > '🜕'","+ [SHIFT K_3] > '🜕'","any(states) + [SHIFT K_4] > '🜖'","+ [SHIFT K_4] > '🜖'","any(states) + [SHIFT K_5] > '🜗'","+ [SHIFT K_5] > '🜗'","any(states) + [CTRL SHIFT K_6] > '∵'","+ [CTRL SHIFT K_6] > '∵'","any(states) + [SHIFT K_6] > '∴'","+ [SHIFT K_6] > '∴'","any(states) + [SHIFT K_8] > '⨳'","+ [SHIFT K_8] > '⨳'"]
nums={'0':'⛎','1':'☿','2':'♀','3':'∮','4':'♂','5':'♃','6':'♄','7':'⛢','8':'♆','9':'♇'}
for k,g in nums.items():L += [f"any(states) + [K_{k}] > {Q(g)} dk({sid[NON]})",f"+ [K_{k}] > {Q(g)}"]
for k,g in nums.items():L += [f"any(states) + [K_NP{k}] > {Q(g)} dk({sid[NON]})",f"+ [K_NP{k}] > {Q(g)}"]
punct=[('K_NPSTAR','⨳'),('K_NPPLUS','ॐ'),('K_NPMINUS','⋯'),('K_NPDOT','∷'),('K_NPSLASH','⋇'),('K_LBRKT','༿'),('K_RBRKT','༾'),('SHIFT K_9','᚛'),('SHIFT K_0','᚜'),('SHIFT K_LBRKT','꧁'),('SHIFT K_RBRKT','꧂'),('K_HYPHEN','⋯'),('K_PERIOD','∷'),('SHIFT K_COLON','∷'),('K_EQUAL','⧟'),('K_COMMA','⊹'),('SHIFT K_COMMA','⁖'),('SHIFT K_PERIOD','჻'),('K_COLON','⁛'),('K_QUOTE','𝇍'),('SHIFT K_QUOTE','𝇎'),('K_BKSLASH','⋱'),('SHIFT K_BKSLASH','⁞'),('K_SLASH','⋰'),('SHIFT K_SLASH','⁙'),('SHIFT K_1','⸭'),('SHIFT K_HYPHEN','…'),('SHIFT K_7','ॐ'),('K_BKQUOTE','⟠'),('SHIFT K_BKQUOTE','࿂')]
for k,g in punct:L += [f"any(states) + [{k}] > {Q(g)}",f"+ [{k}] > {Q(g)}"]
# Space closes lexical state unless a specific registered transition above consumed it.
L += ["dk(ud1) + [K_SPACE] > '𑁦'","dk(ud2) + [K_SPACE] > '𑁦'","dk(ud3) + [K_SPACE] > '𑁦'","any(states) + [K_SPACE] > '𑁦'","+ [K_SPACE] > '𑁦'",""]

# Stateful forward stages preserve the one hidden prefix marker.
L += ["group(fold2m)"]
for p,d in court_by_pair.items():L.append(f"{Q(p)} any(states) > {Q(d)} index(states,{len(text_presentation(p))+1}) use(fold3m)")
L.append("nomatch > use(fold3m)")
L += ["","group(fold3m)"]
for p,d in third_map.items():L.append(f"{Q(p)} any(states) > {Q(d)} index(states,{len(text_presentation(p))+1})")
L.append("nomatch > return")
L.append("")

# Non-state structural groups perform only Second and Third. Whole remains lexical.
L += ["group(fold2)"]
for p,d in court_by_pair.items():L.append(f"{Q(p)} > {Q(d)} use(fold3)")
L.append("nomatch > use(fold3)")
L += ["","group(fold3)"]
for p,d in third_map.items():L.append(f"{Q(p)} > {Q(d)}")
L.append("nomatch > return")
L.append("")

# Mathematical-body suffix groups are retained for direct internal use only.
# Alt+Shift+Enter is intentionally NOT bound to preceding context: the Legend requires host-selected glyph(s).
L += ["group(mathbody_m)"]
for g,m in list(goetic_math.items())+list(court_math.items()):L.append(f"{Q(g)} > {Q(m)}")
L.append("nomatch > return")
L += ["","group(mathbody)"]
for g,m in list(goetic_math.items())+list(court_math.items()):L.append(f"{Q(g)} > {Q(m)}")
L.append("nomatch > return")
L.append("")

# Three explicit reversible lexical levels. Depth is retained in hidden markers so
# identity stages still count as a level and a fourth Alt+Backspace is inert.
whole_to_third=OrderedDict(); third_to_second=OrderedDict(); second_to_first=OrderedDict()
for r in canon:
    if r['whole'] and r['third']: whole_to_third.setdefault(r['whole'],r['third'])
    if r['third'] and r['second']: third_to_second.setdefault(r['third'],r['second'])
    if r['second'] and r['first']: second_to_first.setdefault(r['second'],r['first'])

L += ["group(unfold1)"]
seen_unfold1=set()
for p,d in sorted(whole_to_third.items(),key=lambda kv:(-len(kv[0]),kv[0])):
    L.append(f"{Q(p)} > {Q(d)} dk(ud1)"); seen_unfold1.add(p)
# Natural Third bodies without a registered Whole can still unfold lawfully to their pair.
for p,d in sorted(third_reverse.items(),key=lambda kv:(-len(kv[0]),kv[0])):
    if p not in seen_unfold1:
        L.append(f"{Q(p)} > {Q(d)} dk(ud2)"); seen_unfold1.add(p)
# Natural Court bodies occupy the Second/Third visible level; first press retains the
# visible body and records that the no-op Third level has been traversed.
for p in sorted(court_reverse,key=lambda x:(-len(x),x)):
    if p not in seen_unfold1:
        L.append(f"{Q(p)} > {Q(p)} dk(ud2)"); seen_unfold1.add(p)
L.append("nomatch > return")
L += ["","group(unfold2)"]
for p,d in sorted(third_to_second.items(),key=lambda kv:(-len(kv[0]),kv[0])):
    L.append(f"{Q(p)} > {Q(d)} dk(ud2)")
for p,d in sorted(third_reverse.items(),key=lambda kv:(-len(kv[0]),kv[0])):
    if p not in third_to_second:L.append(f"{Q(p)} > {Q(d)} dk(ud2)")
L.append("nomatch > dk(ud2)")
L += ["","group(unfold3)"]
for p,d in sorted(second_to_first.items(),key=lambda kv:(-len(kv[0]),kv[0])):
    L.append(f"{Q(p)} > {Q(d)} dk(ud3)")
for p,d in sorted(court_reverse.items(),key=lambda kv:(-len(kv[0]),kv[0])):
    if p not in second_to_first:L.append(f"{Q(p)} > {Q(d)} dk(ud3)")
L.append("nomatch > dk(ud3)")
L.append("")

refold=OrderedDict()
for r in canon:
    for src in (r['first'],r['second'],r['third']):
        if src and src!=r['whole']:refold.setdefault(src,r['whole'])
L += ["group(refold_space_m)"]
for p,d in sorted(refold.items(),key=lambda kv:(-len(kv[0]),kv[0])):L.append(f"{Q(p)} > {Q(d)} '𑁦'")
L.append("nomatch > '𑁦'")
L += ["","group(refold_space)"]
for p,d in sorted(refold.items(),key=lambda kv:(-len(kv[0]),kv[0])):L.append(f"{Q(p)} > {Q(d)} '𑁦'")
L.append("nomatch > '𑁦'")
L.append("")

L += ['', 'group(emit) using keys', 'c Empty by design: passes the original control keystroke to the host application.']
KMN.write_text('\n'.join(L)+'\n',encoding='utf-8')
selection_math=OrderedDict(list(goetic_math.items())+list(court_math.items()))
(PACKAGE/'unfolding_map.json').write_text(json.dumps({'primordial':{g:BRAILLE[k] for k,g in base.items()},'courts':dict(court_reverse),'third':dict(third_reverse),'rows':list(row_by_english.values()),'first_spells':dict(first_spells)},ensure_ascii=False,indent=2),encoding='utf-8')
SELMAP.write_text(json.dumps(selection_math,ensure_ascii=False,indent=2),encoding='utf-8')
KPS.write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<Package><System><KeymanDeveloperVersion>18.0.252</KeymanDeveloperVersion><FileVersion>7.0</FileVersion></System><Options><ReadMeFile>readme.htm</ReadMeFile><WelcomeFile>welcome.htm</WelcomeFile><FollowKeyboardVersion/></Options><Info><Name>{text_presentation(NATIVE_NAME)}</Name><Description>Aksharam GlyphKey</Description><Version>3.0</Version></Info><Files><File><Name>aksharam_glyphkey.kmx</Name><Description>Aksharam GlyphKey</Description><CopyLocation>0</CopyLocation><FileType>.kmx</FileType></File><File><Name>welcome.htm</Name><Description></Description><CopyLocation>0</CopyLocation><FileType>.htm</FileType></File><File><Name>readme.htm</Name><Description></Description><CopyLocation>0</CopyLocation><FileType>.htm</FileType></File><File><Name>aksharam_selection_math.py</Name><Description>Selected Aeon mathematical-body resolver</Description><CopyLocation>0</CopyLocation><FileType>.py</FileType></File><File><Name>aksharam_selection_phonetic.py</Name><Description>Selected Aksharam Shape-of-Sound phonetic resolver</Description><CopyLocation>0</CopyLocation><FileType>.py</FileType></File><File><Name>selection_math_map.json</Name><Description>Registered mathematical bodies</Description><CopyLocation>0</CopyLocation><FileType>.json</FileType></File><File><Name>aksharam_host_controls.py</Name><Description>Aksharam 3.0 host unfolding controls</Description><CopyLocation>0</CopyLocation><FileType>.py</FileType></File><File><Name>unfolding_map.json</Name><Description>Aksharam 3.0 host unfolding controls</Description><CopyLocation>0</CopyLocation><FileType>.json</FileType></File><File><Name>xbindkeys.aksharam</Name><Description>Linux selection bindings</Description><CopyLocation>0</CopyLocation><FileType>.aksharam</FileType></File><File><Name>start_selection.sh</Name><Description>Selection binding launcher for Linux</Description><CopyLocation>0</CopyLocation><FileType>.sh</FileType></File></Files><Keyboards><Keyboard><Name>{text_presentation(NATIVE_NAME)}</Name><ID>aksharam_glyphkey</ID><Version>3.0</Version><Languages><Language ID="und">Aksharam</Language></Languages></Keyboard></Keyboards><Strings/></Package>''',encoding='utf-8')

# Static conformance: each non-conflicting supported trigger is terminal by construction.
validation=[dict(english=e,whole=d,terminal=(e in terminal),visible=visible.get(e)) for e,d in supported.items()]
REPORT.parent.mkdir(exist_ok=True)
REPORT.write_text(json.dumps({'native_name':NATIVE_NAME,'base_coordinates':len(base),'goetics':len(goetics),'courts':len(courts),'third_law_pairs':len(third),'raw_rows':len(raw),'deduped_rows':len(canon),'distinct_triggers':len(trigger_dest),'supported_triggers':len(supported),'prefix_states':len(states),'transitions':len(transitions),'source_conflicts':source_conflicts,'trigger_conflicts':trigger_conflicts,'validation':validation},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'generated {KMN.name}: {KMN.stat().st_size} bytes, {len(L)} lines')
print(f'name: {NATIVE_NAME}')
print(f'triggers: {len(supported)}/{len(trigger_dest)} supported; prefix states: {len(states)}; transitions: {len(transitions)}')
print(f'conflicts retained once: source={len(source_conflicts)} trigger={len(trigger_conflicts)}')
