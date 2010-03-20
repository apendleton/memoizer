
import time, os.path
from memoizer import memoize


class LineCounter(object):
	
	def __init__(self, path):
		self.path = path
		self.f = open(path, "r")
	
	@memoize(backend='pickle')
	def count(self):
		time.sleep(1)
		return len(self.f.readlines())
	
	def __hash__(self):
		print os.path.getmtime(self.path)
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
	
	LineCounter.count.sync()
	
	