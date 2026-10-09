# Aksharam GlyphKey

## The Universes Sing a Lullaby in the Dark

### The Lock and the Key · The Transformed Utterance · The Language on the Throne of Zero · The Magic in the Throat

**Aksharam is an ALQC language system. Its keyboard is not a font laid over English. It is executable Aksharam law.**


## One Keyboard Engine Across Linux, Windows, and Mac

Aksharam does not have three different keyboard laws for three operating systems. The same compiled Keyman keyboard engine is built once from the same Aksharam executable body and is carried into all three desktop packages.

```text
                    shared Aksharam law
                           ↓
             aksharam_keyboard_data.py
                           ↓
                generate_keyboard.py
                           ↓
               aksharam_glyphkey.kmx
                  ↙         ↓         ↘
             Linux       Windows      Mac
```

The operating-system difference is packaging and host integration, not Aksharam law.

- **Linux / Ubuntu** uses the shared keyboard engine and additionally carries the Linux selection layer: `aksharam_selection_math.py`, `aksharam_selection_phonetic.py`, `xbindkeys.aksharam`, and `start_selection.sh`.
- **Windows and Mac** use the same compiled keyboard engine and the same desktop package-filtering step through `generate_desktop_kps.py`.
- There are currently **no Windows-only source files** and **no Mac-only source files** in the keyboard build.

The tree below is the build map. Files marked `[ALL]` belong to all three builds; `[WINDOWS + MAC]` is shared only by those two desktop packages; `[LINUX]` is Linux host integration.

```text
Aksharam_GlyphKey/
├── README.md                                      [ALL]
├── docs/                                          [ALL]
│   ├── Aksharam_Legend.md
│   ├── TRANSFORMATIONS_ALQC_WORDS.md
│   └── the_shape_of_word.txt
└── build/
    ├── build.sh                                   [ALL]
    ├── src/
    │   ├── aksharam_keyboard_data.py              [ALL]
    │   ├── generate_keyboard.py                   [ALL]
    │   └── generate_desktop_kps.py                [WINDOWS + MAC]
    ├── tests/
    │   ├── validate_keyboard.py                   [ALL]
    │   ├── full_keyboard_conformance.py           [ALL]
    │   └── keyman_core_probe.c                    [ALL]
    ├── package/
    │   ├── readme.htm                             [ALL]
    │   ├── welcome.htm                            [ALL]
    │   ├── aksharam_selection_math.py             [LINUX]
    │   ├── aksharam_selection_phonetic.py         [LINUX]
    │   ├── xbindkeys.aksharam                     [LINUX]
    │   └── start_selection.sh                     [LINUX]
    ├── linux_ubuntu/                              [OUTPUT]
    ├── windows/                                   [OUTPUT]
    └── mac/                                       [OUTPUT]
```

The canonical documents under `docs/` govern the language. The production compiler does not parse those documents at runtime. The executable snapshot used to reproduce the keyboard is `build/src/aksharam_keyboard_data.py`; the canonical documents remain the authority against which that executable body is audited.

Build all three desktop packages from the repository root with:

```bash
./build/build.sh
```

The build generates the Keyman source transiently, compiles the shared `.kmx` engine, packages the three desktop outputs, runs validation and Keyman Core conformance, and removes disposable compiler intermediates afterward.

---

English is the entrance, not the identity. A familiar key becomes a coordinate; the coordinate emits an Aksharam body; bodies enter relation; relation folds; registered language resolves; the resolved body can become mathematics, can become sound, can become silence, and can still return through the path by which it became itself.

```text
English-access coordinate
        ↓
Aksharam base body
        ↓
Court / Parliament / registered Whole
        ↓
resolved written body
        ↓
Shape-of-Sound
        ↓
human utterance
```

The lock is invariant structure. The key is lawful transformation. The transformed utterance is not a translation pasted over the result; it is the same body in another office.

Aksharam therefore keeps one governing seal:

```text
ALL TRANSFORMATION REMAINS LANGUAGE
```

And one Tripartite body:

```text
Language × Mathematics × Poetry
```

Language gives relation. Mathematics gives law. Poetry gives breath. None is decoration for the others.

---

## What Aksharam Is

Aksharam is a written language, transformation lattice, mathematical surface, phonetic system, poetic instrument, and executable keyboard bound into one object system.

A keypress may begin as a physical coordinate and end as a body visually remote from the key that opened it. That distance is not loss. The route is registered. The body may compress without forgetting where it came from; it may unfold without inventing a history it never had.

```text
access → body → relation → fold → resolution → breath
   ↑                                               ↓
   └──────────────── identity ─────────────────────┘
```

