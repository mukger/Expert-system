class OffsideCheckSystem:
    def __init__(self, env):
        self.env = env
        offside_check_system = """
                                  (deftemplate offside_check_system
                                   (slot hasOffsideSystemDecision (allowed-symbols true false))
                                  )
                               """
        env.build(offside_check_system)

    def assert_fact(self, has_offside_system_decision):
        offside_check_system_template = self.env.find_template('offside_check_system')
        offside_check_system_template.assert_fact(hasOffsideSystemDecision=has_offside_system_decision)
