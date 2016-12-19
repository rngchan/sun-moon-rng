#!/usr/bin/env python

from tinymt import TinyMT


# Clean input file line from excess characters
def parseInput(inp):
    res = inp
    badcharacters = [' ', '\n', '\r']
    for ch in badcharacters:
        res = "".join(res.split(ch))
    return res

if __name__ == "__main__":

    oldseed = None
    with open("seed.txt", 'r') as seedfile:
        seedfile = seedfile.readlines()
        oldseed = seedfile[0]
        seed = [parseInput(s) for s in seedfile[0].split(' ')]
        seed = [int(s, 16) for s in seed]
    tmt = TinyMT(seed)
    for i in range(124):
        tmt.nextState()
    with open("seed.txt", 'w') as seedfile:
        seedfile.write(oldseed)
        seedfile.write("Current Seed is:\n")
        state = tmt.getState()
        for i, s in enumerate(state[::-1]):
            seedfile.write("State {}: {}\n".format(3-i, hex(s)[2:]))
