class DecisionOfReferee:
    def __init__(self, env):
        self.env = env
        decision_of_referee = """
                                 (deftemplate decision_of_referee
                                     (slot hasDecisionOfReferee  
                                     (allowed-symbols goal_fixing goal_rejection red_card warning yellow_card))
                                 )
                              """
        env.build(decision_of_referee)

    def assert_fact(self, decision_of_referee):
        decision_of_referee_template = self.env.find_template('decision_of_referee')
        decision_of_referee_template.assert_fact(hasDecisionOfReferee=decision_of_referee)
