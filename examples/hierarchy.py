import logging
from memoizer import memoize

class BaseClass:
	
	@memoize(verbose=True)
	def evaluate(self):
		return "base"
	
	def __repr__(self):
		return "BaseClass"
	
class LeftClass:
	
	def __init__(self, base):
		self.base = base
		self.state = 0
	
	@memoize(verbose=True)
	def evaluate(self):
		self.base.evaluate()
		return "left"
	
	def __hash__(self):
		return hash((self.base, self.state))
	
	def changeState(self):
		self.state = 1
	
	def __repr__(self):
		return "LeftClass"
	
class RightClass:
	
	def __init__(self, base):
		self.base = base
	
	@memoize(verbose=True)
	def evaluate(self):
		self.base.evaluate()
		return "right"
	
	def __hash__(self):
		return hash(self.base)
	
	def __repr__(self):
		return "RightClass"
	
class TopClass:
	
	def __init__(self, left, right):
		self.left = left
		self.right = right
	
	@memoize(verbose=True)
	def evaluate(self):
		self.left.evaluate()
		self.right.evaluate()
		return "top"
	
	def __repr__(self):
		return "TopClass"
	
	def __hash__(self):
		return hash((self.left, self.right))

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	
	base = BaseClass()
	left = LeftClass(base)
	right = RightClass(base)
	top = TopClass(left, right)
	
	print "Advantage 1: Base class is only evaluated once"
	print
	top.evaluate()
	print 
	print "Advantage 2: Repeated access to all classes not necessary"
	print
	top.evaluate()
	print 
	print "Advantage 3: Once a part in the hierarchy has changed, only the "
	print "             affected classes are evaluated again"
	print
	left.changeState()
	top.evaluate()
	