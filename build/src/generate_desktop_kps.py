#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 3:
    raise SystemExit('usage: generate_desktop_kps.py INPUT_KPS OUTPUT_KPS')

src=Path(sys.argv[1])
out=Path(sys.argv[2])
root=ET.fromstring(src.read_text(encoding='utf-8'))
files=root.find('Files')
linux_only={
    'aksharam_selection_math.py',
    'aksharam_selection_phonetic.py',
    'selection_math_map.json',
    'xbindkeys.aksharam',
    'start_selection.sh',
}
if files is None:
    raise SystemExit('KPS has no Files section')
for node in list(files):
    name=node.findtext('Name','')
    if name in linux_only:
        files.remove(node)
out.parent.mkdir(parents=True,exist_ok=True)
ET.indent(root, space='  ')
out.write_text('<?xml version="1.0" encoding="utf-8"?>\n'+ET.tostring(root, encoding='unicode'), encoding='utf-8')
