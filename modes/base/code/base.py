from mpf.core.mode import Mode

class End_of_Ball_Bonus(Mode):

    def mode_start(self, **kwargs):
        self.machine.events.add_handler('logicblock_lb_bonus_hit', self.light_bonus_lamp)
        self.machine.events.add_handler('bonus_max', self.bonus_maxed)
        
        # Clear Match lamps
        self.machine.lights['bbl_match'].remove_from_stack_by_key(key="match")
        for lamp in ['00','10','20','30','40','50','60','70','80','90']:
            self.machine.lights['bbl_match_' + lamp].remove_from_stack_by_key(key="match")

    def bonus_maxed(self, count, **kwargs):
        self.machine.events.remove_handler(self.light_bonus_lamp)
        self.light_bonus_lamp(count)

    def light_bonus_lamp(self, count, **kwargs):
        self.machine.shows['flash'].play(show_tokens=dict(light='pfl_bonus_' + str(count)), speed=10.0, loops=4)
        self.machine.lights['pfl_bonus_' + str(count)].on()
        self.machine.events.post('bonus_lamp_lit')
        self.machine.events.post('bonus_lamp_' + str(count) + '_lit')
