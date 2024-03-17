class Foul:
    def __init__(self, env):
        self.env = env
        foul = """
                  (deftemplate foul
                      (slot hasFoul (allowed-symbols true false))
                  )
               """
        env.build(foul)

    def assert_fact(self, has_foul):
        foul_template = self.env.find_template('foul')
        foul_template.assert_fact(hasFoul=has_foul)
