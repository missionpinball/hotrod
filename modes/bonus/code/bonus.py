from mpf.core.mode import Mode

class Count(Mode):

    def mode_start(self, **kwargs):
        #if not self.machine.mode_controller.is_active('base'):
        #    self.machine.events.post("bonus_complete")
        #    self.stop()

        self.bonus_value = 0
        self.count_down = self.player['c_bonus_count']
        self.log.debug("Bonus: " + str(self.count_down))
        self.prepare_bonus()

    def prepare_bonus(self):
        if self.machine.game.tilted:
            self.log.debug("Ball has tilted. No bonus for you!")
            return
        
        self.bonus_value = (self.config['scoring']['bonusvalue']['score'])
        self.check_score_reels()

    def check_score_reels(self, **kwargs):
        self.reels = self.machine.score_reel_controller.active_scorereelgroup

        if not self.reels.valid:
            self.add_mode_event_handler('scorereelgroup_{}_valid'.format(self.reels.name),self.start_bonus)
        else:
            self.start_bonus()

    def start_bonus(self, **kwargs):
        # remove the handler that we used to wait for the score reels to be done
        self.machine.events.remove_handler(self.start_bonus)

        # add the handler that will advance through these bonus steps
        self.add_mode_event_handler('scorereelgroup_{}_valid'.format(self.reels.name), self.bonus_step)

        # do the first bonus step to kick off this process
        self.bonus_step()

    def bonus_step(self, **kwargs):
        # automatically called when the score reels are valid
        if self.count_down > 0:
            # sets the "pause" between bonus scores, then does the bonus step
            self.delay.add(ms=200, callback=self.do_bonus_step)
        else:
            self.bonus_done()
            
    def do_bonus_step(self):
        self.log.debug("Countdown: " + str(self.count_down))

        if self.count_down >= 10000:
            self.machine.lights.pfl_bonus_10000.off()
        elif self.count_down == 9000:
            self.machine.lights.pfl_bonus_9000.off()
        elif self.count_down == 8000:
            self.machine.lights.pfl_bonus_8000.off()
        elif self.count_down == 7000:
            self.machine.lights.pfl_bonus_7000.off()
        elif self.count_down == 6000:
            self.machine.lights.pfl_bonus_6000.off()
        elif self.count_down == 5000:
            self.machine.lights.pfl_bonus_5000.off()
        elif self.count_down == 4000:
            self.machine.lights.pfl_bonus_4000.off()
        elif self.count_down == 3000:
            self.machine.lights.pfl_bonus_3000.off()
        elif self.count_down == 2000:
            self.machine.lights.pfl_bonus_2000.off()
        elif self.count_down <= 1000:
            self.machine.lights.pfl_bonus_1000.off()

        self.machine.scoring.add(self.bonus_value)
        self.count_down -= self.bonus_value

    def bonus_done(self):
        self.machine.events.post("bonus_complete")

    def mode_stop(self, **kwargs):
        pass