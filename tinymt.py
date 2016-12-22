class TinyMT(object):

    tmt_constant = 0x7FFFFFFF
    mat1 = 0x8F7011EE
    mat2 = 0xFC78ff1F
    tmat = 0x3793FDFF

    def __init__(self, i_state):
        self.state = i_state[::-1]  # LSBits first

    def getState(self):
        return self.state[:]

    def setState(self, state):
        self.state = state

    def getStateAsHex(self):
        # Return current state as a single hex string
        res = "0x"
        for s in self.state[::-1]:
            status = hex(s)[2:]
            res += "0"*(8 - len(status)) + status
        return res

    def nextState(self):
        # Do a TinyMT roll to update state
        # Mask result to 32 bits after every shift left, force overflow
        x = (self.state[0] & self.tmt_constant) ^ self.state[1] ^ self.state[2]
        y = self.state[3]
        x ^= (x << 1) & 0xFFFFFFFF
        y ^= (y >> 1) ^ x
        self.state[0] = self.state[1]
        self.state[1] = self.state[2]
        self.state[2] = x ^ ((y << 10) & 0xFFFFFFFF)
        self.state[3] = y
        if (y & 0x1):
            self.state[1] ^= self.mat1
            self.state[2] ^= self.mat2

    def nextStateAsPID(self):
        # Return next state as a PID (32 bit integer)
        self.nextState()
        tmp = self.state[0] + (self.state[2] >> 8)
        return (tmp ^ self.state[3] ^ -(tmp & 0x1) & self.tmat)

    def nextStateAsInt(self, limit):
        # Return next state as an integer 0-limit
        return self.nextStateAsPID() % limit
