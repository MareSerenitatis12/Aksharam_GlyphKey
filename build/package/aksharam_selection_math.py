#!/usr/bin/env python3
import json, subprocess, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MAP=json.loads((ROOT/'selection_math_map.json').read_text(encoding='utf-8'))
KEYS=sorted(MAP,key=len,reverse=True)

def transform(s):
    out=[]; i=0
    while i<len(s):
        for k in KEYS:
            if s.startswith(k,i):
                out.append(MAP[k]); i+=len(k); break
        else:
            out.append(s[i]); i+=1
    return ''.join(out)

def main():
    subprocess.run(['xclip','-i','-selection','clipboard'], input='', text=True, check=False)
    subprocess.run(['xdotool','key','--clearmodifiers','ctrl+c'], check=False)
    time.sleep(0.06)
    try:
        s=subprocess.check_output(['xclip','-o','-selection','clipboard'],text=True)
    except Exception:
        return 2
    if not s:
        return 0
    t=transform(s)
    if t==s:
        return 0
    p=subprocess.Popen(['xclip','-i','-selection','clipboard'],stdin=subprocess.PIPE,text=True)
    p.communicate(t)
    time.sleep(0.04)
    subprocess.run(['xdotool','key','--clearmodifiers','ctrl+v'],check=False)
    return 0
if __name__=='__main__': raise SystemExit(main())
