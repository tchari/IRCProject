from math import pow
import decimal

def PMT(P, r, n):
	term1 = decimal.Decimal(pow((1+r),n))
	return P*r*term1/(term1 - 1)

def PV(P,r,n):
	term1 = decimal.Decimal(pow((1+r),n))
	return decimal.Decimal(P)*decimal.Decimal(1/r)*(1-1/term1)
