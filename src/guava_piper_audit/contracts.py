"""Effect and recovery provenance checks; diagnostic, not hardware safety gates."""
import hashlib
from math import isfinite

def sha256(data):return hashlib.sha256(data).hexdigest()

def validate_branch(*,saved_parent_image,current_parent_image,teacher_fault_image,
                    actual_fault_image,parent_model_sha256,restored_model_sha256,
                    reward_before,reward_after,perturbation_displacement_m,
                    minimum_displacement_m,consumed_pair_ids,pair_id):
    errors=[]
    if saved_parent_image!=current_parent_image:errors.append('parent_image_mismatch')
    if teacher_fault_image!=actual_fault_image:errors.append('stale_teacher_image')
    if parent_model_sha256!=restored_model_sha256:errors.append('parent_model_changed')
    if reward_before is not True or reward_after is not False:errors.append('fault_did_not_invalidate_success')
    if not isfinite(perturbation_displacement_m) or minimum_displacement_m<=0 or perturbation_displacement_m<minimum_displacement_m:
        errors.append('ineffective_perturbation')
    if pair_id in consumed_pair_ids:errors.append('pair_already_consumed')
    return {'passed':not errors,'errors':errors,'scope':'provenance/perturbation checks, not semantic or training-quality approval'}

def qualification(*,tool_accepted,lift_landed,target_rise_samples_m,
                  external_penetration_samples_m,min_rise_m=0.025,max_depth_m=0.002):
    """Whole-sequence contact and continuous sampled hold; caller establishes sample coverage."""
    rise=list(target_rise_samples_m);depth=list(external_penetration_samples_m)
    finite=bool(rise and depth) and all(isfinite(x) for x in rise+depth)
    held=finite and min(rise)>=min_rise_m
    contact=finite and max(depth)<=max_depth_m
    return {'operational_held':held,'contact_proxy_passed':contact,
            'qualified':bool(tool_accepted and lift_landed and held and contact),
            'not_hardware_safety_certification':True}
