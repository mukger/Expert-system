class RefereeingStyle:
    def __init__(self, env):
        self.env = env
        refereeing_style = """
                              (deftemplate refereeing_style
                                 (slot hasRefereeingStyle (allowed-symbols liberal objective rigorous))
                              )
                           """
        env.build(refereeing_style)

    def assert_fact(self, has_refereeing_style):
        refereeing_style_template = self.env.find_template('refereeing_style')
        refereeing_style_template.assert_fact(hasRefereeingStyle=has_refereeing_style)
