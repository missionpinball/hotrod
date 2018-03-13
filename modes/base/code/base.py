from mpf.core.mode import Mode

class Bonus(Mode):

    def mode_start(self, **kwargs):
        self.machine.events.add_handler('logicblock_lb_bonus_hit', self.light_bonus_lamp)
        
    def light_bonus_lamp(self, count, **kwargs):
        self.machine.events.post('light_bonus_lamp')
        self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_' + str(count)), speed=10.0, loops=4)
        