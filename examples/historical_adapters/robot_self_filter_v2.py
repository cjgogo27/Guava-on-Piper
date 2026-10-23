"""RGB-D self masking from robot-only CAD/FK. No object geometry/pose lookup."""
import numpy as np
import hashlib
def view_key(rgb):return hashlib.sha256(rgb.tobytes()).hexdigest()
from scipy.spatial.transform import Rotation

def capture_robot_boxes(ctx):
 m=ctx.env.rob.sim.model._model;d=ctx.env.rob.sim.data._data
 base=ctx.env.base_wxyz_xyz();rb=Rotation.from_quat(base[:4][[1,2,3,0]]).as_matrix();boxes=[]
 for gid in range(m.ngeom):
  name=m.geom(gid).name or '';body=m.body(int(m.geom_bodyid[gid])).name or ''
  if not (name.startswith(('robot0_','gripper0_')) or body.startswith(('robot0_','gripper0_'))):continue
  kind=int(m.geom_type[gid])
  if kind==7:
   mid=int(m.geom_dataid[gid]);a=int(m.mesh_vertadr[mid]);n=int(m.mesh_vertnum[mid]);v=m.mesh_vert[a:a+n];lo=v.min(0);hi=v.max(0)
  elif kind==6:lo=-m.geom_size[gid];hi=m.geom_size[gid]
  else:continue
  boxes.append((d.geom_xpos[gid].copy(),d.geom_xmat[gid].reshape(3,3).copy(),lo.copy(),hi.copy()))
 return base[4:].copy(),rb,boxes

def filter_points(points,geometry,margin=.003):
 pbase,rb,boxes=geometry;world=points@rb.T+pbase;keep=np.ones(len(points),bool)
 for pos,rot,lo,hi in boxes:
  local=(world-pos)@rot;keep &= ~np.all((local>=lo-margin)&(local<=hi+margin),axis=1)
 return points[keep],keep

def install():
 from guava.tools import piper_tools as pt
 from guava.tools.tools import _unproject_pointclouds,_remove_statistical_outliers
 save=pt._save_view;estimate=pt._estimate
 def view(ctx):
  v=save(ctx);cache=getattr(ctx,'_robot_geometry_views',{});cache[view_key(v[0])]=capture_robot_boxes(ctx);ctx._robot_geometry_views=cache
  if len(cache)>20:
   for k in list(cache)[:-10]:cache.pop(k,None)
  return v
 def clean_estimate(ctx,target):
  # Use only in isolated candidate tasks until regressions pass.
  task=ctx.env.cfg.task
  if task not in ('apple_juice_order','red_objects_in_basket'):return estimate(ctx,target)
  cache=getattr(ctx,'_piper_estimates',{})
  if target in cache:return cache[target]
  views=getattr(ctx,'_piper_scan_views',None) or [pt._save_view(ctx)];clouds=[];removed=0;total=0
  for rgb,depth,K,T in views:
   mask=ctx.perception.get_mask(target,rgb);_,pc=_unproject_pointclouds(depth,K,mask);pc=_remove_statistical_outliers(pc,k=20,std_ratio=2)
   points=(T@np.c_[pc,np.ones(len(pc))].T).T[:,:3];points=points[np.isfinite(points).all(1)&(points[:,2]>-float(ctx.model_z_offset)+.002)]
   total+=len(points);geometry=getattr(ctx,'_robot_geometry_views',{}).get(view_key(rgb))
   if geometry is None:raise RuntimeError('Observation missing time-matched robot FK; acquire a fresh view.')
   points,keep=filter_points(points,geometry);removed+=int((~keep).sum())
   if len(points)>=10:clouds.append(points)
  ctx._last_self_filter={'target':target,'total':total,'robot_removed':removed,'margin_m':.003,'source':'robot CAD and time-matched proprioceptive FK only'}
  if not clouds or (removed>total*.8 and total-removed<50):raise RuntimeError('Target occluded or segmentation matches the robot; no reliable object depth. Clear the view and observe again.')
  points=np.concatenate(clouds);lo,hi=np.quantile(points,[.005,.995],axis=0);result={'center':(lo+hi)/2,'low':lo,'high':hi,'points':points,'views':len(clouds)};cache[target]=result;ctx._piper_estimates=cache;return result
 pt._save_view=view;pt._estimate=clean_estimate
