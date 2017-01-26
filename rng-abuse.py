#!/usr/bin/env python

from ast import literal_eval as l_eval
from tinymt import TinyMT
from pokemons import Parent, Child, Egg

# Natures in game order
natures = ["HARDY", "LONELY", "BRAVE", "ADAMANT", "NAUGHTY", "BOLD", "DOCILE",
           "RELAXED", "IMPISH", "LAX", "TIMID", "HASTY", "SERIOUS", "JOLLY",
           "NAIVE", "MODEST", "MILD", "QUIET", "BASHFUL", "RASH", "CALM",
           "GENTLE", "SASSY", "CAREFUL", "QUIRKY"]

# Gender ratio rolls
ratios = {"GENDERLESS": 255, "FEMALE": 254, "MALE": 0, "1-1": 126,
          "1-3": 189, "3-1": 63, "1-7": 220, "7-1": 32}

# Hidden power types
types = ["FIGHTING", "FLYING", "POISON", "GROUND", "ROCK", "BUG", "GHOST",
         "STEEL", "FIRE", "WATER", "GRASS", "ELECTRIC", "PSYCHIC", "ICE",
         "DRAGON", "DARK"]


# Clean input file line from excess characters
def parseInput(inp):
    res = inp
    badcharacters = [' ', '\n', '\r']
    for ch in badcharacters:
        res = "".join(res.split(ch))
    return res


# Checks whether a PID is shiny based on TSV
def get_esv(pid):
    pid_high = (pid >> 16)
    pid_low = (pid & 0xFFFF)
    return ((pid_high ^ pid_low) >> 4)


# Determine hidden power type
def get_hpower(ivs):
    bits = [str(iv[1] % 2) for iv in ivs][::-1]
    # Swap speed with spatk and spdef
    bits[0], bits[1], bits[2] = bits[1], bits[2], bits[0]
    hpower = int(int("".join(bits), 2) * 15 / 63)
    return types[hpower]


