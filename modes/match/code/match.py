from mpf.core.mode import Mode
from mpf.core.delays import DelayManager
from random import *

class Match(Mode):

    def mode_start(self, **kwargs):
        self.player_1_match = False
        self.player_2_match = False
  
        self.match_numbers = ['00', '10', '20', '30', '40', '50', '60', '70', '80', '90']
        shuffle(self.match_numbers)
        self.match = self.match_numbers[0]
        self.match_light = "bbl_match_" + self.match
        
        # Determine last two digits of player 1 score for match
        self.player_1_score = self.machine.get_machine_var('player1_score')
        self.match_score_player_1 = '{:02}'.format(int(str(int(str(self.player_1_score)[-2:]))[-2:1]) * 10)

        if self.match == self.match_score_player_1:
            self.player_1_match = True
            self.player_match = True

        # If a 2 player game, also determine last two digits for player 2
        if self.machine.game.num_players == 2:
            self.player_2_score = self.machine.get_machine_var('player2_score')
            self.match_score_player_2 = '{:02}'.format(int(str(int(str(self.player_2_score)[-2:]))[-2:1]) * 10)

            if self.match == self.match_score_player_2:
                self.player_2_match = True
                self.player_match = True

        self.machine.events.post('match_' + self.match)
        self.machine.lights['bbl_match'].on()
        self.machine.lights[self.match_light ].on()

        if self.player_1_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_1')
        if self.player_2_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_2')

        self.machine.events.post('match_code_ended')
        self.stop()
           