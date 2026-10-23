"""Explicit CAD fingertip target path. Same declared tilts and unchanged arm arrival gate."""
import numpy as np
from scipy.spatial.transform import Rotation
from guava.robot.piper_motion import RADIAL_TILTS_DEG
OFFSET=.1358-.005011089-.09755
def move_tip(ctx,goal,reference):
 arm=ctx.arm;env=ctx.env;goal=np.asarray(goal,float)
 if goal.shape!=(3,) or not np.isfinite(goal).all():raise ValueError('Finite tip target required')
 offset=np.asarray(arm.cfg.grasp_center_offset)+[0,0,OFFSET]
 p,q=env.eef_pose_base();start=p+Rotation.from_quat(q[[1,2,3,0]]).apply(offset)
 r0=Rotation.from_quat(np.asarray(reference)[[1,2,3,0]]);count=max(1,int(np.ceil(np.linalg.norm(goal-start)/.025)));arm.last_tip_center_path=[]
 for step in range(1,count+1):
  point=start+(goal-start)*(step/count);direction=point.copy();direction[2]=0
  if np.linalg.norm(direction)<1e-8:raise RuntimeError('Undefined radial direction')
  axis=np.cross([0,0,1],direction/np.linalg.norm(direction));selected=None
  for angle in RADIAL_TILTS_DEG:
   r=Rotation.from_rotvec(axis*np.deg2rad(angle))*r0;q=r.as_quat()[[3,0,1,2]];tcp=point-r.apply(offset)
   sol,info=arm.ik.solve_accepted(tcp,q,env.joint_positions(),target_link_pos=tcp+r.apply(arm.cfg.tcp_offset))
   if sol is not None:selected=(angle,tcp,q);break
  if selected is None:raise RuntimeError('No declared fingertip pose reachable')
  angle,tcp,q=selected;status=arm.move(tcp,q);p,aq=env.eef_pose_base();actual=p+Rotation.from_quat(aq[[1,2,3,0]]).apply(offset)
  arm.last_tip_center_path.append(dict(step=step,tip_goal=point.tolist(),actual_tip=actual.tolist(),radial_tilt_deg=angle,status=status))
  if status!='success':raise RuntimeError('Fingertip motion failed: '+status)
 return float(np.linalg.norm(actual-goal))
