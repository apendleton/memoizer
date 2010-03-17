"""Tests for Memoize Decorator"""

import unittest, random, os, inspect
from memoizer import memoize
from memoizer.cache import _getPath

class TestDecorator(unittest.TestCase):
	
	def testFunctionDecorator(self):
		#verify consecutive calls return same value
		v1 = function(1)
		v2 = function(2)
		self.assertEquals(function(1), v1)
		self.assertEquals(function(2), v2)

	def testMethodDecorator(self):
		#create two instances with different parameter
		c1 = Class(1)
		c2 = Class(2)
		#store verification values
		c1v1 = c1.method(1)
		c1v2 = c1.method(2)
		c2v1 = c2.method(1)
		c2v2 = c2.method(2)
		#check values against cache
		self.assertEquals(c1.method(1), c1v1)
		self.assertEquals(c1.method(2), c1v2)
		self.assertEquals(c2.method(1), c2v1)
		self.assertEquals(c2.method(2), c2v2)
		#be sure that c1 and c2 are not handled equally
		self.assertNotEqual(c1.method(1), c2.method(1))
		self.assertNotEqual(c1.method(2), c2.method(2))
		del c1, c2
		
	def testDecoratorPersistency(self):
		#define undecorated function
		def rand():
			return random.random()
		#delete cache file if present
		path = _getPath(rand)
		if os.path.exists(path):
			os.remove(path)
		#apply decorator
		rand = memoize(path='auto', backend='pickle')(rand)
		#remember random value for verification
		r = rand()
		#make sure cache file is written
		rand.sync()
		del rand 
		
		#define function once more
		@memoize(path='auto', backend='pickle')
		def rand():
			return random.random()
		#function value should match r (because the cached value is returned)
		self.assertEqual(rand(), r)

	def testDecoratorMetadata(self):
		#define undecorated function
		def rand(my_arg, my_kwarg=123, *args, **kwargs):
			return random.random()
		#store metadata
		name = rand.__name__
		docs = rand.__doc__
		spec = inspect.getargspec(rand)
		del rand
		#define function once more, now decorated
		@memoize()
		def rand(my_arg, my_kwarg=123, *args, **kwargs):
			return random.random()
		#check for same meta data
		self.assertEquals(name, rand.__name__)
		self.assertEquals(docs, rand.__doc__)
		self.assertEquals(spec, inspect.getargspec(rand))

@memoize()
def function(argument):
	return random.random()

class Class:
	
	def __init__(self, parameter):
		self.parameter = parameter
	
	@memoize()
	def method(self, argument):
		return random.random()
		
	def __hash__(self):
		return (self.__class__.__name__, self.parameter).__hash__()