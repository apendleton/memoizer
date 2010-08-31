import random, time
from memoizer import memoize

@memoize(backend='sqlite')
def getSQLiteResults(seed):
	random.seed(seed)
	return [random.random() for _ in range(10000)]

@memoize(backend='pickle')
def getPickleResults(seed):
	random.seed(seed)
	return [random.random() for _ in range(10000)]

if __name__ == "__main__":
	print "Run this program at least twice in order to see the difference"
	print "in scaleability of both backends:"
	print
	
	print "First access:"
	
	started = time.time()
	getSQLiteResults(25) #gets only the right part of the cache
	print "SQLite needs %.5f seconds (one database access)" \
		% (time.time()-started)
	
	started = time.time()
	getPickleResults(25) #loads the whole cache into memory
	print "Pickle needs %.5f seconds (loads whole pickle file into memory) " \
		% (time.time()-started)
	
	print
	print "Second access:"
	
	started = time.time()
	getSQLiteResults(30) #the same as before
	print "SQLite needs %.5f seconds (roughly the same as before) " \
		% (time.time()-started)
	
	started = time.time()
	getPickleResults(30) #whole cache already in memory, means faster
	print "Pickle needs %.5f seconds (a lot faster because from memory)" \
		% (time.time()-started)
		
	for i in range(50):
		getSQLiteResults(i)
		getPickleResults(i)
	
	getSQLiteResults.sync()
	getPickleResults.sync()
	
	
	
	