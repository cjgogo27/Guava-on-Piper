"""Pose-consistent TCP/physical-contact-point conversion (no IK or GT input)."""
from math import sqrt, isfinite

def rotate_wxyz(quaternion,vector):
    if len(quaternion)!=4 or len(vector)!=3 or not all(isfinite(x) for x in [*quaternion,*vector]):
        raise ValueError("Finite wxyz quaternion and 3-vector required")
    norm=sqrt(sum(x*x for x in quaternion))
    if norm<1e-12:raise ValueError("Zero quaternion")
    w,x,y,z=[v/norm for v in quaternion];vx,vy,vz=vector
    tx,ty,tz=2*(y*vz-z*vy),2*(z*vx-x*vz),2*(x*vy-y*vx)
    return [vx+w*tx+y*tz-z*ty,vy+w*ty+z*tx-x*tz,vz+w*tz+x*ty-y*tx]

def tcp_for_contact_goal(contact_goal,selected_quaternion,local_contact_offset):
    """Use the SELECTED segment orientation, not a previous segment's orientation."""
    if len(contact_goal)!=3 or not all(isfinite(x) for x in contact_goal):raise ValueError("Finite goal required")
    r=rotate_wxyz(selected_quaternion,local_contact_offset)
    return [a-b for a,b in zip(contact_goal,r)]

def contact_point(tcp,quaternion,offset):
    return [a+b for a,b in zip(tcp,rotate_wxyz(quaternion,offset))]
