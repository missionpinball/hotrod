from mpf.core.mode import Mode
from mpf.core.delays import DelayManager
from time import sleep
from random import *

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
        player_1_score = self.machine.game.player_list[0].score
            
        self.log.info("Player 1 score: " + str(player_1_score))
        match_score_player_1 = '{:02}'.format(int(str(int(str(player_1_score)[-2:]))[-2:1]) * 10)
        self.log.info("Player 1 Match Score: " + str(match_score_player_1))

        if self.match == match_score_player_1:
            self.player_1_match = True
            self.player_match = True

        # If a 2 player game, also determine last two digits for player 2
        if self.machine.game.num_players == 2:
            player_2_score = self.machine.game.player_list[1].score
                
            match_score_player_2 = '{:02}'.format(int(str(int(str(player_2_score)[-2:]))[-2:1]) * 10)

            if self.match == match_score_player_2:
                self.player_2_match = True
                self.player_match = True

        self.machine.events.post('match_' + self.match)
        
        match_show = randint(1,3)
        self.log.info("Match Show: " + str(match_show))

        if match_show == 1:
            self.match_show_circle_right()
        if match_show == 2:
            self.match_show_circle_left()
        if match_show == 3:
            self.match_show_classic()
        
        self.match_done()

    def match_show_classic(self):
        # Just turn on lamps
        self.machine.events.post('match_show_classic')
        self.machine.lights['bbl_match'].on(key="match")
        self.machine.lights[self.match_light].on(key="match")
        self.match_done()

    def match_show_circle_right(self):
        # Rotating Match lamps
        self.machine.events.post('match_show_circle_right')
        match_numbers_circle = ['00','20','40','60','80','90','70','50','30','10']
         
        self.machine.shows['match_circle_right'].play(loops=4)

        previous_match_light_circle = 'bbl_match_00'

        for lamp in match_numbers_circle:
            match_light_circle = 'bbl_match_' + lamp

            self.machine.lights[previous_match_light_circle].off(key="match")
            self.machine.lights[match_light_circle].on(key="match")
            
            if lamp == self.match:
                break

            previous_match_light_circle = match_light_circle

        if self.player_match:
            self.machine.shows['flash'].play(show_tokens=dict(light=match_light_circle), speed=10.0, loops=8)

        self.match_done()

    def match_show_circle_left(self):
        # Rotating Match lamps
        self.machine.events.post('match_show_circle_left')
        match_numbers_circle = ['90','70','50','30','10','00','20','40','60','80']
         
        self.machine.shows['match_circle_left'].play(loops=4)

        previous_match_light_circle = 'bbl_match_90'

        for lamp in match_numbers_circle:
            match_light_circle = 'bbl_match_' + lamp

            self.machine.lights[previous_match_light_circle].off(key="match")
            self.machine.lights[match_light_circle].on(key="match")
            yield from asyncio.sleep(0.2)
            
            if lamp == self.match:
                break

            previous_match_light_circle = match_light_circle

        if self.player_match:
            self.machine.shows['flash'].play(show_tokens=dict(light=match_light_circle), speed=10.0, loops=8)

        self.match_done()

    def match_done(self):
        # Leave Match and Match Number lit
        self.machine.lights['bbl_match'].on(key="match")
        self.machine.lights[self.match_light].on(key="match")

        # Fire knocker if match
        if self.player_1_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_1')
        if self.player_2_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_2')

        self.machine.events.post('match_code_ended')
           
