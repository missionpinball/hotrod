from mpf.core.scriptlet import Scriptlet

class player_100k(Scriptlet):

    def on_load(self):
        self.machine.events.add_handler('scorereelgroup_player1_rollover', self.flash_lamp_player1)
        self.machine.events.add_handler('scorereelgroup_player2_rollover', self.flash_lamp_player2)

    def flash_lamp_player1(self):
        if self.machine.game.player1.score >= 100000:
            flashes = int(self.machine.game.player1.score / 100000)
            self.machine.events.post('flash_player_1_' + flashes + '_times')

    def flash_lamp_player2(self):
        if self.machine.game.player2.score >= 100000:
            flashes = int(self.machine.game.player2.score / 100000)
            self.machine.events.post('flash_player_2_' + flashes + '_times')
            
