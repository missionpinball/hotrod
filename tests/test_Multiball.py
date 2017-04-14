from mpf.tests.MpfGameTestCase import MpfGameTestCase
from mpf.tests.MpfMachineTestCase import MpfMachineTestCase


class TestMultiball(MpfMachineTestCase, MpfGameTestCase):

    def test_lock_on_skillshot(self):
        # start game
        self.hit_and_release_switch("cs_start")
        self.advance_time_and_run(5)
        self.assertGameIsRunning()

        # wait for ball in shooter
        self.assertEqual(1, self.machine.ball_devices.bd_shooter_lane.balls)
        self.assertModeRunning("skill_shot")

        # check default
        self.assertLightFlashing("pfl_top_lane_o")

        # shoot ball
        self.release_switch_and_run("pfs_shooter_lane", 2)

        # hit skill shot
        self.hit_and_release_switch("pfs_top_lane_o")
        self.advance_time_and_run()
        self.assertModeNotRunning("skill_shot")
        self.assertModeRunning("lock")

    def test_lock_on_drop_targets(self):
        # start game
        self.hit_and_release_switch("cs_start")
        self.advance_time_and_run(5)
        self.assertGameIsRunning()

        # wait for ball in shooter
        self.assertEqual(1, self.machine.ball_devices.bd_shooter_lane.balls)
        self.assertModeRunning("skill_shot")

        # check default
        self.assertLightFlashing("pfl_top_lane_o")

        # shoot ball
        self.release_switch_and_run("pfs_shooter_lane", 2)

        # miss skill shot
        self.hit_and_release_switch("pfs_top_lane_h")
        self.advance_time_and_run()
        self.assertModeNotRunning("skill_shot")
        self.assertModeNotRunning("lock")

        self.hit_switch_and_run("pfs_drop_r", 1)
        self.hit_switch_and_run("pfs_drop_o", 1)
        self.hit_switch_and_run("pfs_drop_d", 1)

        self.assertModeRunning("lock")

        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeRunning("lock")
        self.assertModeNotRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(0)
        self.assertBallsInPlay(1)
        self.release_switch_and_run("pfs_shooter_lane", 11)
        self.assertBallsOnPlayfield(1)
        self.assertEqual(1, self.machine.ball_devices.bd_left_saucer.balls)

        self.hit_and_release_switch("pfs_left_eject")
        self.advance_time_and_run(11)
        self.assertEqual(0, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertBallsInPlay(2)
        self.assertBallsOnPlayfield(2)
