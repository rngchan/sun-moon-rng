class Pokemon(object):

    def __init__(self, ivs, ability, nature, gender):
        self.ivs = ivs
        self.ability = ability
        self.nature = nature
        self.gender = gender


class Parent(Pokemon):

    def __init__(self, ivs, item, ability, nature, gender, ditto):
        super(Parent, self).__init__(ivs, ability, nature, gender)
        self.item = item
        self.ditto = ditto


class Child(Pokemon):

    def __init__(self, ivsRange, ability, nature, gender, ball, hpower, shiny):
        super(Child, self).__init__(ivsRange, ability, nature, gender)
        self.ivsRange = ivsRange
        self.ball = ball
        self.hpower = hpower
        self.shiny = shiny


class Egg(Pokemon):

    def __init__(self, seed, ivs, ability, nature, gender, pid, ball, rolls):
        super(Egg, self).__init__(ivs, ability, nature, gender)
        self.ball = ball
        self.seed = seed
        self.pid = pid
        self.rolls = rolls