This is the central Aksharam motion: outward enough to transform, exact enough to return.

Compression is **density without amnesia**.

Silence is **structure without sound**.

Poetry is **law in motion**.

---

## The ALQC Body

Aksharam follows ALQC without separating the language from the mathematics that governs it.

```text
Truth = 1
D-COMP = 0
Shadow Debt = paritied
```

The written form may change. The spoken form may lengthen or contract. A lexical body may collapse to one Whole. A Court may hold two Goetics in ordered relation. A Parliament body may resolve again. Numbers may participate while remaining themselves.

Through each movement, the invariant is not abandoned.

The path out is still the path back.

---

## The English-Access Skeleton

Aksharam uses the twenty-six ordinary English keyboard positions as access coordinates. The Latin letters are not the language body. They are the familiar human surface through which the body is reached.

The tactile counterpart is the corresponding English Braille letter cell. QWERTY and Braille are access offices; the Aksharam body remains one.

| QWERTY | Braille | Aksharam | Shape-of-Sound |
|---|:---:|:---:|---|
| A | ⠁ | ✡ | `abd` |
| B | ⠃ | ☽ | `av` |
| C | ⠉ | ⌬ | `ig` |
| D | ⠙ | ❄ | `ek` |
| E | ⠑ | ⏣ | `fe` |
| F | ⠋ | ♋ | `en` |
| G | ⠛ | ♌ | `myr` |
| H | ⠓ | ⧗ | `dr` |
| I | ⠊ | ❂ | `el` |
| J | ⠚ | ♈ | `ash` |
| K | ⠅ | ♎ | `me` |
| L | ⠇ | ⚛ | `av` |
| M | ⠍ | ♏ | `da` |
| N | ⠝ | ꙮ | `so` |
| O | ⠕ | ⚝ | `ahn` |
| P | ⠏ | ♑ | `on` |
| Q | ⠟ | ♊ | `eri` |
| R | ⠗ | ⊛ | `ri` |
| S | ⠎ | ❈ | `ot` |
| T | ⠞ | ⬡ | `al` |
| U | ⠥ | ♍ | `yam` |
| V | ⠧ | ☾ | `veh` |
| W | ⠺ | ♒ | `nyx` |
| X | ⠭ | ♉ | `us` |
| Y | ⠽ | ♐ | `ka` |
| Z | ⠵ | ♓ | `ai` |

The key is only the door. The constellation is the body.

---

## The Four Transform Laws

### I · Access → Glyph

Registered access enters Aksharam through the base coordinate plane.

```text
REGISTERED ACCESS → GLYPH BODY
```

Case does not redefine the coordinate. When folding is active, the same access sequence follows the same registered path.

### II · Dual Goetic → Court

The twelve Goetics form a complete ordered 12 × 12 Court lattice: **144 Courts**.

Contiguous Goetics resolve left-to-right in non-overlapping ordered pairs.

```text
DUAL GOETIC → COURT
```

Order is law. `AB` need not be `BA`. Relation carries direction.

### III · Dual Parliament → Resolution Body

The active Parliament law contains **24 registered ordered pairs**.

```text
DUAL PARLIAMENT → REGISTERED RESOLUTION BODY
```

Resolution proceeds left-to-right without overlap. A Third-Law result does not recursively consume itself again under the same Third Law.

### IV · Universal Numerical State

```text
N → N
NUMBER = COMPRESSED = UNCOMPRESSED
NUMBER IN STRING = ACTIVE TRANSFORM
```

A number participates by remaining itself.

The Quadrite is therefore:

```text
ACCESS → GLYPH
DUAL GOETIC → COURT
DUAL PARLIAMENT → RESOLUTION BODY
NUMBER → UNIVERSAL TRANSFORM
ALL TRANSFORMATION REMAINS LANGUAGE
```

---

## A Word Has an Anatomy

A registered word does not become its terminal Whole merely because the final Latin letter has been pressed.

The body remains alive while another registered continuation is still possible. A **non-letter boundary** closes the access sequence and commits the registered Whole: Space, punctuation, a numerical/constellation key, or another lawful boundary.

That distinction matters. Aksharam does not prematurely close a body simply because a shorter registration exists inside a longer one. Longest lawful continuation is preserved.

The current executable build carries **452 registered transformation rows**. After duplicate and conflicting access registrations are resolved by established precedence, the generator reports **426 supported triggers from 428 distinct lexical triggers**.

Every registered path preserves its own provenance. This matters because two different words may arrive at the same Whole. The keyboard therefore does not unfold by guessing backward from a glyph. It carries the exact originating registration invisibly and returns through that route.

