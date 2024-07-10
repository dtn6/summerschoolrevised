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


class Constants(BaseConstants):
    name_in_url = 'encoding_task'
    players_per_group = None
    num_rounds = 2
    letters = {'A': 1, 'B': 2}
    reward = 5

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    shown_letter = models.StringField()
    entered_code = models.IntegerField(min=1, max=2)
    is_correct = models.BooleanField()
    payoff_round = models.IntegerField()

# PAGES
class Introduction(Page):
    pass

class EncodingTask(Page):
    form_model = 'player'
    form_fields = ['entered_code']

    @staticmethod
    def vars_for_template(player: Player):
        import random
        player.shown_letter = random.choice(list(Constants.letters.keys()))
        return {
            'shown_letter': player.shown_letter,
            'round_number': player.round_number,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.is_correct = (player.entered_code == Constants.letters[player.shown_letter])

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'is_correct': player.is_correct,
            'correct_code': Constants.letters[player.shown_letter],
        }

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.round_number == Constants.num_rounds:
            player.payoff_round = random.randint(1, Constants.num_rounds)
            player.participant.payoff = Constants.reward if player.in_round(player.payoff_round).is_correct else 0

page_sequence = [EncodingTask, Results]