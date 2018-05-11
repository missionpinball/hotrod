import asyncio

from mpf.core.async_mode import AsyncMode
from random import *

class Match(AsyncMode):

    @asyncio.coroutine
    def _run(self):
        self.player_1_match = False
        self.player_2_match = False
        self.player_match = False
        player_1_score = 0
        player_2_score = 0
        self.match_numbers = ['00', '10', '20', '30', '40', '50', '60', '70', '80', '90']

        for loop in self.match_numbers:
            self.machine.lights[loop].off(key="match")

        random_match_numbers = self.match_numbers
        shuffle(random_match_numbers)
        self.match = random_match_numbers[0]
        self.match_light = "bbl_match_" + self.match

        self.machine.lights['bbl_match'].on(key="match")

        # Determine last two digits of player 1 score for match
        player_1_score = self.machine.game.player_list[0].score

        self.log.info('Player 1 score: ' + str(player_1_score))
        match_score_player_1 = '{:02}'.format(int(str(int(str(player_1_score)[-2:]))[-2:1]) * 10)
        self.log.info('Player 1 Match Score: ' + str(match_score_player_1))

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
        self.log.info('Match Show: ' + str(match_show))

        #if match_show == 1:
        yield from self.match_show_circle_right()
        #if match_show == 2:
        #    self.match_show_circle_left()
        #if match_show == 3:
        #    self.match_show_classic()

        yield from self.match_done()

    @asyncio.coroutine
    def match_show_classic(self):
        # Just turn on lamps
        self.machine.events.post('match_show_classic')
        self.machine.lights['bbl_match'].on(key="match")
        self.machine.lights[self.match_light].on(key="match")
        self.match_flash()

    @asyncio.coroutine
    def match_show_circle_right(self):
        # Rotating Match lamps
        self.machine.events.post('match_show_circle_right')
        self.machine.shows['match_circle_right'].play(events_when_completed=["match_show_circle_right_complete"],loops=0)
        # wait for show to finish
        yield from self.machine.events.wait_for_event("match_show_circle_right_complete")
        yield from self.match_show_circle_right_complete()

    @asyncio.coroutine
    def match_show_circle_right_complete(self, **kwargs):
        match_numbers_circle = ['00','20','40','60','80','90','70','50','30','10']

        previous_match_light_circle = 'bbl_match_00'

        for lamp in match_numbers_circle:
            match_light_circle = 'bbl_match_' + lamp

            self.machine.lights[previous_match_light_circle].off(key="match")
            self.machine.lights[match_light_circle].on(key="match")
            yield from asyncio.sleep(0.1)

            if lamp == self.match:
                break

            previous_match_light_circle = match_light_circle

        yield from self.match_flash()

    @asyncio.coroutine
    def match_flash(self):
        # Flash Match number if matched
        if self.player_match:
            self.machine.shows['flash'].play(show_tokens=dict(light=match_light_circle), loops=5, speed=4)

        self.match_done()

    @asyncio.coroutine
    def match_done(self):
        self.machine.lights[self.match_light].on(key="match")

        # Fire knocker if match
        if self.player_1_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_1')
        if self.player_2_match:
            self.machine.shows['match_knocker'].play(loops=0)
            self.machine.events.post('match_player_2')

        self.machine.events.post('match_code_ended')
     
