from mpf.core.mode import Mode
from mpf.core.delays import DelayManager
from mpf.core.utility_functions import Util

class Count(Mode):

    def mode_start(self, **kwargs):
        self.bonus_value = 1000
        self.count_down = self.machine.counters.lb_bonus.value
        self.machine.events.post("bonus_code_starting_value_" + str(self.count_down))
        self.prepare_bonus()

    def prepare_bonus(self):
        if self.machine.game.tilted:
            self.machine.events.post("bonus_code_tilt_stop")
            self.stop()
            return

        self.check_score_reels()

    def check_score_reels(self, **kwargs):
        self.machine.events.post("bonus_code_check_score_reels_valid")
        if self.player['player_number'] == 1:
            ready_future = Util.ensure_future(self.machine.score_reel_groups.player1.wait_for_ready(), loop=self.machine.clock.loop)
        else:
            ready_future = Util.ensure_future(self.machine.score_reel_groups.player2.wait_for_ready(), loop=self.machine.clock.loop)

        ready_future.add_done_callback(self.bonus_step)

    def bonus_step(self, future=None, **kwargs):
        self.machine.events.post("bonus_code_step")
        if self.count_down > 0:
            self.delay.add(ms=500, callback=self.do_bonus_step)
        else:
            self.bonus_pause()
            
    def do_bonus_step(self):
        self.machine.events.post("bonus_code_countdown_" + str(self.count_down))
        self.player.score += self.bonus_value

        if self.count_down >= 10000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_10000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_10000.off()
        elif self.count_down == 9000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_9000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_9000.off()
        elif self.count_down == 8000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_8000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_8000.off()
        elif self.count_down == 7000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_7000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_7000.off()
        elif self.count_down == 6000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_6000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_6000.off()
        elif self.count_down == 5000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_5000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_5000.off()
        elif self.count_down == 4000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_4000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_4000.off()
        elif self.count_down == 3000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_3000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_3000.off()
        elif self.count_down == 2000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_2000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_2000.off()
        elif self.count_down <= 1000:
            self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_1000'), speed=10.0, loops=3)
            self.machine.lights.pfl_bonus_1000.off()

        self.count_down -= self.bonus_value

        self.check_score_reels()

    def bonus_pause(self):
        self.delay.add(ms=1000, callback=self.bonus_done)

    def bonus_done(self):
        self.machine.events.post("bonus_complete")
        self.stop()
