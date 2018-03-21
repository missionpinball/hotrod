from mpf.core.mode import Mode
from mpf.core.delays import DelayManager
from random import *

class Match(Mode):

    def mode_start(self, **kwargs):
        player_1_match = False
        player_2_match = False
  
        match_score_player_1 = 0
        match_score_player_2 = 0
        
        match_numbers = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        shuffle(match_numbers)
        match = int(match_numbers[0])
        
        player_1_score = self.machine.get_machine_var('player1_score')

        if self.machine.game.num_players == 2:
            player_2_score = self.machine.get_machine_var('player2_score')
        else:
            player_2_score = 0

        if player_1_score > 9:
            match_score_player_1 = int(str(int(str(player_1_score)[-2:]))[-2:1]) * 10
        if player_2_score > 9:
            match_score_player_2 = int(str(int(str(player_2_score)[-2:]))[-2:1]) * 10
        
        if match == match_score_player_1:
            player_1_match = True
            
        if self.machine.game.num_players == 2:
            if match == match_score_player_2:
                player_2_match = True
        
        self.machine.lights['bbl_match'].on()

        if match == 0:
            self.machine.lights['bbl_match_00'].on()
        else:
            self.machine.lights['bbl_match_' + str(match)].on()
            
        self.machine.events.post('match_' + str(match))

        if player_1_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_1')
        if player_2_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_2')

        self.stop()
        