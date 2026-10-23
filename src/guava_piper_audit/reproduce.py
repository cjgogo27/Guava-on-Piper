"""Recompute RELEASED numerical evidence. Does not claim to rerun physics."""
from pathlib import Path
from collections import Counter
import json,argparse,hashlib
from .statistics import exact_mcnemar,holm,paired_counts,wilson

def reproduce(root):
    root=Path(root);read=lambda p:json.loads((root/p).read_text(encoding='utf8'));out={}
    ev=read('data/evaluation/task_counts.json');rows=ev['tasks']
    assert sum(x['planned'] for x in rows)==450
    assert sum(x['baseline_success'] for x in rows)==ev['baseline_success']==49
    assert sum(x['sft_success'] for x in rows)==ev['sft_success']==66
    assert ev['official_completed']+ev['process_aborts']==450
    assert sum(ev['paired_complete_cases'].values())==449
    out['full_task_descriptive']={'planned_per_model':450,'baseline_success':49,'sft_success':66,'delta_pp':100*(66-49)/450,'sft_aborts':1,'not_causal_interface_ablation':True}
    g1=read('data/perception/g1.json');grows=g1['rows'];assert len(grows)==48
    counts={m:sum(r['valid'][m] for r in grows) for m in ['D','R','O','H']}
    assert counts=={m:x['valid'] for m,x in g1['totals'].items()}
    contrasts={m:paired_counts([r['valid'][m] for r in grows],[r['valid']['D'] for r in grows]) for m in ['R','O']}
    ps=[exact_mcnemar(**x) for x in contrasts.values()];adj=holm(ps)
    out['G1']={'planned_layouts':48,'counts':counts,'contrasts':{m:{**contrasts[m],'exact_p':ps[i],'holm_p':adj[i]} for i,m in enumerate(contrasts)}}
    for i,m in enumerate(contrasts):assert abs(adj[i]-g1['contrasts'][m+'-D']['holm_p'])<1e-12
    g2=read('data/perception/g2_calibration.json');assert len(g2['rows'])==16
    counts={m:sum(r['arms'].get(m,{}).get('valid',False) for r in g2['rows']) for m in g2['methods']}
    assert counts=={m:x['valid'] for m,x in g2['methods'].items()}
    union=sum(any(a['valid'] for a in r['arms'].values()) for r in g2['rows'])
    assert union==counts['SOR']==counts['CC']==7
    g2tests={}
    for m in ['SOR','CC']:
        c=paired_counts([r['arms'].get(m,{}).get('valid',False) for r in g2['rows']], [r['arms'].get('D',{}).get('valid',False) for r in g2['rows']])
        g2tests[m]={'discordants':c,'exact_p':exact_mcnemar(**c)}
        assert g2tests[m]['exact_p']==g2['methods'][m]['exact_McNemar_p_exploratory']
    out['G2_calibration']={'planned_layouts':16,'initial_rejects':len(g2['initial_rejects']),'physical_arms':g2['actual_physical_arms'],'counts':counts,'observed_candidate_union':union,'exploratory_paired_tests':g2tests,'not_generalization_test':True}
    held=read('data/verification/held_detection.json');hrows=held['all_rows'];assert len(hrows)==32
    conf={}
    for m in ['B0','B1','B2','H']:
        c=Counter()
        for r in hrows:
            pos=r['predictions'][m]=='positive';truth=r['label']=='held'
            c['TP' if pos and truth else 'FP' if pos else 'FN_negative' if truth else 'TN']+=1
        assert all(c[k]==held['methods'][m][k] for k in ['TP','FP','FN_negative','TN'])
        conf[m]={**dict(c),'sensitivity_wilson95':wilson(c['TP'],25),'false_positive_rate_wilson95':wilson(c['FP'],7)}
    assert all(r['predictions']['B2']==r['predictions']['H'] for r in hrows)
    four=[]
    for kind,label in [('FP','nonheld'),('TP','held')]:
        rows=[r for r in hrows if r['label']==label]
        for baseline in ['B1','B2']:
            c=paired_counts([r['predictions']['H']=='positive' for r in rows],[r['predictions'][baseline]=='positive' for r in rows])
            four.append({'type':kind,'baseline':baseline,**c,'p_exact':exact_mcnemar(**c)})
    for x,p,expected in zip(four,holm([x['p_exact'] for x in four]),held['paired_tests_four_Holm']):
        x['p_holm']=p
        assert abs(p-expected['p_holm'])<1e-12 and x['rescued']==expected['H_positive_only'] and x['lost']==expected['baseline_positive_only']
    out['held_detection']={'independent_layouts':32,'repeats_not_independent':4,'methods':conf,'four_planned_paired_tests':four,'fusion_additional_corrections_vs_B1':0,'lost_true_positives_vs_B1':11,'not_full_task_SR':True}
    contract=read('data/collection/interface_audit.json')['training_interface']
    assert contract['rows']==1041 and contract['motion_mode_episodes']==420 and contract['motion_mode_calls']==2476
    assert sum(contract['motion_modes'].values())==2476
    out['schema_audit']={'rows':1041,'extended_argument_records':420,'extended_argument_calls':2476,'affected_record_percent':420/1041*100}
    out['scope']='Reproduced curated numerical tables, not raw-state audit or fresh dynamics.'
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--output',type=Path)
    a=ap.parse_args();out=reproduce(a.root);s=json.dumps(out,indent=2)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s+'\n',encoding='utf8')
    print(s)

if __name__=='__main__':main()
