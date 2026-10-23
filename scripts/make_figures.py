"""Optional local publication figures. Requires matplotlib; no API/physics."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((R/p).read_text(encoding='utf8'))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
fig,axes=plt.subplots(1,3,figsize=(12,3.6),layout='constrained')
g1=read('data/perception/g1.json');g2=read('data/perception/g2_calibration.json');held=read('data/verification/held_detection.json')
axes[0].bar(['D','R','O','H'],[g1['totals'][m]['valid'] for m in ['D','R','O','H']],color=['#999999','#3587a4','#8f6cad','#59a96a'])
axes[0].set(ylim=(0,48),ylabel='Whole-sequence qualified / planned',title='G1: 48 layouts (7 initial rejects)')
for i,m in enumerate(['D','R','O','H']):axes[0].text(i,g1['totals'][m]['valid']+.5,str(g1['totals'][m]['valid']),ha='center')
ms=['D','R','O','H','SOR','RAD','CC','Q0'];vs=[g2['methods'][m]['valid'] for m in ms]
axes[1].bar(ms,vs,color=['#999999']*4+['#3587a4','#999999','#3587a4','#999999']);axes[1].axhline(7,color='black',ls='--',lw=1,label='Observed candidate union')
axes[1].set(ylim=(0,16),title='G2: calibration, 16 layouts');axes[1].tick_params(axis='x',labelrotation=45);axes[1].legend(frameon=False,fontsize=8)
ms=['B0','B1','B2','H'];xs=list(range(4))
axes[2].bar([x-.18 for x in xs],[held['methods'][m]['TP'] for m in ms],width=.36,label='TP / 25',color='#3587a4')
axes[2].bar([x+.18 for x in xs],[held['methods'][m]['FP'] for m in ms],width=.36,label='FP / 7',color='#cf7357')
axes[2].set(xticks=xs,xticklabels=ms,ylim=(0,28),title='Held verification: 32 layouts');axes[2].legend(frameon=False)
out=R/'paper/figures';out.mkdir(parents=True,exist_ok=True)
for ext in ['pdf','svg','png']:fig.savefig(out/f'diagnostic_results.{ext}',dpi=180)
plt.close(fig)
print(out)
