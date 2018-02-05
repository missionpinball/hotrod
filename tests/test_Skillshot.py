from mpf.tests.MpfGameTestCase import MpfGameTestCase
from mpf.tests.MpfMachineTestCase import MpfMachineTestCase


class TestSkillshot(MpfMachineTestCase, MpfGameTestCase):

    def test_hit(self):
        self.mock_event("sw_skill_shot_success")
        self.mock_event("sw_skill_shot_cancel")
        # start game
        self.hit_and_release_switch("cs_start")
        self.advance_time_and_run(5)
        self.assertGameIsRunning()

        # wait for ball in shooter
        self.assertEqual(1, self.machine.ball_devices.bd_shooter_lane.balls)
        self.assertModeRunning("skill_shot")

        # check default
        self.assertLightFlashing("pfl_top_lane_o")

        # test lane switch
        self.hit_and_release_switch("cs_left_flipper")
        self.assertLightFlashing("pfl_top_lane_h")

        # shoot ball
        self.release_switch_and_run("pfs_shooter_lane", 2)

        # hit skill shot
        self.hit_and_release_switch("pfs_top_lane_h")
        self.advance_time_and_run()
        self.assertModeNotRunning("skill_shot")
        self.assertEventCalled("sw_skill_shot_success")
        self.assertEventNotCalled("sw_skill_shot_cancel")

        self.assertPlayerVarEqual(1000, "score")

    def test_miss(self):
        self.mock_event("sw_skill_shot_success")
        self.mock_event("sw_skill_shot_cancel")
        # start game
        self.hit_and_release_switch("cs_start")
        self.advance_time_and_run(5)
        self.assertGameIsRunning()

        # wait for ball in shooter
        self.assertEqual(1, self.machine.ball_devices.bd_shooter_lane.balls)
        self.assertModeRunning("skill_shot")

        # check default
        self.assertLightFlashing("pfl_top_lane_o")

        # test lane switch
        self.hit_and_release_switch("cs_right_flipper")
        self.assertLightFlashing("pfl_top_lane_t")

        # shoot ball
        self.release_switch_and_run("pfs_shooter_lane", 2)

        # miss skill shot
        self.hit_and_release_switch("pfs_top_lane_h")
        self.advance_time_and_run()
        self.assertModeNotRunning("skill_shot")
        self.assertEventNotCalled("sw_skill_shot_success")
        self.assertEventCalled("sw_skill_shot_cancel")

        self.assertPlayerVarEqual(0, "score")