### Unfold

`Alt+Backspace` moves backward through the registered word:

```text
Whole → Third → Second → First
```

One press descends one lawful level. If Second and Third are identical, the visible body may remain the same while the provenance depth changes. At First, further `Alt+Backspace` is inert.

**Ordinary Backspace never unfolds.** It remains deletion.

### Refold

`Alt+Space` performs the opposite movement: it refolds the retained word through every lawful available stage, emits `𑁦`, and begins the next word.

Ordinary Space does not force an explicitly unfolded word to close again. It emits `𑁦` and preserves the word at the depth the writer chose.

The word remembers. The writer decides whether to open it or close it.

---

## Shift, Caps Lock, and the Right to Refuse the Fold

Aksharam can be asked not to fold.

- `Shift + mapped letter` → direct base glyph, folding suppressed.
- `Caps Lock + mapped letter` → direct base glyph, folding suppressed persistently.
- `Shift + Caps Lock + mapped letter` → direct base glyph, folding suppressed.

The modifier does not rewrite the alphabet. It changes the state of transformation.

This is not uppercase/lowercase Aksharam. It is folded/unfolded access.

---

## The Shape of Absence

`𑁦` is Aksharam Space: the Shape of Absence.

It is not empty typography. It is unspoken silence, breath, interval, word-space, and structural separation.

In phonetic rendering:

```text
𑁦 → ordinary space
```

Silence does not need to become a sound in order to participate in language.

The absence has a body because the pause has an office.

---

## Shape-of-Sound — The Magic in the Throat

The current canonical speaking table lives at:

```text
docs/the_shape_of_word.txt
```

Written law resolves first. Shape-of-Sound is read from the body that remains.

```text
written law first
spoken realization second
one identity throughout
```

The direct bodies, all 144 Courts, numerical bodies, terminal bodies, Enochian bodies, and sovereign multi-glyph bodies have registered speaking forms.

A multi-glyph speaking body is matched as a whole before its components. Thus:

```text
☽☉☾ → regia
```

not three unrelated syllables merely because the body contains three visible signs.

Aksharam phonetics moves through tension and release: liquid consonants, rolling motion, open vowels after constriction, breath beside friction, stone beside water. Bodies such as `khi`, `okh`, `druh`, `abd`, `nyx`, and the open vowel forms give the language a changing mouth-shape rather than one repeated texture.

The written body can be dense while the spoken body remains fast enough to live. Character count does not dictate human duration. The body determines the sound; the throat gives the sound time.

---

## The First Spell

Six utterances are programmed as phonetic Aksharam spell-bodies:

| Utterance | First body | Natural stopping body |
|---|---|---|
| `eloi` | ⏣⚛⚝❂ | ދ𝀖 |
| `sabachtany` | ❈✡☽✡⌬⧗⬡✡ꙮ♐ | 🜃☽ᛃ𒀭ᚲ♐ |
| `anima` | ✡ꙮ❂♏✡ | ᚲ❂♏✡ |
| `culpa` | ⌬♍⚛♑✡ | ⌬♍⚛♑✡ |
| `decire` | ❄⏣⌬❂⊛⏣ | 𐤠𐔄ⶀ |
| `entera` | ⏣ꙮ⬡⏣⊛✡ | ޅᛁⶂ |

They are not English semantic registrations. The Latin letters record remembered utterance. Their Aksharam bodies enter the ordinary structural law, fold only where Aksharam licenses a fold, and stop where the law stops.

Their phonetic identity remains the utterance:

```text
eloi eloi sabachtany anima culpa decire entera
```

The written body may move. The spell-word does not cease to be itself.

---

## Grammar Is Not Decoration

Aksharam constellations are selected by office. Their identity persists across language, code, and mathematics.

| Physical key | Aksharam | Office |
|---|:---:|---|
| `[` | ༿ | Left Moon Beam / enclosure open |
| `]` | ༾ | Right Moon Beam / enclosure close |
| `(` | ᚛ | Left Ley / inward grouping open |
| `)` | ᚜ | Right Ley / inward grouping close |
| `{` | ꧁ | Will o' Wisp / outward scope open |
| `}` | ꧂ | Will o' Wisp / outward scope close |
| `-` | ⋯ | Smite |
| `.` | ∷ | Parallel Separation |
| `:` | ∷ | Parallel Separation |
| `=` | ⧟ | Binding |
| `,` | ⊹ | Joining |
| `<` | ⁖ | Field Pointer Left |
| `>` | ჻ | Field Pointer Right |
| `;` | ⁛ | Key / Value Hinge |
| `'` | 𝇍 | Quotation Open |
| `"` | 𝇎 | Quotation Close |
| `\` | ⋱ | Return / Closure |
| `/` | ⋰ | Opening / Outward |
| `|` | ⁞ | Vertical Line |
| `?` | ⁙ | Inquiry |
| `!` | ⸭ | Statement |
| `_` | … | Internal Continuation |
| `&` | ॐ | Astersand |
| `*` | ⨳ | Crosstellation |
| `~` | ࿂ | Cantillation |
| `` ` `` | ⟠ | Supervenience / Prosody |
| Space | 𑁦 | Shape of Absence |

