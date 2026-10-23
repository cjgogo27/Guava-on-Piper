import unittest,math
from pathlib import Path
from guava_piper_audit.reproduce import reproduce
from guava_piper_audit.geometry import tcp_for_contact_goal,contact_point
from guava_piper_audit.contracts import qualification,validate_branch
from guava_piper_audit.interface import audit_records
from guava_piper_audit.statistics import exact_mcnemar,holm

class ReleaseTests(unittest.TestCase):
    def test_released_tables(self):
        out=reproduce(Path(__file__).resolve().parents[1]);self.assertEqual(out['G1']['counts']['H'],39)
    def test_pose_changed_between_segments(self):
        goal=[.2,.1,.3];offset=[0,0,.03];q=[math.sqrt(.5),0,math.sqrt(.5),0]
        tcp=tcp_for_contact_goal(goal,q,offset)
        for x,y in zip(contact_point(tcp,q,offset),goal):self.assertAlmostEqual(x,y)
        stale=tcp_for_contact_goal(goal,[1,0,0,0],offset)
        self.assertGreater(math.dist(contact_point(stale,q,offset),goal),.04)
    def test_prefix_collision_not_hidden_by_held(self):
        x=qualification(tool_accepted=True,lift_landed=True,target_rise_samples_m=[.03]*20,external_penetration_samples_m=[.003,0,0])
        self.assertTrue(x['operational_held']);self.assertFalse(x['qualified'])
    def test_nonfinite_and_empty_not_qualified(self):
        for samples in [[],[float('nan')]]:
            self.assertFalse(qualification(tool_accepted=True,lift_landed=True,target_rise_samples_m=samples,external_penetration_samples_m=[0])['qualified'])
    def test_unsupported_arg_retained(self):
        records=[{'messages':[{'role':'assistant','tool_calls':[{'function':{'name':'move','arguments':'{"motion_mode":"preserve_tcp","target_position":[0,0,0]}'}}]}]}]
        self.assertEqual(audit_records(records,{'move':['target_position']})['affected_records'],{'move.motion_mode':1})
        self.assertIn('motion_mode',records[0]['messages'][0]['tool_calls'][0]['function']['arguments'])
    def test_stale_image_and_model_rejected(self):
        x=validate_branch(saved_parent_image=b'a',current_parent_image=b'a',teacher_fault_image=b'old',actual_fault_image=b'new',parent_model_sha256='a',restored_model_sha256='b',reward_before=True,reward_after=False,perturbation_displacement_m=.08,minimum_displacement_m=.07,consumed_pair_ids=set(),pair_id='x')
        self.assertEqual(x['errors'],['stale_teacher_image','parent_model_changed'])
    def test_exact_tests(self):
        self.assertAlmostEqual(exact_mcnemar(7,1),.0703125);self.assertEqual(exact_mcnemar(0,0),1)
        self.assertEqual(holm([.0703125,.1796875]),[.140625,.1796875])

if __name__=='__main__':unittest.main()
