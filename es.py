import clips
from entities.decision_of_referee import DecisionOfReferee
from entities.offside import Offside
from entities.game_density import GameDensity
from entities.refereeing_style import RefereeingStyle
from entities.var_tip import VarTip
from entities.offside_check_system import OffsideCheckSystem
from entities.foul import Foul


class Es:
    def __init__(self):
        self.env = clips.Environment()

        self.decision_of_referee_template = DecisionOfReferee(self.env)
        self.offside_template = Offside(self.env)
        self.game_density_template = GameDensity(self.env)
        self.refereeing_style_template = RefereeingStyle(self.env)
        self.var_tip_template = VarTip(self.env)
        self.offside_check_system_template = OffsideCheckSystem(self.env)
        self.foul_template = Foul(self.env)

    def assert_facts(self, form):
        self.offside_template.assert_fact(
            has_offside='true' if form.violation.choices[int(form.violation.data) - 1][1] == 'offside' else 'false')
        self.game_density_template.assert_fact(
            has_game_density=form.game_density.choices[int(form.game_density.data) - 1][1])
        self.refereeing_style_template.assert_fact(
            has_refereeing_style=form.refereeing_style.choices[int(form.refereeing_style.data) - 1][1])
        self.var_tip_template.assert_fact(
            has_var_tip=form.var_tip.choices[int(form.var_tip.data) - 1][1])
        self.offside_check_system_template.assert_fact(
            has_offside_system_decision=form.offside_check_system.choices[int(form.offside_check_system.data) - 1][1])
        self.foul_template.assert_fact(
            has_foul='true' if form.violation.choices[int(form.violation.data) - 1][1] == 'foul' else 'false')

    def get_result(self):
        self.rule_yellow_card()
        self.env.call('run')
        if self.env.agenda_changed:
            self.env.reset()
            return "yellow_card"

        self.rule_red_card()
        self.env.call('run')
        if self.env.agenda_changed:
            self.env.reset()
            return "red_card"

        self.rule_warning()
        self.env.call('run')
        if self.env.agenda_changed:
            self.env.reset()
            return "warning"

        self.rule_goal_fixing()
        self.env.call('run')
        if self.env.agenda_changed:
            self.env.reset()
            return "goal_fixing"

        self.rule_offside()
        self.env.call('run')
        if self.env.agenda_changed:
            self.env.reset()
            return "warning"


        for rule in self.env.rules():
            print(rule)
        self.env.reset()
        return False

    def rule_yellow_card(self):
        rule1 = """
                   (defrule rule1
                      (foul (hasFoul "true"))
                      (offside (hasOffside "false"))
                      (or (game_density (hasGameDensity "intensive"))
                          (game_density (hasGameDensity "variable")))
                      (offside_check_system (hasOffsideSystemDecision "false"))
                      (refereeing_style (hasRefereeingStyle "objective"))
                      (or (var_tip (hasVarTip "true"))
                          (var_tip (hasVarTip "false")))
                      =>
                      (assert (decision_of_referee (hasDecisionOfReferee "yellow_card")))
                   )
                """
        rule2 = """
                   (defrule rule2
                      (foul (hasFoul "true"))
                      (offside (hasOffside "false"))
                      (game_density (hasGameDensity "affiliated"))
                      (offside_check_system (hasOffsideSystemDecision "false"))
                      (refereeing_style (hasRefereeingStyle "rigorous"))
                      (or (var_tip (hasVarTip "true"))
                          (var_tip (hasVarTip "false")))
                      =>
                      (assert (decision_of_referee (hasDecisionOfReferee "yellow_card")))
                   )
                """
        rule3 = """
                   (defrule rule3
                      (foul (hasFoul "true"))
                      (offside (hasOffside "false"))
                      (game_density (hasGameDensity "variable"))
                      (offside_check_system (hasOffsideSystemDecision "false"))
                      (refereeing_style (hasRefereeingStyle "rigorous"))
                      (var_tip (hasVarTip "false"))
                      =>
                      (assert (decision_of_referee (hasDecisionOfReferee "yellow_card")))
                   )
                """

        self.env.build(rule1)
        self.env.build(rule2)
        self.env.build(rule3)

    def rule_red_card(self):
        rule4 = """
                   (defrule rule4
                      (foul (hasFoul "true"))
                      (offside (hasOffside "false"))
                      (or (game_density (hasGameDensity "intensive"))
                          (game_density (hasGameDensity "variable")))
                      (offside_check_system (hasOffsideSystemDecision "false"))
                      (refereeing_style (hasRefereeingStyle "rigorous"))
                      (var_tip (hasVarTip "true"))
                      =>
                      (assert (decision_of_referee (hasDecisionOfReferee "red_card")))
                   )
                """
        rule5 = """
                   (defrule rule5
                      (foul (hasFoul "true"))
                      (offside (hasOffside "false"))
                      (game_density (hasGameDensity "intensive"))
                      (offside_check_system (hasOffsideSystemDecision "false"))
                      (refereeing_style (hasRefereeingStyle "rigorous"))
                      (var_tip (hasVarTip "false"))
                      =>
                      (assert (decision_of_referee (hasDecisionOfReferee "red_card")))
                   )
                """
        self.env.build(rule4)
        self.env.build(rule5)

    def rule_warning(self):
        rule6 = """
                   (defrule rule6
                      (foul (hasFoul "true"))
                      (offside (hasOffside "false"))
                      (or (game_density (hasGameDensity "intensive"))
                          (game_density (hasGameDensity "affiliated"))
                          (game_density (hasGameDensity "variable")))
                      (offside_check_system (hasOffsideSystemDecision "false"))
                      (refereeing_style (hasRefereeingStyle "liberal"))
                      (var_tip (hasVarTip "false"))
                      =>
                      (assert (decision_of_referee (hasDecisionOfReferee "warning")))
                   )
                """
        rule7 = """
                   (defrule rule7
                      (foul (hasFoul "true"))
                      (offside (hasOffside "false"))
                      (game_density (hasGameDensity "affiliated"))
                      (offside_check_system (hasOffsideSystemDecision "false"))
                      (refereeing_style (hasRefereeingStyle "objective"))
                      (var_tip (hasVarTip "false"))
                      =>
                      (assert (decision_of_referee (hasDecisionOfReferee "warning")))
                   )
                """
        self.env.build(rule6)
        self.env.build(rule7)

    def rule_goal_fixing(self):
        rule8 = """
                   (defrule rule8
                      (foul (hasFoul "false"))
                      (offside (hasOffside "false"))
                      (offside_check_system (hasOffsideSystemDecision "false"))
                      (or (var_tip (hasVarTip "true"))
                          (var_tip (hasVarTip "false")))
                      =>
                      (assert (decision_of_referee (hasDecisionOfReferee "goal_fixing")))
                   )
                """
        self.env.build(rule8)

    def rule_offside(self):
        rule9 = """
                   (defrule rule9
                      (foul (hasFoul "false"))
                      (or (offside_check_system (hasOffsideSystemDecision "true"))
                          (offside_check_system (hasOffsideSystemDecision "false")))
                      (offside (hasOffside "true"))
                      (or (var_tip (hasVarTip "true"))
                          (var_tip (hasVarTip "false")))
                      =>
                      (assert (decision_of_referee (hasDecisionOfReferee "warning")))
                   )
                """
        self.env.build(rule9)