# Read config file parameters
def readConfigFile():
    with open("config.txt") as cfgfile:
        config = cfgfile.readlines()
        params = {}
        hasDitto = False

        # Read parents parameters
        params["parents"] = {}
        for gender, skip in [("Male", 3), ("Female", 17)]:
            ivs = []
            # Read IVs as integers 0-31
            for i in range(6):
                try:
                    iv = int(config[skip+i].split(':')[1])
                except ValueError:
                    return None, "Invalid IVs for parent"
                if iv < 0 or iv > 31:
                    return None, "Parent IVs out of 0-31 range"
                ivs.append(iv)
            # Only accepted items are d.knot and everstone
            # One day there will be support for power items
            item = parseInput(config[skip+6].split(':')[1]).upper()
            if item not in ["NONE", "DESTINYKNOT", "EVERSTONE"]:
                return None, "Invalid item for parent"
            # Ability slot should be one of 1, 2, HA
            ability = parseInput(config[skip+7].split(':')[1]).upper()
            if ability not in ["1", "2", "HA"]:
                return None, "Invalid ability for parent"
            # Nature should be one of the valid natures
            nature = parseInput(config[skip+8].split(':')[1]).upper()
            if nature not in natures:
                return None, "Invalid nature for parent"
            # Whether or not this parent is a ditto - boolean value
            ditto = parseInput(config[skip+9].split(':')[1]).upper()
            if ditto not in ["Y", "N"]:
                return None, "Invalid Ditto parameter in parent"
            # Check if breeding two dittos
            if ditto == "Y" and hasDitto:
                return None, "Cannot breed 2 Dittos"
            if ditto == "Y":
                hasDitto = True
            ditto = True if ditto == "Y" else False
            # Store parent info
            params["parents"][gender] = Parent(ivs, item, ability, nature,
                                               gender, ditto)

        # Read desired child traits parameters
        skip = 31
        ivs = []
        # Rad IVs as range of integers 0-31
        for i in range(6):
            try:
                iv_range = l_eval(parseInput(config[skip+i].split(':')[1]))
            except Exception:
                return None, "Invalid IV range for child"
            if type(iv_range) != list or len(iv_range) != 2:
                return None, "Invalid IV range format for child"
            for iv in iv_range:
                if iv < 0 or iv > 31:
                    return None, "Child IVs out of 0-31 range"
            ivs.append(iv_range)
        # Ability slot should be one of Anything, 1, 2, HA
        ability = parseInput(config[skip+6].split(':')[1]).upper()
        if ability not in ["ANYTHING", "1", "2", "HA"]:
            return None, "Invalid ability for child"
        ability = None if ability == "ANYTHING" else ability
        # Nature should be one of the valid natures or "Anything"
        nature = parseInput(config[skip+7].split(':')[1]).upper()
        if nature not in ["ANYTHING"]+natures:
            return None, "Invalid nature for child"
        nature = None if nature == "ANYTHING" else nature
        # Gender should be one of Anything, M, F, Genderless
        gender = parseInput(config[skip+8].split(':')[1]).upper()
        if gender not in ["ANYTHING", "M", "F", "GENDERLESS"]:
            return None, "Invalid gender for child"
        # Ball should be one of Anything, M, F
        gender = None if gender == "ANYTHING" else gender
        ball = parseInput(config[skip+9].split(':')[1]).upper()
        if ball not in ["ANYTHING", "M", "F"]:
            return None, "Invalid ball for child"
        ball = None if ball == "ANYTHING" else ball
        # Hidden power should be a valid type
        hpower = parseInput(config[skip+10].split(':')[1]).upper()
        if hpower not in ["ANYTHING"]+types:
            return None, "Invalid hidden power type"
        hpower = None if hpower == "ANYTHING" else hpower
        # Shiny should be one of Anything, Y, N
        shiny = parseInput(config[skip+11].split(':')[1]).upper()
        if shiny not in ["ANYTHING", "Y", "N"]:
            return None, "Invalid shiny parameter for child"
        shiny = True if shiny == "Y" else False if shiny == "N" else None
        # Store child info
        params["child"] = Child(ivs, ability, nature, gender, ball, hpower,
                                shiny)

        skip = 47
        # Read RNG seed info
        params["seed"] = []
        for i in range(4):
            try:
                status = int(config[skip+i].split(':')[1], 16)
            except ValueError:
                return None, "Invalid seed status"
            params["seed"].append(status)
        # Read TSV as integer between 0 and 4096
        try:
            tsv = int(config[skip+4].split(':')[1])
        except ValueError:
            return None, "Invalid TSV"
        if tsv < 0 or tsv > 4096:
            return None, "TSV must be between 0 and 4096"
        params["tsv"] = tsv
        # Read ESV parameter as a list of ESV values
        try:
            esvs = l_eval(parseInput(config[skip+5].split(':')[1]))
        except Exception:
            return None, "Invalid ESV, are you usuing the right format?"
        params["esvs"] = []
        for esv in esvs:
            try:
                esv = int(esv)
            except ValueError:
                return None, "Invalid ESV value, not an integer"
            if esv < 0 or esv > 4096:
                return None, "Invalid ESV value, must e between 0 and 4096"
            params["esvs"].append(esv)

        skip = 57
        # Read gender ratio info
        ratio = parseInput(config[skip].split(':')[1]).upper()
        if ratio not in ratios:
            return None, "Invalid ratio for child"
        params["ratio"] = ratios[ratio]
        # Read masuda method info
        mmethod = parseInput(config[skip+1].split(':')[1]).upper()
        if mmethod not in ["Y", "N"]:
            return None, "Invalid Masuda Method parameter"
        params["masuda"] = True if mmethod == "Y" else False
        # Read shiny charm info
        charm = parseInput(config[skip+2].split(':')[1]).upper()
        if charm not in ["Y", "N"]:
            return None, "Invalid Shiny Charm parameter"
        params["charm"] = True if charm == "Y" else False
        # Read ballcheck info / same species info
        ballcheck = parseInput(config[skip+3].split(':')[1]).upper()
        if ballcheck not in ["Y", "N"]:
            return None, "Invalid same species parameter"
        params["ballcheck"] = True if ballcheck == "Y" else False
        # Read number of desired results
        try:
            params["nresults"] = int(config[skip+4].split(':')[1])
        except ValueError:
            return None, "Invalid number of results to be shown"

        return params, None


