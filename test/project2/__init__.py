from otree.api import *
from random import choice , randint, sample

doc = """ """

class C(BaseConstants):
    NAME_IN_URL = ''
    PLAYERS_PER_GROUP = 9
    NUM_ROUNDS = 30

    roles = ["g1", "g2", "g3", "g4", "b11", "b12", "b21", "b22"]

    s_roles = sample(["a"]+["g1", "g2", "g3", "g4", "b11", "b12", "b21", "b22"] , 9)

    Player0_ROLE = s_roles[0]
    Player1_ROLE = s_roles[1]
    Player2_ROLE = s_roles[2]
    Player3_ROLE = s_roles[3]
    Player4_ROLE = s_roles[4]
    Player5_ROLE = s_roles[5]
    Player6_ROLE = s_roles[6]
    Player7_ROLE = s_roles[7]
    Player8_ROLE = s_roles[8]

    JOB_A_SOLVER_MUL = 0.5
    JOB_B_SOLVER_MUL = 0.25
    JOB_A_ASSIGNER_MUL = 0.8 - JOB_A_SOLVER_MUL
    JOB_B_ASSIGNER_MUL = 0.5 - JOB_B_SOLVER_MUL

    TYPE_2_JOB_A_TASK_COUNT_PER_ROUND = 2
    USE_POINTS = True

    payoff = cu(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
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

    b11 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    b12 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    b21 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    b22 = models.BooleanField(
        choices=[[True, 'Job A'], [False, 'Job B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    allow_type_2 = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    allowed = models.BooleanField(initial=True)
    job_A = models.BooleanField(initial=True)
    num1 = models.IntegerField(initial=0)
    num2 = models.IntegerField(initial=0)
    job_count = models.IntegerField(initial = 0)

    lang_eng = models.BooleanField(initial=True)

class instructions(Page):
    def vars_for_template(player):
        return dict(language = player.lang_eng)
    def is_displayed(player):
        return player.round_number == 1

class instructions_test(Page):
    def vars_for_template(player):
        return dict(language = player.lang_eng)
    def is_displayed(player):
        return player.round_number == 1


class Introduction(Page):
    def vars_for_template(player):
        sum1 = sum(p.payoff for p in player.in_all_rounds())
        return dict(role=player.role, points = sum1, round_number= player.round_number)

class VoteForType2(Page):
    form_model = 'player'
    form_fields = ['allow_type_2']

    def is_displayed(player):
        return (not player.role in ["a", "b21", "b22"])

class VotingWait(WaitPage):
    title_text = "Voting for Type 2 ongoing"
    body_text = "Plese wait for all Type-1 solvers to finish their voting."
    def after_all_players_arrive(group):
        vote_results = []
        for a in C.roles[:-2]:
            vote_results.append(group.get_player_by_role(a).allow_type_2)
        random_vote = choice(vote_results)
        for player in [ group.get_player_by_role(a) for a in ["b21", "b22","a"] ] :
            player.allowed = random_vote

class JobAssign(Page):
    form_model = 'player'
    def get_form_fields(player):
        if player.allowed:
            return sample(["g1", "g2", "g3", "g4", "b11", "b12", "b21", "b22"], 8)
        else:
            return sample(["g1", "g2", "g3", "g4", "b11", "b12"], 6)

    def is_displayed(player):
        return player.role == "a"
    
    def vars_for_template(player):
        return dict(fields = sample(["g1", "g2", "g3", "g4", "b11", "b12", "b21", "b22"], 8) if player.allowed else sample(["g1", "g2", "g3", "g4", "b11", "b12"], 6))

class WaitJobAssign(WaitPage):
    title_text = "Job assign ongoing"
    body_text = "Plese wait for Assigner to assign jobs."
    def after_all_players_arrive(group):
        assigner = group.get_player_by_role("a")
        array = [assigner.g1, assigner.g2, assigner.g3, assigner.g4, assigner.b11, assigner.b12, assigner.field_maybe_none('b21'), assigner.field_maybe_none('b22')]
        i = 0
        p = None
        while i < 8:
            p = group.get_player_by_role(C.roles[i])
            p.job_A = array[i] if array[i] != None else False
            p.num1 = randint(1,10)
            p.num2 = randint(1,10)
            i+=1

class JobPage(Page):
    timeout_seconds = 30

    def vars_for_template(player):
        return dict(num1=player.num1, num2= player.num2, job = player.job_A, role=player.role)

    def is_displayed(player):
        return (not (player.role == "a")) and player.allowed
    
    def live_method(player, data):
        if data["type"] == 'ans':
            if data['data']["ans"] == None:
                pass
            elif int(data['data']["ans"]) == player.num1 * player.num2:
                player.job_count+=1
                player.num1 = randint(1,10)
                player.num2 = randint(1,10)
                return {player.id_in_group:{"type":"reload", "data" : {"num1": player.num1, "num2": player.num2}}}
        

class WaitJob(WaitPage):
    title_text = "Jobs ongoing"
    body_text = "Plese wait for all Solvers to finish their Jobs."
    def after_all_players_arrive(group):
        assigner = None
        job_A_count = 0
        job_B_count = 0
        for player in group.get_players():
            if player.role == "a":
                assigner = player
            elif player.job_A:
                if player.role in ["b21", "b22"]:
                    player.payoff = C.JOB_A_SOLVER_MUL * player.job_count//2 * C.payoff
                    job_A_count+=player.job_count
                else:
                    player.payoff = C.JOB_A_SOLVER_MUL * player.job_count * C.payoff
                    job_A_count+=player.job_count
            else:
                player.payoff = C.JOB_B_SOLVER_MUL * player.job_count * C.payoff
                job_B_count+=player.job_count

        assigner.payoff = (C.JOB_A_ASSIGNER_MUL * job_A_count + C.JOB_B_ASSIGNER_MUL*job_B_count) * C.payoff

class Results(Page):
    def vars_for_template(player):
        return dict(points = player.payoff, job = player.job_A, allowed = player.allowed, role = player.role)

class FinalResults(Page):
    def vars_for_template(player):
        sum1 = sum(p.payoff for p in player.in_all_rounds())
        return dict(points = sum)
    def is_displayed(player):
        return player.round_number == 30

page_sequence = [instructions,Introduction,VoteForType2,VotingWait, JobAssign, WaitJobAssign, JobPage, WaitJob,Results,FinalResults]
        