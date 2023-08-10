from otree.api import *
import random

doc = """

""" 

class C(BaseConstants):
    NAME_IN_URL = 'uu'

    ####################### Player Numbers
    NUM_OF_GREEN = 4
    NUM_OF_T1_BLUE = 2
    NUM_OF_T2_BLUE = 2
    PLAYERS_PER_GROUP = 1 + NUM_OF_GREEN + NUM_OF_T1_BLUE + NUM_OF_T2_BLUE

    ########################### Round Number
    NUM_ROUNDS = 30

    ########################### Job Reward Multipliers
    JOB_A_SOLVER_MUL = 0.5
    JOB_B_SOLVER_MUL = 0.25
    JOB_B_ASSIGNER_MUL = 0.8
    JOB_B_ASSIGNER_MUL = 0.5

    ########################### Type 2
    TYPE_2_JOB_A_TASK_COUNT_PER_ROUND = 2
    USE_POINTS = True

def set_as_assigner(player:Player):
    player.is_assigner = True
    player.assigner_id = player.id_in_group

def set_as_BLUE(player:Player, is_type_1 = True):
    player.is_assigner = False
    player.is_GREEN = False
    player.is_type_1 = is_type_1

def set_roles(group: Group):
    players = group.get_players()
    roles = ["A"] + ["G"]*C.NUM_OF_GREEN + ["B1"]*C.NUM_OF_T1_BLUE + ["B0"]*C.NUM_OF_T2_BLUE

    for player in players:
        randomRole = roles.pop(random.randrange(len(roles)))

        if randomRole == "A":
            set_as_assigner(player)

        elif randomRole == "G":
            pass

        elif randomRole == "B1":
            set_as_BLUE(player, True)

        elif randomRole == "B0":
            set_as_BLUE(player, False) 

def set_type2_permission(group:Group):
    players = group.get_players()
    randomPlayer = random.choice(players)
    while randomPlayer.is_assigner or player.is_type_1:
        randomPlayer = random.choice(players)

    for p in players:
        p.type_2_allowed = randomPlayer.allow_type_2
        if not (p.is_type_1):
            p.is_allowed_in_round = randomPlayer.allow_type_2


def set_jobs(group:Group):
    players = group.get_players()
    assigner = None
    
    for player in players:
        if player.is_assigner:
            assigner = player
            players.remove(player)
            break

    if assigner.type_2_allowed:
        job_set = [assigner.g1, assigner.g2, assigner.g3, assigner.g4, assigner.b1, assigner.b2, assigner.b3, assigner.b4]
    else:
        job_set = [assigner.g1, assigner.g2, assigner.g3, assigner.g4, assigner.b3, assigner.b4]

    green_count = 0
    for player in players:
        if player.is_GREEN:
            player.job_A = job_set.pop(0)
            player.assigner_id = assigner.assigner_id
            green_count+=1
        else:
            if player.is_allowed_in_round:
                player.job_A = job_set.pop(4 - green_count)
                player.assigner_id = assigner.assigner_id
    
def calculate_payoff(group):
    players = group.get_players()
    for player in players:
        pass
    

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass



class Player(BasePlayer):
    allow_type_2 = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    g1 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    g2 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    g3 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    g4 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    b1 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    b2 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    b3 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    b4 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    is_assigner = False
    is_GREEN = True
    is_type_1 = True
    is_allowed_in_round = True
    job_A = True
    type_2_allowed = True
    num1 = random.randint(1,10)
    num2 = random.randint(1,10)
    correct_ans = num1*num2
    answered = models.models.IntegerField()
    correct = 0
    assigner_id = None
    job_done = [0,0]

#pages
class WaitForPlayers(WaitPage):
    after_all_players_arrive = set_roles
    def is_displayed(player):
        return player.round_number == 1

class RoleDisplay(Page):
    timeout_seconds = 10
    def is_displayed(player):
        return player.round_number == 1

class RoundStartWait(Page):
    timeout_seconds = 10
    pass

class VoteForType2(page):
    form_model = 'player'
    form_fields = ['allow_type_2']
    def is_displayed(player):
        return player.is_type_1

class WaitForVoting(WaitPage):
    after_all_players_arrive = set_type2_permission

class VoteResultDisplay(Page):
    def vars_for_template(player:Player):
        return dict(type2 = player.type_2_allowed)

class WaitForJobs(WaitPage):
    after_all_players_arrive = set_jobs
    pass

class JobAllocation(Page):

    form_model = 'player'

    def get_form_fields(player):
        if player.type_2_allowed:
            return ['b1','b2','b3','b4','g1', 'g2', 'g3', 'g4']
        else:
            return ['b3','b4','g1', 'g2', 'g3', 'g4']

    def is_displayed(player):
        return player.is_assigner
    

class JobPage(Page):
    form_model = 'player'
    form_fields = ["answered"]

    def live_method(player , data):
        if data["type"] == "ans":
            if data["data"] == player.correct_ans:
                player.correct += 1
        

class AssignerWait(WaitPage):
    after_all_players_arrive = calculate_payoff
    pass

class PayoffInfo(Page):
    def vars_for_template(player):
        return dict(payoff = player.payoff)

class EndResult(Page):
    def vars_for_template(player):

    #def is_displayed(player):
     #   return player.round_number == 30
    

page_sequence = [WaitForPlayers, RoleDisplay, RoundStartWait, VoteForType2, WaitForVoting, JobAllocation, VoteResultDisplay, WaitForJobs, JobPage, AssignerWait, PayoffInfo, EndResult]
