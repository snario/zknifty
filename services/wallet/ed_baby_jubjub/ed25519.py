# The Ed25519 software is in the public domain. 
# http://ed25519.cr.yp.to/software.html

import hashlib
import pdb
from .sapling_jubjub import *
import codecs 


def hexToBinary(hexString):
  out = [ int(x) for x in bin(int(hexString, 16))[2:].zfill(256)]
  return(out)

def hashPadded(left, right):
  
  x1 = int(left , 16).to_bytes(32, "big")
  x2 = int(right , 16).to_bytes(32, "big")

  data = x1 + x2
  answer = hashlib.sha256(data).hexdigest()
  
  return(answer)


def H(m):
  size = len(m)
  # if m is too long break it into two hashes

  if(size > 128):
    m = H(m[0:size//2]) + H(m[size//2:])
  #pad m if its too short
  #if len(m) != 128:
    #pdb.set_trace()
  m = m + "0" *(128 - len(m)) 

  return hashPadded(m[:64], m[64:])


def xrecover(y):
  xx = (y*y-1) * inv(d*y*y+1)
  x = expmod(xx,(q+3)//8,q)
  if (x*x - xx) % q != 0: x = (x*I) % q
  if x % 2 != 0: x = q-x
  return x

def expmod(b,e,m):
  if e == 0: return 1

  t = expmod(b,int(e//2),m)**2 % m
  if int(e) & 1: t = (t*b) % m
  return t

def inv(x):
  return expmod(x,q-2,q)

'''
b = 256
q = 2**255 - 19
l = 2**252 + 27742317777372353535851937790883648493


d = -121665 * inv(121666)
I = expmod(2,(q-1)/4,q)
a = -1


# taken from github.com/barrywhitehat/jubjub
By = 4 * inv(5) #17777552123799933955779906779655732241715742912184938656739573121738514868268 #4 * inv(5)
Bx = xrecover(By) #2626589144620713026669568689430873010625803728049924121243784502389097019475 #xrecover(By)
B = [Bx % q,By % q]
print("    base     " , B)
'''



b = 126 # beacuse b * 2  must be less than the max element that exists in the field. otherwise we cannot encode it inside zksnark.
q = 21888242871839275222246405745257275088548364400416034343698204186575808495617 #2**255 - 19
l = 2736030358979909402780800718157159386076813972158567259200215660948447373041 #2**252 + 27742317777372353535851937790883648493

d = 168696 #-121665 * inv(121666)
a = 168700 
I = expmod(2,(q-1)/4,q)

Bx = 17777552123799933955779906779655732241715742912184938656739573121738514868268 #4 * inv(5)
By = 2626589144620713026669568689430873010625803728049924121243784502389097019475 #xrecover(By)



'''
b = 16
q = q_j
l = r_j

d = -121665 * inv(121666)
I = expmod(2,(q-1)/4,q)
a = -1

Bx = 15112221349535400772501151409588531511454012693041857206046113283949847762202 #4 * inv(5)
By = 46316835694926478169428394003475163141307993866256225615783033603165251855960 #xrecover(By)
'''
B = [Bx % q,By % q]




def edwards(P,Q):
  x1 = P[0]
  y1 = P[1]
  x2 = Q[0]
  y2 = Q[1]
  x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2)
  y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2)
  return [x3 % q,y3 % q]

def scalarmult(P,e):
  '''
  if e == 0: return [0,1]
  Q = scalarmult(P,int(e//2))
  Q = edwards(Q,Q)
  if e & 1: Q = edwards(Q,P)

  return Q
  '''
  point = Point(Fq(P[0]), Fq(P[1])) 


  out = point * Fq(e)

  return([int(out.u), int(out.v)])
  
def pointAddition(P, e):
  '''
  print(" input   ", P, e)
  print(" result  ", edwards(P,e))
  point1 = Point(Fq(P[0]), Fq(P[1]))
  point2 = Point(Fq(e[0]), Fq(e[1]))
  out = point1 + point2
  print("  pot out", int(out.v), out)
  print("  is equal" , edwards(P,e) == [int(out.u), int(out.v)])
  '''
  #return edwards(P,e)
  
  point1 = Point(Fq(P[0]), Fq(P[1]))
  point2 = Point(Fq(e[0]), Fq(e[1]))
  out = point1 + point2
  return([int(out.u), int(out.v)])
  

def encodeint(y):
  bits = [(y >> i) & 1 for i in range(b)]
  return ''.join([chr(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b/8)])

def encodepoint(P):
  x = P[0]
  y = P[1] 
  
  x = hex(int(''.join(str(e) for e in hexToBinary(hex(x))[::-1]),2))
  y = hex(int(''.join(str(e) for e in hexToBinary(hex(y))[::-1]),2))
  out = hashPadded(x,y)

  return(out)
  '''
  bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
  out = ''.join([chr(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(int(b//8))])
  print(" out " , len(out), out)
  return( codecs.encode(codecs.encode(out, "utf-8"), "hex_codec").decode("utf-8")  )
  '''
def bit(h,i):
  out = bin(int(h,16))[2:].zfill(256)[i]
  return int(out)

def publickey(sk):
  h = H(sk)
  a = 2**(b-2) + sum(2**i * bit(h,i) for i in range(3,b-2))
  A = scalarmult(B,a)
  return A

def Hint(m):

  #this is engineered to match the libsnark
  #packing gagdget which willl convert h  
  # to a field element
  h = H(m)
  tmp = []
  tmp2 = []
  out = 0
  size = 2*b + 1
  for i in range(size)[::-1]:

    tmp.append(bit(h,i))
    tmp3 = str(bit(h,i)) + "+ " + str(out) + "+ " + str(out) + "=  " 
    out = out + out + bit(h, i)
    #print (tmp3 + str(out))

  #reverse endineess and return

  binary = bin(out)[2:][::-1].ljust(size,"0")
  binary = binary[:size]

  return(int(binary,2))



def signature(m,sk,pk):
  h = H(sk)
  a = 2**(b-2) + sum(2**i * bit(h,i) for i in range(3,b-2))
  r = Hint(''.join([h[i] for i in range(int(b//8),int(b//4))]) + m)
  R = scalarmult(B,r)
  h =  Hint( hashPadded(encodepoint(R) , encodepoint(pk)) + m) 
  S = (r + h * a) % l
  return R, S

def decodeint(s):
  return sum(2**i * bit(s,i) for i in range(0,b))

def decodepoint(s):
  y = sum(2**i * bit(s,i) for i in range(0,b-1))
  x = xrecover(y)
  if x & 1 != bit(s,b-1): x = q-x
  P = [x,y]
  if not isoncurve(P): raise Exception("decoding point that is not on curve")
  return P

def checkvalid(R, S,m,pk):
  A = pk
  h = Hint(hashPadded(encodepoint(R) , encodepoint(pk)) + m)

  
  if scalarmult(B,S) != pointAddition(R,scalarmult(A,h)):
    raise Exception("signature does not pass verification")