#https://github.com/zcash-hackworks/zcash-test-vectors

#!/usr/bin/env python3

def cldiv(n, divisor):
    return (n + (divisor - 1)) // divisor

def i2lebsp(l, x):
    return [int(c) for c in format(x, '0%sb' % l)[::-1]]

def leos2ip(S):
    return int.from_bytes(S, byteorder='little')

# This should be equivalent to LEBS2OSP(I2LEBSP(l, x))
def i2leosp(l, x):
    return x.to_bytes(cldiv(l, 8), byteorder='little')

def ledna(bits):
    ret = 0
    for b in bits[::-1]:
        ret = ret * 2
        if b:
            ret += 1
    return ret

def lebs2osp(bits):
    l = len(bits)
    bits = bits + [0] * (8 * cldiv(l, 8) - l)
    return bytes([ledna(bits[i:i + 8]) for i in range(0, len(bits), 8)])

def leos2bsp(buf):
    return sum([[(c >> i) & 1 for i in range(8)] for c in buf], [])


assert i2leosp(5, 7) == lebs2osp(i2lebsp(5, 7))
assert i2leosp(32, 1234567890) == lebs2osp(i2lebsp(32, 1234567890))