/* Deterministic DOM-logic unit checks. Not a browser-rendering/screenshot test. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
class Element{
  constructor(){this.children=[];this.dataset={};this.events={};this.attributes={};this.textContent='';this.style={};this.classList={toggle(){}};}
  append(...items){this.children.push(...items);}
  replaceChildren(...items){this.children=items;}
  setAttribute(k,v){this.attributes[k]=v;}
  addEventListener(k,f){this.events[k]=f;}
  click(){this.events.click?.({target:this});}
  play(){return Promise.resolve();}
  pause(){}
  showModal(){this.open=true;}
  close(){this.open=false;}
}
const elements=new Map();const get=k=>{if(!elements.has(k))elements.set(k,new Element());return elements.get(k);};
const buttonSets={};
for(const [attr,values] of [['task-filter',['all','trained','unseen']],['stage',['g1','g2']],['case',['visualFN','sharedFP']],['image',['before','after']]]){
  const prop=attr.replace(/-([a-z])/g,(_,s)=>s.toUpperCase());buttonSets[`[data-${attr}]`]=values.map(v=>{const e=new Element();e.dataset[prop]=v;return e;});
}
const document={querySelector:get,querySelectorAll:s=>buttonSets[s]||[],createElement:()=>new Element(),createTextNode:s=>({textContent:s})};
const context={document,console,fetch:async()=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.join(root,'site/evidence.json'),'utf8'))}),matchMedia:()=>({matches:true})};
vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(root,'site/app.js'),'utf8'),context,{timeout:3000});
setImmediate(()=>{
  assert.equal(get('#task-chart').children.length,15);
  buttonSets['[data-task-filter]'][1].click();assert.equal(get('#task-chart').children.length,7);
  buttonSets['[data-task-filter]'][2].click();assert.equal(get('#task-chart').children.length,8);
  buttonSets['[data-task-filter]'][0].click();assert.equal(get('#task-chart').children.length,15);
  assert.equal(get('#baseline-chart').children.length,4);
  buttonSets['[data-stage]'][1].click();assert.equal(get('#baseline-chart').children.length,8);assert.match(get('#stage-headline').textContent,/7 \/ 16/);assert.match(get('#stage-note').textContent,/泛化/);
  buttonSets['[data-stage]'][0].click();assert.equal(get('#baseline-chart').children.length,4);
  buttonSets['[data-case]'][1].click();assert.match(get('#case-id').textContent,/3402301017/);assert.equal(get('#case-before').src,'assets/sharedFP_C0.png');
  buttonSets['[data-image]'][0].click();assert.equal(get('#image-dialog').open,true);
  get('.dialog-close').click();assert.equal(get('#image-dialog').open,false);
  buttonSets['[data-case]'][0].click();assert.equal(get('#case-before').src,'assets/visualFN_C0.png');
  console.log(JSON.stringify({passed:true,scope:'DOM-logic simulation only; not actual browser rendering',checks:['15/7/8 task filters','G1/G2 chart source and denominator','case switch','image-dialog open/close']}));
});
