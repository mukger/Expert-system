class Offside:
    def __init__(self, env):
        self.env = env
        offside = """
                     (deftemplate offside
                         (slot hasOffside (allowed-symbols true false))
                     )
                  """
        env.build(offside)

    def assert_fact(self, has_offside):
        offside_template = self.env.find_template('offside')
        offside_template.assert_fact(hasOffside=has_offside)
