#https://github.com/zcash-hackworks/zcash-test-vectors

#!/usr/bin/env python3
from sapling_utils import i2lebsp, leos2ip, i2leosp


import pdb

'''
b = 256
q_j = 2**255 - 19
r_j = 2**252 + 27742317777372353535851937790883648493
'''
#qm1d2 = 26217937587563095239723870254092982918845276250263818911301829349969290592256
#assert (q_j - 1) // 2 == qm1d2


#
# Field arithmetic
#

class FieldElement(object):
    def __init__(self, t, s, modulus, strict=False):
        if strict and not (0 <= s and s < modulus):
            raise ValueError
        self.t = t
        self.s = s % modulus
        self.m = modulus

    def __add__(self, a):
        return self.t(self.s + a.s)

    def __sub__(self, a):
        return self.t(self.s - a.s)

    def __mul__(self, a):
        return self.t(self.s * a.s)

    def __truediv__(self, a):
        assert a.s != 0
        return self * a.inv()

    def exp(self, e):
        e = format(e, '0256b')
        ret = self.t(1)
        for c in e:
            ret = ret * ret
            if int(c):
                ret = ret * self
        return ret

    def inv(self):

        return self.exp(self.m - 2)

    def bits(self, l):
        return i2lebsp(l, self.s)

    def __bytes__(self):
        return i2leosp(256, self.s)

    def __eq__(self, a):
        return self.s == a.s



class Fq(FieldElement):
    @staticmethod
    def from_bytes(buf):
        return Fq(leos2ip(buf), strict=True)

    def __init__(self, s, strict=False):
        FieldElement.__init__(self, Fq, s, q_j, strict=strict)

    def __str__(self):
        return 'Fq(%s)' % self.s

    def __int__(self):
        return(self.s)

    def sqrt(self):
        # Tonelli-Shank's algorithm for q mod 16 = 1
        # https://eprint.iacr.org/2012/685.pdf (page 12, algorithm 5)

        a = self.exp(qm1d2)
        if a == self.ONE:
            c = Fq(10238227357739495823651030575849232062558860180284477541189508159991286009131)
            # 21888242871839275222246405745257275088548364400416034343698204186575808495617 // 8589934591
            # = 2548126838447922149288273404183046483985545449471285076948056144584

            r = self.exp(2548126838447922149288273404183046483985545449471285076948056144584)

            # 21888242871839275222246405745257275088548364400416034343698204186575808495617 // 4294967296
            # = 5096253676302562286669017222071363378443840053029366383258766538131
            t = self.exp(5096253676302562286669017222071363378443840053029366383258766538131)
            # math.log2(4294967296)
            # 32.0
            m = 32

            # 7: while b != 1 do
            while t != self.ONE:
                # 8: Find least integer k >= 0 such that b^(2^k) == 1
                i = 1
                t2i = t * t
                while t2i != self.ONE:
                    t2i = t2i * t2i
                    i += 1
                assert i < m

                # 9:
                # w <- z^(2^(v-k-1))
                for _ in range(0, m - i - 1):
                    c = c * c
                # b <- bz
                r = r * c
                # z <- w^2
                c = c * c
                # x <- xw
                t = t * c
                # v <- k
                m = i
            assert r * r == self
            return r
        elif a == self.MINUS_ONE:
            print("return none")
            return None
        
        #return self.ZERO


class Fr(FieldElement):
    def __init__(self, s, strict=False):
        FieldElement.__init__(self, Fr, s, r_j, strict=strict)
    def __str__(self):
        return 'Fr(%s)' % self.s



q_j = 21888242871839275222246405745257275088548364400416034343698204186575808495617 
r_j = 2736030358979909402780800718157159386076813972158567259200215660948447373041


qm1d2 = (21888242871839275222246405745257275088548364400416034343698204186575808495617 - 1)//2

JUBJUB_A = Fq(168700)
JUBJUB_D = Fq(168696)
JUBJUB_COFACTOR = Fr(8)


# remove this
#JUBJUB_A = Fq(-1)
#JUBJUB_D = Fq(-121665) / Fq(121666)
#JUBJUB_COFACTOR = Fr(8)



Fq.ZERO = Fq(0)
Fq.ONE = Fq(1)
Fq.MINUS_ONE = Fq(-1)

assert Fq.ZERO + Fq.ZERO == Fq.ZERO
assert Fq.ZERO + Fq.ONE == Fq.ONE
assert Fq.ONE + Fq.ZERO == Fq.ONE
assert Fq.ZERO - Fq.ONE == Fq.MINUS_ONE
assert Fq.ZERO * Fq.ONE == Fq.ZERO
assert Fq.ONE * Fq.ZERO == Fq.ZERO

#_A = Fq(-13443226831829260228624682877674385705155231329884953466695813022153219761455)
#_A_SQUARED = Fq(1615918303262283860389448007513155112015187847020867660361132469416696757234)
#assert _A * _A == _A_SQUARED
#assert _A.exp(2) == _A_SQUARED
#assert _A_SQUARED.sqrt() == _A


#
# Point arithmetic
#

class Point(object):
    @staticmethod
    def from_bytes(buf):
        assert len(buf) == 32
        u_sign = buf[31] >> 7
        buf = buf[:31] + bytes([buf[31] & 0b01111111])
        try:
            v = Fq.from_bytes(buf)
        except ValueError:
            return None

        vv = v * v
        u2 = (vv - Fq.ONE) / (vv * JUBJUB_D - JUBJUB_A)

        u = u2.sqrt()
        if not u:
            return None

        if u.s % 2 != u_sign:
            u = Fq.ZERO - u

        return Point(u, v)

    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __add__(self, a):
        (u1, v1) = (self.u, self.v)
        (u2, v2) = (a.u, a.v)

        u3 = (u1*v2 + v1*u2) / (Fq.ONE + JUBJUB_D*u1*u2*v1*v2)
        v3 = (v1*v2 - JUBJUB_A*u1*u2) / (Fq.ONE - JUBJUB_D*u1*u2*v1*v2)
        return Point(u3, v3)

    def double(self):
        return self + self

    def __mul__(self, s):
        # something weird is happenign here. When it ry to format int
        #s = '1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001'
        # as binary it gives me
        # 0001111100110111011000110001101000111101100111001011111110101100100011110101111101110100100100101111110011111101010011110100010110101111100110000010111101101111000011001000110100011110110111010111100000111100000101001101100000011111111111111111111111111111 256  
        # not sure what is causing this but will make a bug when i create repo
        # in the mean time you can gen test input by putting s = '10000...0001'
        s = format(s.s, '0253b')
        ret = self.ZERO
        for c in s:
            ret = ret.double()
               
            if int(c):
                ret = ret + self
            
        return ret

    def __bytes__(self):
        buf = bytes(self.v)
        if self.u.s % 2 == 1:
            buf = buf[:31] + bytes([buf[31] | (1 << 7)])
        return buf

    def __eq__(self, a):
        return self.u == a.u and self.v == a.v

    def __str__(self):
        return 'Point(%s, %s)' % (self.u, self.v)

    def is_on_curve(self):
        try:
            x = self.u
            y = self.v

            return (JUBJUB_A*(x*x) + (y*y) - Fq(1) - (JUBJUB_D * (x*x) * (y*y))) == Fq(0)
        except ValueError:
            return False




Point.ZERO = Point(Fq.ZERO, Fq.ONE)

assert Point.ZERO + Point.ZERO == Point.ZERO