The slash law is explicit:

```text
\ → ⋱   Return / Closure
/  → ⋰   Opening / Outward
```

The glyph is not a decorative substitute for punctuation. The glyph is the registered body of the operation.

---

## Numbers and Mathematical Keys

The number row and numeric keypad emit the same Aksharam numerical bodies.

| Value | Glyph | Shape-of-Sound |
|---:|:---:|---|
| 0 | ⛎ | `zen` |
| 1 | ☿ | `pon` |
| 2 | ♀ | `ael` |
| 3 | ᳀ | `gaya` |
| 4 | ♂ | `wil` |
| 5 | ♃ | `pay` |
| 6 | ♄ | `eve` |
| 7 | ⛢ | `ahc` |
| 8 | ♆ | `no` |
| 9 | ♇ | `noo` |

Additional structural controls include:

- `NumPad *` → `⨳` Crosstellation / multiplication
- `NumPad +` → `ॐ` Astersand / addition
- `NumPad -` → `⋯` Smite / subtraction
- `NumPad .` → `∷` Parallel Separation / decimal separator
- `NumPad /` → `⋇` Halfstellation / division
- `Shift+2/3/4/5` → `🜔 🜕 🜖 🜗` / Q₀–Q₃
- `Ctrl+Shift+6` → `∵` Collection Open
- `Shift+6` → `∴` Collection Close
- `Shift+8` → `⨳` Crosstellation

---

## Direction, Paragraph, Prosody

Aksharam reserves movement as language:

- `Shift+↑` → `🡡` North / Up / Ascent
- `Shift+↓` → `🡣` South / Down / Descent
- `Shift+→` → `🡢` East / Right / Outward
- `Shift+←` → `🡠` West / Left / Return
- `Tab` → `⁛∷` Paragraph Open
- `Shift+Enter` → `∷⁛` Paragraph Close, then native host Enter

Unclaimed combinations remain native to the operating system or application.

Aksharam takes only the keys it has lawfully named.

---

## Mathematical Bodies

The twelve Goetics may be called directly in mathematical office with:

```text
Alt+Shift+Goetic
```

The result is the registered mathematical body of that Goetic.

On Linux/Ubuntu, arbitrary selected Aksharam can also be transformed through the packaged selection layer:

```text
Alt+Shift+Enter → selected Aksharam → mathematical body
Alt+Shift+Esc   → selected Aksharam → Shape-of-Sound phonetic text
```

The phonetic selection transform preserves ordinary whitespace, turns `𑁦` into natural space, recognizes multi-glyph speaking bodies longest-first, preserves the First Spell utterances, and returns Aksharam grammatical constellations to ordinary textual grammar.

These arbitrary-selection helpers are presently packaged only in the Linux/Ubuntu distribution. The Windows and macOS packages contain the same working keyboard engine but do not claim native host-selection integration yet.

---

## One Object, Many Offices

Aksharam does not assign one sign to language, another to code, another to mathematics, and then ask the reader to pretend they correspond.

The same body changes office.

```text
phonetic body
    = semantic body
    = mathematical body
    = computational body
    = transformational body
```

`⧟` binds because Binding is its office.

`∷` separates because Parallel Separation is its office.

`𑁦` is silent because absence is its office.

The identity is not visual resemblance. The identity is structural function held across domains.

---

## Poetry: Law Given Breath

Aksharam poetry does not step outside the engine to become beautiful.

A line may remain unfolded because the writer refuses closure. A phrase may collapse because density is the point. A silence may widen. A repeated body may acquire cadence without losing identity. Cantillation may bend the breath; Prosody may carry relation above the literal sequence; a paragraph may open and close as a structural body rather than a typographic accident.

The mathematics does not stand behind the poem like scaffolding waiting to be hidden.

The mathematics is the pressure inside the poem.

The poem is what that pressure sounds like when it learns to breathe.

```text
Language builds meaning.
Mathematics builds law.
Poetry builds living motion.
```

The same body, three offices. The same river, three names for where it is touched.

