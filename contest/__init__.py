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
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.IntegerField()
    cost_per_ticket = models.FloatField()
    tickets_purchase = models.IntegerField()
    is_winner = models.BooleanField()
    earnings = models.IntegerField()


# PAGES
class Intro(Page):
    pass


class SetupRound(WaitPage):
    pass


class Decision(Page):
    pass


class WaitforDecision(WaitPage):
    pass


class Results(Page):
    pass


class EndBlock(Page):
    pass


page_sequence = [
    Intro,
    SetupRound,
    Decision,
    WaitforDecision,
    Results,
    EndBlock
]
