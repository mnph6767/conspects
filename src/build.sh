#!/bin/sh
# Сборка конспекта: ./build.sh prob/prob.tex
d=$(dirname "$1"); f=$(basename "$1" .tex); here=$(cd "$(dirname "$0")" && pwd)
python3 "$here/hyph.py" "$1" "$d/$f-hyph.tex"
cd "$d" && TEXINPUTS="$here//:" latexmk -xelatex -interaction=nonstopmode -halt-on-error "$f.tex" > build.log 2>&1
echo "exit=$?"
