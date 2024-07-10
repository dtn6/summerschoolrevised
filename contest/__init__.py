import random

from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    models,
    Page,
    WaitPage,
)


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'contest'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    ENDOWMENT = 20
    COST_PER_TICKET = {1: 1, 2: 2}
    PRIZE = 20


class Subsession(BaseSubsession):
    is_paid = models.BooleanField()

    def setup(self):
        self.is_paid = (self.round_number == 1)
        self.group_randomly()
        for group in self.get_groups():
            group.setup()


class Group(BaseGroup):
    def setup(self):
        for player in self.get_players():
            player.setup()

    def determine_outcomes(self):
        tickets = []
        for player in self.get_players():
            for i in range(player.ticket_purchase):
                tickets.append(player.id_in_group)
        if not tickets:
            for player in self.get_players():
                tickets.append(player.id_in_group)
        print(tickets)
        winning_id = random.choice(tickets)
        for player in self.get_players():
            player.is_winner = (player.id_in_group == winning_id)
            player.earnings = player.endowment - player.cost_per_ticket*player.tickets_purchase+player.is_winner*C.PRIZE

            if self.subsession.is_paid:
                player.payoff = player.earnings


class Player(BasePlayer):
    endowment = models.IntegerField()
    cost_per_ticket = models.FloatField()
    tickets_purchase = models.IntegerField()
    is_winner = models.BooleanField()
    earnings = models.IntegerField()

    def setup(self):
        self.endowment = C.ENDOWMENT
        self.cost_per_ticket = C.COST_PER_TICKET[self.id_in_group]

    @property
    def coplayer(self):
            return self.get_others_in_group()[0]


def creating_session(subsession):
    subsession.setup()


# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


class SetupRound(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.setup()


class Decision(Page):
    form_model = "player"

    @staticmethod
    def get_form_fields(player):
        return ["tickets_purchase"]


class WaitforDecision(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        for group in subsession.get_groups():
            group.setup()


class Results(Page):
    pass


class EndBlock(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Intro,
    SetupRound,
    Decision,
    WaitforDecision,
    Results,
    EndBlock
]
