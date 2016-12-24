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

    def __init__(self, seeds, ivs, ability, nature, gender, pid, ball, rolls,
                 esv, shiny, hpower):
        super(Egg, self).__init__(ivs, ability, nature, gender)
        self.ball = ball
        self.seeds = seeds
        self.pid = pid
        self.rolls = rolls
        self.esv = esv
        self.shiny = shiny
        self.hpower = hpower

    def __str__(self):
        result = "IV Spread: "
        for iv in self.ivs:
            result += "({}, {}) / ".format(iv[0], iv[1])
        result = result[:-3] + '\n'
        result += "Ability: {}\n".format(self.ability)
        result += "Nature: {}\n".format(self.nature)
        result += "Gender: {}\n".format(self.gender)
        result += "Ball Inherited: {}\n".format(self.ball)
        result += "Hidden Power Type: {}\n".format(self.hpower)
        result += "PID: {}\n".format(hex(self.pid)[2:])
        result += "ESV: {}\n".format(self.esv)
        result += "Shiny: {}\n".format("Yes if traded" if self.shiny == "P"
                                       else self.shiny)
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
        # Check for ability, nature, gender ball, hpower, shiny
        if self.ability is not None and egg.ability != self.ability:
            return False
        if self.nature is not None and egg.nature != self.nature:
            return False
        if self.gender is not None and egg.gender != self.gender:
            return False
        if self.ball is not None and egg.ball != self.ball:
            return False
        if self.hpower is not None and egg.hpower != self.hpower:
            return False
        if self.shiny and egg.shiny not in ["Yes", "P"]:
            return False
        elif self.shiny is not None and not self.shiny and egg.shiny != "No":
            return False
        return True
