from mpf.core.mode import Mode
from random import shuffle
from time import sleep

class Match(Mode):

    def mode_start(self, **kwargs):
        self.player_1_match = False
        self.player_2_match = False
        self.player_match = False
        player_1_score = 0
        player_2_score = 0
        self.match_numbers = ['00', '10', '20', '30', '40', '50', '60', '70', '80', '90']

        random_match_numbers = self.match_numbers
        shuffle(random_match_numbers)
        self.match = random_match_numbers[0]
        self.match_light = "bbl_match_" + self.match
        
        # Determine last two digits of player 1 score for match
        player_1_score = self.machine.get_machine_var('player1_score')
        match_score_player_1 = '{:02}'.format(int(str(int(str(player_1_score)[-2:]))[-2:1]) * 10)

        if self.match == match_score_player_1:
            self.player_1_match = True
            self.player_match = True

        # If a 2 player game, also determine last two digits for player 2
        if self.machine.game.num_players == 2:
            player_2_score = self.machine.get_machine_var('player2_score')
            match_score_player_2 = '{:02}'.format(int(str(int(str(player_2_score)[-2:]))[-2:1]) * 10)

            if match == match_score_player_2:
                self.player_2_match = True
                self.player_match = True

        self.machine.events.post('match_' + self.match)

        self.match_show_circle()
        
    def match_show_classic(self):
        # Just turn on lamps
        self.machine.lights['bbl_match'].on()
        self.machine.lights[self.match_light].on()
        self.match_done()

    def match_show_circle(self):
        # Rotating Match lamps
        self.machine.shows['match_circle'].play(loops=4)

        previous_match_light_circle = 'bbl_match_90'

        for lamp in self.match_numbers:
            match_light_circle = 'bbl_match_' + lamp

            self.machine.lights[previous_match_light_circle].off()
            self.machine.lights[match_light_circle].on()
            sleep(2)
            
            if lamp == self.match:
                break

            previous_match_light_circle = match_light_circle

        if self.player_match:
            self.machine.shows['flash'].play(show_tokens=dict(light=match_light_circle), speed=10.0, loops=8)

        self.match_done()

    def match_done(self):
        # Leave Match and Match Number lit
        self.machine.lights['bbl_match'].on()
        self.machine.lights['bbl_match_10'].on()
        self.machine.lights[self.match_light].on()

        # Fire knocker if match
        if self.player_1_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_1')
        if self.player_2_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_2')

        self.machine.events.post('match_code_ended')
        self.stop()
           