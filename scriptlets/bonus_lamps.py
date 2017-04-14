from mpf.core.scriptlet import Scriptlet

class bonus_lamps(Scriptlet):

    def on_load(self):
        self.machine.events.add_handler('logicblock_bonus_hit', self.light_bonus)

    def light_bonus(self):
        bonus_total = self.machine.game.player["logicblock_bonus"]

		for bonus_count in range(0,10000,1000):
			if bonus_count <= bonus_total
			    self.machine.lights["pfl_bonus_".bonus_count].on()
