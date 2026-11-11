#!/usr/bin/env python3
"""Составляет \\hyphenation{...} для всех русских слов .tex-файла (слоговые правила)."""
import re, sys
V = set("аеёиоуыэюя"); SPEC = set("йьъ")
def points(w):
    n = len(w); cuts = set()
    for i in range(1, n):
        a, b = w[i-1], w[i]
        if b in SPEC: continue                    # не отрываем й, ь, ъ
        left, right = w[:i], w[i:]
        if not any(c in V for c in left) or not any(c in V for c in right): continue
        if len(left) < 2 or len(right) < 2: continue
        if a in V and b not in V and i+1 < n and w[i+1] in V: cuts.add(i)        # ко-ро-ва
        elif a in V and b in V: cuts.add(i)                                       # по-эт
        elif a not in V and b not in V and i >= 2 and w[i-2] in V: cuts.add(i)   # кон-тракт, май-ка
        elif a in "ьъ" and b not in V: cuts.add(i)                                # паль-то
        elif a == "ъ": cuts.add(i)
    return sorted(cuts)
src = open(sys.argv[1], encoding="utf-8").read()
words = sorted({w.lower() for w in re.findall(r"[А-Яа-яЁё]+", src) if len(w) >= 5})
out = []
for w in words:
    p = points(w)
    if not p: continue
    s = ""; prev = 0
    for c in p: s += w[prev:c] + "-"; prev = c
    out.append(s + w[prev:])
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write("\\hyphenation{\n" + "\n".join(out) + "\n}\n")
print(len(out), "слов")
