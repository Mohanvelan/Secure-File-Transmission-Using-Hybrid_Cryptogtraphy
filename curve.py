from math import log
from copy import copy
from time import time 
from fractions import gcd
from random import SystemRandom 

rand=SystemRandom()


def hex2int(hexString):
	return int("".join(hexString.replace(":","").split()),16)

# Half the extended Euclidean algorithm:
def half_extended_gcd(aa, bb):
	lastrem, rem = abs(aa), abs(bb)
	x, lastx = 0, 1
	while rem:
		lastrem, (quotient, rem) = rem, divmod(lastrem, rem)
		x, lastx = lastx - quotient*x, x
	return lastrem, lastx 

# Modular inverse
def modular_inverse(a, m):
	g, x = half_extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m


#elliptic curve
class ECcurve:
	def __init__(self):
		return

	# Prime field multiplication: return a*b mod p
	def field_mul(self,a,b):
		return (a*b)%self.p

	# Prime field division: return num/den mod p
	def field_div(self,num,den):
		inverse_den = modular_inverse(den % self.p, self.p)
		return self.field_mul(num % self.p, inverse_den)

	# Prime field exponentiation: raise num to power mod p
	def field_exp(self,num,power):
		return pow(num % self.p,power, self.p)

	# Return the special identity point
	def identity(self):
		return ECpoint(self ,self.p, 0)
		#return (Q2.y-Q1.y)

	# Return true if point Q lies on our curve
	def touches(self,Q):
		y2=self.field_exp(Q.y,2)
		x3ab=(self.field_mul((Q.x*Q.x)%self.p+self.a,Q.x)+self.b)%self.p
		return y2==x3ab

	# Return the slope of the tangent of this curve at point Q
	def tangent(self,Q):
		return self.field_div(3*Q.x*Q.x + self.a, 2*Q.y)


	def line_intersect(self,Q1,Q2,m):
		v=(Q1.y + self.p - (m*Q1.x) % self.p) % self.p
		x=(m*m + self.p - Q1.x + self.p - Q2.x) % self.p
		y=(self.p - (m*x) % self.p + self.p - v) % self.p
		return ECpoint(self,x,y)

	# Return a doubled version of this elliptic curve point
	def double(self,Q):
		if (Q.x==self.p): 
			return Q
		return self.line_intersect(Q,Q,self.tangent(Q))

	# Return the "sum" of these elliptic curve points
	def add(self,Q1,Q2):
		# Identity special cases
		if (Q1.x==self.p): 
			return Q2
		if (Q2.x==self.p):
			return Q1

		# Equality special cases
		if (Q1.x==Q2.x):
			if (Q1.y==Q2.y):
				return self.double(Q1)
			else: 
				return self.identity()
			    #return self.field_div(Q2.y - Q1.y, Q2.x - Q1.x)

		# Ordinary case
		m=self.field_div(Q1.y + self.p - Q2.y, Q1.x + self.p - Q2.x)
		return self.line_intersect(Q1, Q2, m)
		
    # Return the point multiplied by a scanlar
	def mul(self,Q,m):
		R=self.identity()
		while m!=0:
			if m&1:
				R=self.add(R,Q)
			m=m>>1
			if (m!=0):
				# print("  mul: doubling Q =",Q);
				Q=self.double(Q)
		
		return R

# A point on an elliptic curve: (x,y)
class ECpoint:
	"""A point on an elliptic curve (x,y)"""
	def __init__(self,curve, x,y):
		self.curve=curve
		self.x=x
		self.y=y
			

	# "Add" this point to another point on the same curve
	def add(self,Q2):
		return self.curve.add(self,Q2)

	# "Multiply" this point by a scalar
	def mul(self,m):
		return self.curve.mul(self,m)

	# Print this ECpoint
	def __str__(self):
		if (self.x==self.curve.p):
			return "identity_point"
		else:
			return "("+str(self.x)+", "+str(self.y)+")"



secp256k1=ECcurve() #six tuple (p,a,b,G,n,h)
secp256k1.p=hex2int('0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f')
secp256k1.a=0
secp256k1.b=7
secp256k1.n=hex2int('0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141')

secp256k1.G=ECpoint(curve=secp256k1,
	x = hex2int('0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798'),
	y = hex2int('0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8'))

curve=secp256k1
Q=curve.G
