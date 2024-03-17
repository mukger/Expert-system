class GameDensity:
    def __init__(self, env):
        self.env = env
        game_density = """
                          (deftemplate game_density
                              (slot hasGameDensity (allowed-symbols affiliated intensive variable))
                          )
                       """
        env.build(game_density)

    def assert_fact(self, has_game_density):
        game_density_template = self.env.find_template('game_density')
        game_density_template.assert_fact(hasGameDensity=has_game_density)