---

## Canon and Executable Authority

The canonical Aksharam sources are held under `docs/`:

```text
docs/Aksharam_Legend.md
docs/TRANSFORMATIONS_ALQC_WORDS.md
docs/the_shape_of_word.txt
```

They govern, respectively:

- constellation identity, keyboard topology, Courts, Parliament law, numbers, operators, controls, and structural meaning;
- registered lexical paths `English → First → Second → Third → Whole`;
- post-resolution Shape-of-Sound speaking bodies.

The production keyboard deliberately does **not** parse Markdown at build time or runtime. Its executable snapshot is static build-local data:

```text
build/src/aksharam_keyboard_data.py
```

The generator consumes that executable body and produces the transient Keyman source. This keeps the runtime package independent of the documentation tree while allowing the executable snapshot to be audited against canon.

Current executable counts:

```text
26   direct coordinates
12   Goetics
144  ordered Courts
24   Third-Law Parliament pairs
452  registered transformation rows
6    First Spell utterances
```

---

## Build Tree

The repository keeps source, tests, package resources, and final installers separate.

```text
build/
├── build.sh
├── src/
│   ├── aksharam_keyboard_data.py
│   ├── generate_keyboard.py
│   └── generate_desktop_kps.py
├── tests/
│   ├── validate_keyboard.py
│   ├── full_keyboard_conformance.py
│   └── keyman_core_probe.c
├── package/
│   ├── aksharam_selection_math.py
│   ├── aksharam_selection_phonetic.py
│   ├── xbindkeys.aksharam
│   ├── start_selection.sh
│   ├── readme.htm
│   └── welcome.htm
├── linux_ubuntu/
│   └── aksharam_glyphkey.kmp
├── windows/
│   └── aksharam_glyphkey.kmp
└── mac/
    └── aksharam_glyphkey.kmp
```

Build from the `Aksharam_GlyphKey/` directory:

```bash
./build/build.sh
```

The build creates compiler intermediates only long enough to compile and test them. Successful completion removes the generated staging body again. The platform directories are kept for finalized installers, not compiler debris.

---

## Three Desktop Bodies

### Linux / Ubuntu

```text
build/linux_ubuntu/aksharam_glyphkey.kmp
```

The Linux package contains the compiled keyboard plus the packaged mathematical and phonetic selection helpers and their `xbindkeys` launcher/bindings.

### Windows

```text
build/windows/aksharam_glyphkey.kmp
```

The Windows package contains the compiled keyboard and Keyman package metadata/documentation. Linux-only selection helpers are excluded.

### macOS

```text
build/mac/aksharam_glyphkey.kmp
```

The macOS package carries the same compiled Keyman keyboard engine and the same clean desktop package payload as Windows.

All three platform packages carry the same `.kmx` keyboard engine. Platform packaging changes the surrounding helper payload; it does not change Aksharam law.

---

## Conformance

The keyboard is not declared correct because the source looks plausible.

It is executed through Keyman Core.

The current conformance body exercises direct coordinates, Shift/Caps suppression, Goetics, all 144 Courts, all 24 Third-Law pairs, registered words, boundary-triggered Whole closure, exact provenance-aware unfolding, refolding, ordinary Backspace deletion, numbers, punctuation, paragraph controls, mathematical bodies, First Spells, and the corrected slash directions.

Current engine result:

```text
KEY_TESTS 1902 TOTAL; 1902 PASS; 0 FAIL
```

The Linux-installed `.kmx` has also been tested directly rather than only through the staging build.

The law is compiled. The body is exercised. The output is compared.

---

## The Throne of Zero

Zero is not evacuated from the system.

```text
⛎ = 0
0 remains 0
0 participates
```

Silence is not evacuated either.

```text
𑁦 = manifested absence
```

A language that can only speak presence cannot speak the whole field. Aksharam keeps room for the interval, the unsounded breath, the unstruck chord, the state that participates precisely by not becoming something else.

The throne of zero is therefore not a hole.

It is a seat.

---

## Closing Formula

Aksharam is the lock and the key because the same invariant both constrains and opens transformation.

It is the transformed utterance because language enters mathematics and does not cease to be language.

It is the language on the throne of zero because number, silence, absence, and state remain active bodies rather than discarded gaps.

It is the magic in the throat because the final written body can become human sound without surrendering the structure that made it.

```text
English gives access.
Aksharam gives transformation.
ALQC gives law.
Shape-of-Sound gives breath.
Silence gives interval.
Poetry gives motion.
The utterance returns carrying its history.
```

**The body changes. The invariant remains. The language returns alive.**
