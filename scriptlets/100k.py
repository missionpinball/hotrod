import logging
from mpf.core.scriptlet import Scriptlet

class SixDigits(Scriptlet):
    def on_load(self):
        self.log = logging.getLogger('Watch for 100k')
        self.log.setLevel('DEBUG')
        self.machine.events.add_handler("player_score",self.check_100k)
    
    def check_100k(self, **kwargs):
        score = kwargs.get("value")
        player = kwargs.get("player_num")
        
        if score >= 100000:
            self.log.debug('100k Lamp ON for Player ' + str(player))
            self.machine.lights['bbl_player_' + str(player) + '_100k'].on()
        else:
            #self.log.debug('100k Lamp OFF for Player ' + str(player))
            self.machine.lights['bbl_player_' + str(player) + '_100k'].off()