
import time
from memoizer import memoize

@memoize()
def fib(n):
	return (n<=2) and 1 or fib(n-1)+fib(n-2)

def fib_old(n):
	return (n<=2) and 1 or fib_old(n-1)+fib_old(n-2)

if __name__ == "__main__":
	print "	fib		memoized fib"
	for n in [1,5,10,20,30,35]:
		print "n=%d	" % n,
		
		#test regular fibonacci
		started = time.time()
		fib_old(n)	
		print "%.5f		" % (time.time()-started),
		
		#test cached fibonacci
		started  = time.time()
		fib(n)		
		print "%.5f" % (time.time()-started)
	