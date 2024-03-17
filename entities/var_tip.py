class VarTip:
    def __init__(self, env):
        self.env = env
        var_tip = """
                     (deftemplate var_tip
                         (slot hasVarTip (allowed-symbols true false))
                     )
                  """
        env.build(var_tip)

    def assert_fact(self, has_var_tip):
        var_tip_template = self.env.find_template('var_tip')
        var_tip_template.assert_fact(hasVarTip=has_var_tip)
