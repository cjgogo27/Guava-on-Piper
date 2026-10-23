"""Candidate grasp yaw selected from visible RGB-D obstacles and robot-owned CAD only."""
import json,numpy as np
from scipy.spatial.transform import Rotation
from scipy.spatial import ConvexHull
from scipy.ndimage import binary_dilation
from guava.robot.piper_motion import RADIAL_TILTS_DEG
def select(ctx,target,contact,reference):
 from guava.tools import piper_tools as pt
 from guava.tools.tools import _unproject_pointclouds
 from robot_self_filter_v2 import capture_robot_boxes,filter_points
 from contact_path_v33 import OFFSET
 rgb,depth,K,T=pt._save_view(ctx);mask=ctx.perception.get_mask(target,rgb);exclude=binary_dilation(mask,iterations=2)
 _,pc=_unproject_pointclouds(depth,K,~exclude);pc=pc[::3];points=(T@np.c_[pc,np.ones(len(pc))].T).T[:,:3];points=points[np.isfinite(points).all(1)];points=points[(points[:,2]>-ctx.model_z_offset+.003)&(np.linalg.norm(points[:,:2]-contact[:2],axis=1)<.15)];points,_=filter_points(points,capture_robot_boxes(ctx))
 m=ctx.env.rob.sim.model._model;d=ctx.env.rob.sim.data._data;p,q=ctx.env.eef_pose_base();base=ctx.env.base_wxyz_xyz();rb=Rotation.from_quat(base[:4][[1,2,3,0]]).as_matrix();rnow=rb@Rotation.from_quat(q[[1,2,3,0]]).as_matrix();pw=rb@p+base[4:];hulls=[]
 for gid in range(m.ngeom):
  name=m.geom(gid).name or ''
  if not name.startswith(('gripper0_right_link7','gripper0_right_link8')) or not m.geom_contype[gid]:continue
  if m.geom_type[gid]==7:
   mid=int(m.geom_dataid[gid]);adr=int(m.mesh_vertadr[mid]);verts=m.mesh_vert[adr:adr+int(m.mesh_vertnum[mid])]
  elif m.geom_type[gid]==6:
   verts=np.array([[x,y,z] for x in [-1,1] for y in [-1,1] for z in [-1,1]])*m.geom_size[gid]
  else:continue
  local=(verts@d.geom_xmat[gid].reshape(3,3).T+d.geom_xpos[gid]-pw)@rnow;hulls.append(ConvexHull(local).equations)
 offset=np.asarray(ctx.arm.cfg.grasp_center_offset)+[0,0,OFFSET];r0=Rotation.from_quat(reference[[1,2,3,0]]);trials=[]
 for yaw in [0,45,-45,90]:
  rr=Rotation.from_rotvec([0,0,np.deg2rad(yaw)])*r0;score=0;feasible=True
  for height in [.075,.05,.025,0]:
   tip=contact+[0,0,height];axis=np.cross([0,0,1],np.r_[tip[:2]/np.linalg.norm(tip[:2]),0]);selected=None
   for tilt in RADIAL_TILTS_DEG:
    r=Rotation.from_rotvec(axis*np.deg2rad(tilt))*rr;quat=r.as_quat()[[3,0,1,2]];tcp=tip-r.apply(offset)
    sol,_=ctx.arm.ik.solve_accepted(tcp,quat,ctx.env.joint_positions(),target_link_pos=tcp+r.apply(ctx.arm.cfg.tcp_offset))
    if sol is not None:selected=(r,tcp);break
   if selected is None:feasible=False;break
   r,tcp=selected;cloud=(points-tcp)@r.as_matrix();inside=np.zeros(len(cloud),bool)
   for eq in hulls:inside|=np.all(cloud@eq[:,:3].T+eq[:,3]<=.003,axis=1)
   score+=int(inside.sum())
  trials.append(dict(yaw_deg=yaw,visible_obstacle_points=int(len(points)),collision_risk_points=score,ik_feasible=feasible))
 eligible=[t for t in trials if t['ik_feasible'] and t['collision_risk_points']==0]
 ctx._last_visible_grasp_clearance=dict(candidates=trials,margin_m=.003,scope='visible surfaces only; not hidden collision-free guarantee')
 if not eligible:raise RuntimeError('No clear observed grasp approach; acquire another view or clear neighbor before grasp')
 chosen=min(eligible,key=lambda t:abs(t['yaw_deg']));ctx._last_visible_grasp_clearance['selected_yaw_deg']=chosen['yaw_deg']
 return (Rotation.from_rotvec([0,0,np.deg2rad(chosen['yaw_deg'])])*r0).as_quat()[[3,0,1,2]]
