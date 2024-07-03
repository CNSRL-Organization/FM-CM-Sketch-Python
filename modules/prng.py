import math
import random
import numpy as np

PI = 3.141592653589793
MOD = (1 << 31) - 1
HL = 31

def hash31(a, b, x):
    result = (a * x + b)
    result = ((result >> HL) + result) & MOD
    return result

def fourwise(a, b, c, d, x):
    result = hash31(hash31(hash31(x, a, b), x, c), x, d)
    return result

class PRNG:
    IA = 16807
    IM = 2147483647
    AM = 1.0 / IM
    IQ = 127773
    IR = 2836
    NTAB = 32
    NDIV = 1 + (IM - 1) // NTAB
    EPS = 1.2e-7
    RNMX = 1.0 - EPS
    R1 = 5
    R2 = 3
    JJ = 10
    KK = 17

    def __init__(self, seed, usenric):
        self.iv = [0] * PRNG.NTAB
        self.floatidum = -seed if seed > 0 else seed
        self.intidum = -seed if seed > 0 else seed
        self.iset = 0
        self.gset = 0
        self.iy = 0
        self.usenric = usenric
        self.randbuffer = [0] * PRNG.KK
        if usenric == 2:
            self.RanrotAInit(seed)
        elif usenric == 3:
            random.seed(seed)
        self.prng_float()
        self.prng_int()

    def ran1(self):
        if self.floatidum <= 0 or not self.iy:
            if -(self.floatidum) < 1:
                self.floatidum = 1
            else:
                self.floatidum = -(self.floatidum)
            for j in range(PRNG.NTAB + 7, -1, -1):
                k = self.floatidum // PRNG.IQ
                self.floatidum = PRNG.IA * (self.floatidum - k * PRNG.IQ) - PRNG.IR * k
                if self.floatidum < 0:
                    self.floatidum += PRNG.IM
                if j < PRNG.NTAB:
                    self.iv[j] = self.floatidum
            self.iy = self.iv[0]
        k = self.floatidum // PRNG.IQ
        self.floatidum = PRNG.IA * (self.floatidum - k * PRNG.IQ) - PRNG.IR * k
        if self.floatidum < 0:
            self.floatidum += PRNG.IM
        j = self.iy // PRNG.NDIV
        self.iy = self.iv[j]
        self.iv[j] = self.floatidum
        temp = PRNG.AM * self.iy
        return PRNG.RNMX if temp > PRNG.RNMX else temp

    def ran2(self):
        if self.intidum <= 0 or not self.iy:
            if -(self.intidum) < 1:
                self.intidum = 1
            else:
                self.intidum = -(self.intidum)
            for j in range(PRNG.NTAB + 7, -1, -1):
                k = self.intidum // PRNG.IQ
                self.intidum = PRNG.IA * (self.intidum - k * PRNG.IQ) - PRNG.IR * k
                if self.intidum < 0:
                    self.intidum += PRNG.IM
                if j < PRNG.NTAB:
                    self.iv[j] = self.intidum
            self.iy = self.iv[0]
        k = self.intidum // PRNG.IQ
        self.intidum = PRNG.IA * (self.intidum - k * PRNG.IQ) - PRNG.IR * k
        if self.intidum < 0:
            self.intidum += PRNG.IM
        j = self.iy // PRNG.NDIV
        self.iy = self.iv[j]
        self.iv[j] = self.intidum
        return self.iy 

    def rotl(self, x, r, w = "none"):
        result = ((x << r) | (x >> (64 - r))) & 0xFFFFFFFFFFFFFFFF  # Assuming 32-bit unsigned long in C context
        #print(f"Left rotated by {x} bits: {result}",w)
        return result
        

    def ran3(self):
        x = self.randbuffer[self.r_p1] = self.rotl(self.randbuffer[self.r_p2], PRNG.R1,'ran3-1') + self.rotl(self.randbuffer[self.r_p1], PRNG.R2,'ran3-2') & 0xFFFFFFFFFFFFFFFF  # Assuming 32-bit unsigned long in C contex
        # if self.r_p1 <= 0:
        #     self.r_p1 = PRNG.KK - 1
        # else:
        #     self.r_p1 -= 1
        # if self.r_p2 <= 0:
        #     self.r_p2 = PRNG.KK - 1
        # else:
        #     self.r_p2 -= 1
        self.r_p1 -= 1
        if self.r_p1 < 0:
            self.r_p1 = PRNG.KK - 1
        
        self.r_p2 -= 1
        if self.r_p2 < 0:
            self.r_p2 = PRNG.KK - 1
        x = x & 0xFFFFFFFF
        if x >= 0x80000000:
            x -= 0x100000000
            
        return x

    def ran4(self):
        return self.ran3() * self.scale

    def RanrotAInit(self, seed):
        seed = seed & 0xFFFFFFFFFFFFFFFF
        for i in range(PRNG.KK):
            self.randbuffer[i] = seed
            seed = self.rotl(seed, 5) + 97 
        self.r_p1 = 0
        self.r_p2 = PRNG.JJ
        for i in range(300):
            self.ran3()
        self.scale = math.ldexp(1, -8 * 4)

    def prng_int(self):
        if self.usenric == 1:
            return self.ran2()
        elif self.usenric == 2:
            return self.ran3()
        elif self.usenric == 3:
            return random.randint(0, PRNG.IM)

    def prng_float(self):
        if self.usenric == 1:
            return self.ran1()
        elif self.usenric == 2:
            return self.ran4()
        elif self.usenric == 3:
            return random.random()

    def prng_normal(self):
        if self.iset == 0:
            while True:
                v1 = 2.0 * self.prng_float() - 1.0
                v2 = 2.0 * self.prng_float() - 1.0
                rsq = v1 * v1 + v2 * v2
                if rsq < 1.0 and rsq != 0.0:
                    break
            fac = math.sqrt(-2.0 * math.log(rsq) / rsq)
            self.gset = v1 * fac
            self.iset = 1
            return v2 * fac
        else:
            self.iset = 0
            return self.gset

    def prng_stabledbn(self, alpha):
        theta = PI * (self.prng_float() - 0.5)
        W = -math.log(self.prng_float())
        left = (math.sin(alpha * theta) / pow(math.cos(theta), 1.0 / alpha))
        right = pow(math.cos(theta * (1.0 - alpha)) / W, (1.0 - alpha) / alpha)
        return left * right

    def prng_cauchy(self):
        return math.tan(PI * (self.prng_float() - 0.5))

    def prng_altstab(self, p):
        u = self.prng_float()
        v = self.prng_float()
        result = pow(u, p)
        return -result if v < 0.5 else result

    def prng_stable(self, alpha):
        if alpha == 2.0:
            return self.prng_normal()
        elif alpha == 1.0:
            return self.prng_cauchy()
        elif alpha < 0.01:
            return self.prng_altstab(-50.0)
        else:
            return self.prng_stabledbn(alpha)