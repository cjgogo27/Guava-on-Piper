"""Branch-only provenance and applicable perturbation checks; never teacher observations."""
import re,xml.etree.ElementTree as ET

def resolve_target(target,aliases):
 target=str(target).strip().lower(); normalized={str(k).lower():v for k,v in aliases.items()}
 if target in normalized:return normalized[target]
 if target in normalized.values():return target
 tokens=set(re.findall(r'[a-z0-9]+',target));matches={v for k,v in normalized.items() if set(re.findall(r'[a-z0-9]+',k))<=tokens}
 if len(matches)==1:return next(iter(matches))
 return None

def free_joint_for(snapshot,target):
 if not target:return None
 xml=(snapshot or {}).get('xml')
 if not xml:return None
 root=ET.fromstring(xml)
 for name in dict.fromkeys((target,target.replace(' ','_'))):
  for j in root.iter('joint'):
   if j.get('name') in (name+'_joint0',name+'_jnt') and j.get('type','hinge')=='free':return j.get('name')
  for body in root.iter('body'):
   if body.get('name') not in (name,name+'_main',name+'_body'):continue
   for j in list(body):
    if j.tag=='freejoint' or (j.tag=='joint' and j.get('type')=='free'):return j.get('name')
 return None

def install():
 from guava.collection import branch
 from guava.collection.perturbation import SetObjectPose
 original=branch.make_branch_specs
 def make(vocab,aliases=None):
  aliases=aliases or {};specs=original(vocab,aliases)
  for name in ('object_moved_align','drop_during_transport'):
   s=specs[name];condition=s.trigger_condition;factory=s.make_perturbation
   def target(ck,n=name):
    value=ck.tool_args.get('target_name','') if n=='object_moved_align' else ck.grasped_object
    return resolve_target(value,aliases)
   def applicable(ck,c=condition,t=target):return c(ck) and free_joint_for(ck.snapshot,t(ck)) is not None
   def perturb(ck,f=factory,t=target):
    obj=t(ck)
    if not free_joint_for(ck.snapshot,obj):raise ValueError('Inapplicable free-object perturbation: unresolved or articulated target')
    value=f(ck)
    if not isinstance(value,SetObjectPose):raise TypeError('Unexpected object perturbation')
    value.object_name=obj;return value
   s.trigger_condition=applicable;s.make_perturbation=perturb
  return specs
 branch.make_branch_specs=make
