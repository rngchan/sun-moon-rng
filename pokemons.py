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


class Egg(Pokemon):

    def __init__(self, seeds, ivs, ability, nature, gender, pid, ball, rolls):
        super(Egg, self).__init__(ivs, ability, nature, gender)
        self.ball = ball
        self.seeds = seeds
        self.pid = pid
        self.rolls = rolls

    def __str__(self):
        result = "IV Spread: "
        for iv in self.ivs:
            result += "({}, {}) / ".format(iv[0], iv[1])
        result = result[:-3] + '\n'
        result += "Ability: {}\n".format(self.ability)
        result += "Nature: {}\n".format(self.nature)
        result += "Gender: {}\n".format(self.gender)
        result += "Ball Inherited: {}\n".format(self.ball)
        result += "PID: {}\n".format(hex(self.pid)[2:])
        result += "Seed to hatch: "
        for seed_step in self.seeds[0][::-1]:
            result += "{} ".format(hex(seed_step)[2:])
        result = result[:-1] + '\n'
        result += "Seed after hatching: "
        for seed_step in self.seeds[1][::-1]:
            result += "{} ".format(hex(seed_step)[2:])
        result = result[:-1] + '\n'
        return result


class Child(Pokemon):

    def __init__(self, ivsRange, ability, nature, gender, ball, hpower, shiny):
        super(Child, self).__init__(ivsRange, ability, nature, gender)
        self.ivsRange = ivsRange
        self.ball = ball
        self.hpower = hpower
        self.shiny = shiny

    def matches(self, egg):
        # Check for IVs withing range
        for i in range(6):
            eggIV = egg.ivs[i][1]
            childIVRange = self.ivsRange[i]
            if eggIV < childIVRange[0] or eggIV > childIVRange[1]:
                return False
        # Check for ability, nature, gender and ball
        if self.ability is not None and egg.ability != self.ability:
            return False
        if self.nature is not None and egg.nature != self.nature:
            return False
        if self.gender is not None and egg.gender != self.gender:
            return False
        if self.ball is not None and egg.ball != self.ball:
            return False
        # Add check for hidden power and shiny sometime
        return True
