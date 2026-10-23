'use strict';
const repo='https://github.com/cjgogo27/Guava-on-Piper';
const names={apple_juice_order:'苹果与果汁排序',push_basket:'推篮',red_objects_in_basket:'红色物体入篮',can_in_bin:'罐子入箱',close_drawer:'关闭抽屉',remove_cube_from_tray:'托盘取方块',shell_game:'杯子游戏',pick_up_carrot:'拿起胡萝卜',tomato_near_potato:'番茄放到土豆旁',lemon_in_bin:'柠檬入箱',push_pot:'推锅',cube_stack_reverse:'反向堆方块',apple_juice_reverse_order:'苹果与果汁反向排序',bin_and_tray_simple:'箱子与托盘',set_table:'摆桌'};
const methodNames={D:'原估计',R:'分位处理',O:'重新观察',H:'简单规则',SOR:'统计过滤',RAD:'半径过滤',CC:'连通分量',Q0:'质量规则'};
const order=['apple_juice_order','push_basket','red_objects_in_basket','can_in_bin','close_drawer','remove_cube_from_tray','shell_game','pick_up_carrot','tomato_near_potato','lemon_in_bin','push_pot','cube_stack_reverse','apple_juice_reverse_order','bin_and_tray_simple','set_table'];
let evidence;
function pressed(selector,chosen){document.querySelectorAll(selector).forEach(b=>{const selected=b===chosen;b.classList.toggle('active',selected);b.setAttribute('aria-pressed',String(selected));});}
function text(tag,value,className){const el=document.createElement(tag);el.textContent=value;if(className)el.className=className;return el;}
function taskChart(group='all'){
  const host=document.querySelector('#task-chart');host.replaceChildren();
  const rows=evidence.task_counts.filter(r=>group==='all'||r.group===group).sort((a,b)=>order.indexOf(a.task)-order.indexOf(b.task));
  for(const r of rows){
    const row=document.createElement('div');row.className='task-row'+(r.sft_success<r.baseline_success?' decline':'');row.setAttribute('role','group');row.setAttribute('aria-label',`${names[r.task]}：基线 ${r.baseline_success}/${r.planned}，SFT ${r.sft_success}/${r.planned}`);
    const label=text('div',names[r.task]||r.task,'task-name');label.append(text('small',r.group==='trained'?'TRAINED':'UNSEEN'));row.append(label);
    const bars=document.createElement('div');bars.className='task-bars';bars.setAttribute('aria-hidden','true');
    for(const [count,cls] of [[r.baseline_success,'base'],[r.sft_success,'tuned']]){const track=document.createElement('div');track.className='task-track';const fill=document.createElement('div');fill.className='task-fill '+cls;fill.style.width=`${100*count/r.planned}%`;track.append(fill);bars.append(track);}
    row.append(bars);const values=text('div','','task-values');values.append(text('span',String(r.baseline_success)),text('span','→'),text('b',String(r.sft_success)));row.append(values);host.append(row);
  }
}
function baselineChart(stage='g1'){
  const data=evidence[stage];const host=document.querySelector('#baseline-chart');host.replaceChildren();
  for(const [m,count] of Object.entries(data.counts)){
    const col=document.createElement('div');col.className='baseline-col';col.setAttribute('role','img');col.setAttribute('aria-label',`${methodNames[m]} ${count}/${data.denominator} 物理合格`);
    const bar=document.createElement('div');bar.className='baseline-bar'+((stage==='g2'&&['SOR','CC'].includes(m))||(stage==='g1'&&m==='H')?' highlight':'');bar.style.height=`${count/data.denominator*170}px`;bar.append(text('span',String(count),'baseline-number'));col.append(bar,text('span',`${m} ${methodNames[m]}`,'baseline-method'));host.append(col);
  }
  document.querySelector('#stage-denominator').textContent=stage==='g1'?'48 个计划布局，含 7 个初态拒绝':'16 个校准布局，含 5 个初态拒绝；非密封测试';
  document.querySelector('#stage-headline').textContent=stage==='g1'?'32 → 38，但还不能说“显著改善”。':'标准 SOR / CC 已达到本次 8 方法并集：7 / 16。';
  document.querySelector('#stage-note').textContent=stage==='g1'?'分位处理对原估计救回 7 例、损失 1 例；Holm 校正 p = 0.140625。简单规则达到本次候选并集 39/48，不构成泛化保证。':'两种标准过滤各自救回 2 例且没有损失原成功；探索性配对 p = 0.5。它们是在校准集上选出的强基线，尚无独立新对象泛化证据；不证明等效或观察普遍无用。';
  document.querySelector('#stage-link').href=repo+'/blob/main/data/perception/'+(stage==='g1'?'g1.json':'g2_calibration.json');
}
const cases={
  visualFN:{seed:3402301020,title:'物体升起了，可见中心没有升够。',real:'40.270',estimated:'20.203',text:'夹爪遮挡后，可见点集发生变化。以 25 mm 可见中心位移作为必要条件，在这个案例中漏掉了一次有效抬升。',caution:'这是个例线索，不是对所有漏判成因的因果证明。',before:'操作前，果汁瓶在桌面上且较完整可见。',after:'抬升后，夹爪遮挡果汁瓶的一部分。'},
  sharedFP:{seed:3402301017,title:'同一个“果汁瓶”描述，前后选中了不同物体。',real:'约 0',estimated:'33.898',text:'离线查看保存掩码：C0 选中了苹果，C1 选中了果汁瓶。实际果汁未被抬起，但两个可见中心之差产生了正向抬升估计。',caution:'目标身份切换只在这个例子中核实，不能直接推广为全部误报的成因。',before:'操作前画面；保存掩码将果汁描述关联到苹果。',after:'操作后画面；保存掩码将同一描述关联到果汁瓶。'}
};
let currentCase='visualFN';
function chooseCase(id){currentCase=id;const c=cases[id];for(const [suffix,key] of [['C0','before'],['C1','after']]){const img=document.querySelector('#case-'+key);img.src=`assets/${id}_${suffix}.png`;img.alt=c[key];}document.querySelector('#case-id').textContent='布局 seed '+c.seed;document.querySelector('#case-title').textContent=c.title;for(const [element,value] of [['#case-real',c.real],['#case-estimate',c.estimated]]){const el=document.querySelector(element);el.replaceChildren(document.createTextNode(value+' '),text('small','mm'));}document.querySelector('#case-text').textContent=c.text;document.querySelector('#case-caution').textContent=c.caution;}
document.querySelectorAll('[data-case]').forEach(b=>b.addEventListener('click',()=>{pressed('[data-case]',b);chooseCase(b.dataset.case);}));
const dialog=document.querySelector('#image-dialog');
document.querySelectorAll('[data-image]').forEach(b=>b.addEventListener('click',()=>{const img=document.querySelector('#case-'+b.dataset.image);document.querySelector('#dialog-image').src=img.src;document.querySelector('#dialog-image').alt=img.alt;document.querySelector('#dialog-caption').textContent=`seed ${cases[currentCase].seed} · `+img.alt;dialog.showModal();}));
document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
fetch('evidence.json').then(r=>{if(!r.ok)throw new Error('Evidence unavailable');return r.json();}).then(data=>{
  evidence=data;taskChart();baselineChart();
  document.querySelectorAll('[data-task-filter]').forEach(b=>b.addEventListener('click',()=>{pressed('[data-task-filter]',b);taskChart(b.dataset.taskFilter);}));
  document.querySelectorAll('[data-stage]').forEach(b=>b.addEventListener('click',()=>{pressed('[data-stage]',b);baselineChart(b.dataset.stage);}));
}).catch(()=>{document.querySelector('#task-chart').textContent='数值表暂时无法加载，请使用仓库 data/evaluation/task_counts.csv。';document.querySelector('#baseline-chart').textContent='请查看仓库 data/perception/ 下的原表。';});
const hero=document.querySelector('#hero-video');
if(!matchMedia('(prefers-reduced-motion: reduce)').matches){hero.play().catch(()=>{});new IntersectionObserver(entries=>{for(const entry of entries)if(!entry.isIntersecting)hero.pause();},{threshold:.05}).observe(hero);}
