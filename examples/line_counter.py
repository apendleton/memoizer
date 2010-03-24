"""Example demonstrating persistent caching.

This example shows how you can decorate a function in a way that its result is
stored persistently, yet the cache recognises when the function has to be 
re-evaluated."""

import time, os.path
from memoizer import memoize

class LineCounter(object):
	"""Counts the number of lines of a file"""
	
	def __init__(self, path):
		self.path = path
	
	@memoize(backend='pickle')
	def count(self):
		"""Is executed at most once, then the cached result is returned."""
		time.sleep(1) #makes sure you can see the difference
		f = open(self.path, "r")
		lines = len(f.readlines())
		f.close()
		return lines		
	
	def __hash__(self):
		"""Computes a unique hash that only changes when 'count' needs to be 
		evaluated again."""
		return hash((
			self.path,
			os.path.getmtime(self.path)
		))


if __name__ == "__main__":
	lc = LineCounter(__file__)
	#first
	started = time.time()
	count = lc.count()
	print "First: counted %d lines in %.5f" % (count,time.time()-started)
	
	#second
	started = time.time()
	count = lc.count()
	print "Second: counted %d lines in %.5f" % (count,time.time()-started)
	
	#make sure cache is stored persisently
	LineCounter.count.sync()