def makeEgg(tinymt, parentA, parentB, ratio, charm, masuda, ballcheck, tsv,
            esvs):
    seed_before = tinymt.getState()
    rolls = 0  # Keep track of rolls number

    # Roll for gender if not fixed gender
    if ratio == 255:
        gender = "GENDERLESS"
    elif ratio == 254:
        gender = "F"
    elif not ratio:
        gender = "M"
    else:
        gender = "F" if tinymt.nextStateAsInt(252)+1 < ratio else "M"
        rolls += 1

    # Roll for nature, then check for everstone, roll if necessary
    nature = natures[tinymt.nextStateAsInt(25)]
    rolls += 1
    if parentA.item == "EVERSTONE" and parentB.item == "EVERSTONE":
        nature = parentB.nature if tinymt.nextStateAsInt(2) else parentA.nature
        rolls += 1
    elif parentA.item == "EVERSTONE":
        nature = parentA.nature
    elif parentB.item == "EVERSTONE":
        nature = parentB.nature

    # Roll for ability, assigning result based on non-ditto / female parent
    ab_parent = parentA if parentB.ditto else parentB
    ab_roll = tinymt.nextStateAsInt(100)
    rolls += 1
    if ab_parent.ability == "1":
        ability = "1" if ab_roll < 80 else "2"
    elif ab_parent.ability == "2":
        ability = "1" if ab_roll < 20 else "2"
    else:
        ability = "1" if ab_roll < 20 else "2" if ab_roll < 40 else "HA"

    # Check for destiny knot
    dknot = parentA.item == "DESTINYKNOT" or parentB.item == "DESTINYKNOT"
    ivs_to_inherit = 5 if dknot else 3
    inherit_ivs = [None]*6
    inherited = 0
    # IV inheritance done just like the game does it
    while (inherited < ivs_to_inherit):
        # Roll random stat 0-5
        stat = tinymt.nextStateAsInt(6)
        rolls += 1
        # Check if stat was already inherited, skip if so
        if inherit_ivs[stat] is None:
            # Roll which parent passes down this stat
            inherit_ivs[stat] = "B" if tinymt.nextStateAsInt(2) else "A"
            rolls += 1
            inherited += 1
    # Roll random IVs for child
    natural_ivs = [tinymt.nextStateAsInt(32) for i in range(6)]
    rolls += 6
    ivs = []
    # Child gets inherited IVs / random IVs
    for i in range(6):
        if inherit_ivs[i] is None:
            ivs.append(("R", natural_ivs[i]))
        elif inherit_ivs[i] == "A":
            ivs.append((parentA.gender[0], parentA.ivs[i]))
        elif inherit_ivs[i] == "B":
            ivs.append((parentB.gender[0], parentB.ivs[i]))
    hpower = get_hpower(ivs)

    # Roll random PID
    pid = tinymt.nextStateAsPID()
    esv = "No way to know - please use either Masuda method or Shiny Charm"
    shiny = "No way to know - please use either Masuda method or Shiny Charm"
    rolls += 1
    rerolls = 0
    rerolls += 2 if charm else 0
    rerolls += 6 if masuda else 0
    # Reroll PID if shiny charm / MM / both
    for i in range(rerolls):
        pid = tinymt.nextStateAsPID()
        rolls += 1
        esv = get_esv(pid)
        shiny = "Yes" if esv == tsv else "P" if esv in esvs else "No"
        if shiny == "Yes":
            break

    # Roll for ball check if necessary
    genderA, genderB = parentA.gender[0], parentB.gender[0]
    if parentB.ditto:
        ball = genderA
    elif parentA.ditto:
        ball = genderB
    elif not ballcheck:
        ball = "F"
    else:
        ball = genderB if tinymt.nextStateAsInt(100)+1 <= 50 else genderA
        rolls += 1

    # Extra mythical rolls that do random shit unrelated to eggs
    rolls += 2
    tinymt.nextState()
    tinymt.nextState()
    seed_after = tinymt.getState()
    seeds = [seed_before, seed_after]

    # Build egg and return
    return Egg(seeds, ivs, ability, nature, gender, pid, ball, rolls, esv,
               shiny, hpower)


def main():
    # Read parameters, check for errors
    try:
        params, msg = readConfigFile()
    except Exception:
        msg = "Unknown error occured. Are you using the right format?"
    if msg is not None:
        with open("results.txt", 'w') as res:
            res.write("There was an error processing your config file:\n")
            res.write("ERROR: {}\n".format(msg))
        return

    results = []
    rolls = []
    tries = 0
    tmt = TinyMT(params["seed"])
    parentA = params["parents"]["Male"]
    parentB = params["parents"]["Female"]

    # Repeat until enough results are found, timeout at 10000
    while not results or len(results) < params["nresults"] and tries < 10000:
        tmtState = tmt.getState()
        egg = makeEgg(tmt, parentA, parentB, params["ratio"], params["charm"],
                      params["masuda"], params["ballcheck"], params["tsv"],
                      params["esvs"])
        rolls.append(egg.rolls)
        if params["child"].matches(egg):
            results.append((tries, egg))
        tmt.setState(tmtState)
        tmt.nextState()
        tries += 1
        if not tries % 20000:
            print "WARNING: Script is taking too long to finish."
            print "         {} seeds were already searched.".format(tries)
            print "         Press CTRL+C to terminate the script.\n"

    print("Found {} results, writing them to results.txt".format(len(results)))
    with open("results.txt", 'w') as res:
        for frame, egg in results:
            # Print egg info
            res.write(str(egg))
            # Build actions path and store it in file
            path = "Sequence of actions to hatch:\n"
            path += "(This one might not work, still working the details)\n"
            f = a = r = 0
            while f+rolls[f] <= frame:
                f += rolls[f]
                a += 1
            while f < frame:
                f += 1
                r += 1
            if not r:
                if a+1 == 1:
                    path += ">Accept egg\n"
                else:
                    path += ">Accept {} eggs\n".format(a+1)
            else:
                if a == 1:
                    path += ">Accept egg\n"
                elif a:
                    path += ">Accept {} eggs\n".format(a)
                if r == 1:
                    path += ">Reject egg\n"
                else:
                    path += ">Reject {} eggs\n".format(r)
                path += ">Accept egg\n"
            path += "(This one will work for sure, but is longer)\n"
            if frame == 1:
                path += ">Reject egg\n"
            elif frame:
                path += ">Reject {} eggs\n".format(frame)
            path += ">Accept egg\n"
            res.write(path+'\n')

if __name__ == "__main__":

    main()
    print("DONE!")
