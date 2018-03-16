import logging
from mpf.core.scriptlet import Scriptlet

class SixDigits(Scriptlet):
    def on_load(self):
        self.log = logging.getLogger('Watch for 100k')
        self.log.setLevel('DEBUG')
        self.machine.events.add_handler("player_score",self.check_100k)

    def check_100k(self, **kwargs):
        score = kwargs.get("value")
        num_flash = int(score / 100000)
        player = kwargs.get("player_num")

        if num_flash > 9:
            num_flash == 9

        if score < 100000:
            self.machine.lights['bbl_player_' + str(player) + '_100k'].off()

        if score >= 100000 and score < 200000:
            self.log.debug('100k Lamp ON for Player ' + str(player))
            self.machine.lights['bbl_player_' + str(player) + '_100k'].on()
        if score >= 200000:
            self.machine.shows['flash_100k_' + str(num_flash)].play(show_tokens=dict(light='bbl_player_' + str(player) + '_100k'))
