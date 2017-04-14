from mpf.tests.MpfGameTestCase import MpfGameTestCase
from mpf.tests.MpfMachineTestCase import MpfMachineTestCase


class TestMultiball(MpfMachineTestCase, MpfGameTestCase):

    def test_lock_on_skillshot_and_three_ball(self):
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

        # should do nothing
        self.hit_and_release_switch("pfs_left_eject")

        self.assertModeNotRunning("2ball")
        self.assertModeNotRunning("3ball")

        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeRunning("lock")
        self.assertModeNotRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_right_saucer", 5)
        self.assertModeNotRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeNotRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(0)
        self.assertBallsInPlay(1)
        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(1)
        self.assertEqual(1, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertEqual(0, self.machine.ball_devices.bd_right_saucer.balls)

        self.hit_switch_and_run("pfs_right_saucer", 5)
        self.assertBallsOnPlayfield(0)
        self.assertBallsInPlay(1)
        self.assertEqual(1, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertEqual(1, self.machine.ball_devices.bd_right_saucer.balls)

        self.assertFalse(self.machine.multiballs.mb_2ball.balls_added_live)
        self.assertFalse(self.machine.multiballs.mb_3ball.balls_added_live)

        self.assertModeNotRunning("2ball")
        self.assertModeRunning("3ball")

        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(1)

        self.assertTrue(self.machine.multiballs.mb_3ball.balls_added_live)
        self.assertTrue(self.machine.multiballs.mb_3ball.shoot_again)
        self.advance_time_and_run(3)

        self.assertEqual(0, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertEqual(0, self.machine.ball_devices.bd_right_saucer.balls)
        self.assertBallsInPlay(3)
        self.assertBallsOnPlayfield(3)

        self.drain_ball()
        self.advance_time_and_run(3)
        self.assertBallsInPlay(3)
        self.assertBallsOnPlayfield(2)

        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(3)
        self.assertBallsInPlay(3)

        self.advance_time_and_run(10)
        self.drain_ball()

        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(2)
        self.assertBallsInPlay(2)

        self.advance_time_and_run(10)
        self.drain_ball()
        self.advance_time_and_run()
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.assertBallNumber(1)
        self.assertModeRunning("saucer")

        self.drain_ball()
        self.advance_time_and_run()
        self.assertBallsOnPlayfield(0)
        self.assertBallsInPlay(1)
        self.assertBallNumber(2)

        # check default
        self.assertLightFlashing("pfl_top_lane_o")

        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.assertModeRunning("saucer")

        self.assertModeRunning("skill_shot")
        self.assertModeNotRunning("lock")
        self.assertModeRunning("saucer")

        # make skill shot
        self.hit_and_release_switch("pfs_top_lane_o")
        self.advance_time_and_run()

        self.assertModeNotRunning("skill_shot")
        self.assertModeRunning("lock")
        self.assertModeNotRunning("saucer")

        # try again
        # should do nothing
        self.hit_and_release_switch("pfs_left_eject")

        self.assertModeNotRunning("2ball")
        self.assertModeNotRunning("3ball")

        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeRunning("lock")
        self.assertModeNotRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeNotRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeNotRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(0)
        self.assertBallsInPlay(1)
        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(1)
        self.assertEqual(1, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertEqual(0, self.machine.ball_devices.bd_right_saucer.balls)

        self.hit_switch_and_run("pfs_right_saucer", 5)
        self.assertBallsOnPlayfield(0)
        self.assertBallsInPlay(1)
        self.assertEqual(1, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertEqual(1, self.machine.ball_devices.bd_right_saucer.balls)

        self.assertFalse(self.machine.multiballs.mb_2ball.balls_added_live)
        self.assertFalse(self.machine.multiballs.mb_3ball.balls_added_live)

        self.assertModeNotRunning("2ball")
        self.assertModeRunning("3ball")

        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(1)

    def test_lock_on_drop_targets_and_two_ball(self):
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
        self.assertModeRunning("saucer")

        self.hit_switch_and_run("pfs_drop_r", 1)
        self.hit_switch_and_run("pfs_drop_o", 1)
        self.hit_switch_and_run("pfs_drop_d", 1)

        self.assertModeRunning("lock")
        self.assertModeNotRunning("saucer")

        # should do nothing
        self.hit_and_release_switch("pfs_left_eject")

        self.assertModeNotRunning("2ball")
        self.assertModeNotRunning("3ball")

        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeRunning("lock")
        self.assertModeNotRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeNotRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeNotRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(0)
        self.assertBallsInPlay(1)
        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(1)
        self.assertEqual(1, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertFalse(self.machine.multiballs.mb_2ball.balls_added_live)

        self.hit_and_release_switch("pfs_left_eject")
        self.advance_time_and_run(3)
        self.assertEqual(0, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertBallsInPlay(2)
        self.assertBallsOnPlayfield(2)
        self.assertModeRunning("2ball")
        self.assertModeNotRunning("3ball")

        self.assertTrue(self.machine.multiballs.mb_2ball.balls_added_live)
        self.assertTrue(self.machine.multiballs.mb_2ball.shoot_again)

        self.drain_ball()
        self.advance_time_and_run(3)
        self.assertBallsInPlay(2)
        self.assertBallsOnPlayfield(1)

        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(2)
        self.assertBallsInPlay(2)

        self.advance_time_and_run(10)
        self.drain_ball()
        self.advance_time_and_run()
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.assertBallNumber(1)
        self.assertModeRunning("saucer")

        self.drain_ball()
        self.advance_time_and_run()
        self.assertBallsOnPlayfield(0)
        self.assertBallsInPlay(1)
        self.assertBallNumber(2)

        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.assertModeRunning("saucer")

        # check default
        self.assertLightFlashing("pfl_top_lane_o")

        # miss again
        self.hit_and_release_switch("pfs_top_lane_h")
        self.advance_time_and_run()
        self.assertModeNotRunning("skill_shot")
        self.assertModeNotRunning("lock")
        self.assertModeRunning("saucer")

        self.hit_switch_and_run("pfs_drop_r", 1)
        self.hit_switch_and_run("pfs_drop_o", 1)
        self.hit_switch_and_run("pfs_drop_d", 1)

        self.assertModeRunning("lock")
        self.assertModeNotRunning("saucer")

        # should do nothing
        self.hit_and_release_switch("pfs_left_eject")

        self.assertModeNotRunning("2ball")
        self.assertModeNotRunning("3ball")

        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeRunning("lock")
        self.assertModeNotRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeNotRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(1)
        self.assertBallsInPlay(1)
        self.hit_switch_and_run("pfs_left_saucer", 5)
        self.assertModeNotRunning("lock")
        self.assertModeRunning("lock_lit")
        self.assertBallsOnPlayfield(0)
        self.assertBallsInPlay(1)
        self.release_switch_and_run("pfs_shooter_lane", 4)
        self.assertBallsOnPlayfield(1)
        self.assertEqual(1, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertFalse(self.machine.multiballs.mb_2ball.balls_added_live)

        self.hit_and_release_switch("pfs_left_eject")
        self.advance_time_and_run(3)
        self.assertEqual(0, self.machine.ball_devices.bd_left_saucer.balls)
        self.assertBallsInPlay(2)
        self.assertBallsOnPlayfield(2)
        self.assertModeRunning("2ball")
        self.assertModeNotRunning("3ball")

        self.assertTrue(self.machine.multiballs.mb_2ball.balls_added_live)
        self.assertTrue(self.machine.multiballs.mb_2ball.shoot_again)

