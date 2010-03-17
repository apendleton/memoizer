"""Tests for Cache Backends"""

import unittest, os
from os.path import join
from memoizer.config import CACHE_DIR
from memoizer.backends.pickle import PickleCache

class Object: pass

class BackendTest:
		
	def testCacheConsistency(self):
		cache = self.backend()
		#string consistency
		cache["key"] = "value"
		self.assertEqual(cache["key"], "value")
		
		#number consistency
		cache["int"] = 123
		self.assertEqual(cache["int"], 123)
		cache["float"] = 0.1
		self.assertAlmostEqual(cache["float"], 0.1)
		
		#list consistency
		cache["list"] = [1,2,3,4]
		self.assertEqual(cache["list"], [1,2,3,4])
		
		#object reference consistency
		obj = Object()
		obj.abc = 123
		cache["object"] = obj
		self.assertEqual(cache["object"].abc, 123)
		del cache
		
	def testCachePersistency(self):
		#remove previous cache file
		path = join(CACHE_DIR, self.__class__.__name__ + ".cache")
		if os.path.exists(path):
			os.remove(path)
			
		#cache some stuff and write to file
		cache = self.backend(path)
		cache["string"] = "abc"
		cache["number"] = 123
		obj = Object()
		obj.abc = "123"
		cache["object"] = obj
		cache.sync()
		del cache
		
		#read cache from file and test for consistency
		cache = self.backend(path)
		self.assertEqual(cache["string"], "abc")
		self.assertEqual(cache["number"], 123)
		self.assertNotEqual(cache["object"], obj)
		self.assertEqual(cache["object"].abc, "123")
		del cache


class TestPickleCache(BackendTest, unittest.TestCase):
	"""Test pickle backend."""
	
	def setUp(self):
		self.backend = PickleCache
		
		
		
if __name__ == "__main__":
	unittest.main()