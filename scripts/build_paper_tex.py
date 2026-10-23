"""Generate the plain technical-report TeX source from the English working draft.
Not an official CVPR template; no conference/acceptance status is implied.
"""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]

def esc(s):
    math=[]
    def keep(m):math.append(m.group());return f'ZZMATH{len(math)-1}ZZ'
    s=re.sub(r'\\\(.*?\\\)',keep,s)
    links=[]
    def link(m):links.append((m.group(1),m.group(2)));return f'ZZLINK{len(links)-1}ZZ'
    s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',link,s)
    s=s.replace('—','--').replace('–','--').replace('’',"'").replace('“','``').replace('”',"''")
    symbols={'→':r'\(\rightarrow\)','×':r'\(\times\)','≥':r'\(\geq\)','≤':r'\(\leq\)','α':r'\(\alpha\)'}
    chars={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    s=''.join(symbols.get(c,chars.get(c,c)) for c in s)
    s=re.sub(r'`([^`]+)`',lambda m:r'\texttt{'+m.group(1)+'}',s)
    s=re.sub(r'\*\*([^*]+)\*\*',lambda m:r'\textbf{'+m.group(1)+'}',s)
    for i,m in enumerate(math):s=s.replace(f'ZZMATH{i}ZZ',m)
    for i,(label,url) in enumerate(links):s=s.replace(f'ZZLINK{i}ZZ',r'\href{'+url.replace('%',r'\%')+'}{'+esc(label)+'}')
    s=re.sub(r'(?<![\w{])(https://\S+)',lambda m:r'\url{'+m.group(1)+'}',s)
    return s

lines=(R/'paper/DRAFT.md').read_text(encoding='utf8').splitlines();title=lines[0][2:];body=[];i=1
while i<len(lines):
    line=lines[i]
    if line.startswith('|'):
        table=[]
        while i<len(lines) and lines[i].startswith('|'):
            cells=[x.strip() for x in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',c) for c in cells):table.append(cells)
            i+=1
        n=len(table[0]);width=(.94-.035*n)/n
        widths=[.37,.14,.145,.145] if n==4 and table[0][0]=='Task' else [width]*n
        columns=''.join('p{'+f'{w:.3f}'+r'\textwidth}' for w in widths)
        body.append(r'\par\noindent\begin{minipage}{\linewidth}\centering\small\setlength{\tabcolsep}{4pt}\begin{tabular}{'+columns+r'}\hline')
        for j,row in enumerate(table):body.append(' & '.join(esc(x) for x in row)+r' \\'+(r' \hline' if j==0 else ''))
        body.append(r'\hline\end{tabular}\end{minipage}\par\medskip');continue
    if line.startswith('### '):body.append(r'\subsection*{'+esc(line[4:])+'}')
    elif line.startswith('## '):body.append(r'\section*{'+esc(line[3:])+'}')
    elif re.match(r'^\d+\. ',line):body.append(r'\par\noindent '+esc(line)+r'\par')
    else:body.append(esc(line))
    if line.startswith('## 5.'):
        body[-1:-1]=[r'\begin{figure}[ht]\centering\includegraphics[width=\linewidth]{../figures/diagnostic_results.pdf}\caption{Distinct diagnostic cohorts, not pooled samples. G1 uses 48 planned layouts; G2 is 16 calibration layouts including initial rejects; held verification uses 32 layouts. Counts do not imply statistically significant improvement or full-task success.}\end{figure}']
    i+=1
tex=r'''\documentclass[10pt]{article}
\usepackage[margin=0.85in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{amsmath,graphicx,array,longtable}
\usepackage[hidelinks]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\setlength{\emergencystretch}{3em}
\title{'''+esc(title)+r'''}
\author{Guava-on-Piper working technical report\\Human author metadata to be finalized}
\date{23 October 2026}
\begin{document}
\maketitle
'''+ '\n'.join(body)+r'\end{document}'+'\n'
(R/'paper/latex/main.tex').write_text(tex,encoding='utf8')
print('Wrote paper/latex/main.tex')
