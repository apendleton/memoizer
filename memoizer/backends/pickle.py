"""Simple file based cache using Pickle"""

import sys, cPickle

class PickleCache:
	"""Simple file based cache using Pickle
	
	Holds cached values in memory and later writes them to a file using 
	cPickle. If volatile mode is enabled, cache is written to file on each
	change."""
	
	def __init__(self, path=None, volatile=False, protocol=-1):
		"""Load cache from file if specified
		
		path=None <string>
			Path to file used to store cache permanently. If not specified,
			cache will not be written to file.
		
		volatile=False <boolean>
			Write cache to file on every change.
			
		protocol=-1 <integer>
			Pickle protocol. See documentation of module pickle."""
		self._path = path
		self._volatile = volatile
		self._protocol = protocol
		self._cache = {}
		try:
			f = open(path, 'rb')
			self._cache = cPickle.load(f)
			f.close()
		except (TypeError, IOError):
			pass
	
	def __getitem__(self, key):
		"""Return cached value for key"""
		return self._cache[key]
		
	def __setitem__(self, key, value):
		"""Set cached value for key and write to file if volatile mode"""
		self._cache[key] = value
		if self._volatile:
			self.sync()
	
	def sync(self):
		"""Write cache to file if specified"""
		if self._path:
			f = open(self._path, 'wb')
			cPickle.dump(self._cache, f, self._protocol)
			f.close()		
	
	def __del__(self):
		"""Try to synchronise before deletion"""
		try:
			self.sync()
		except:
			print >> sys.stderr, "Memoizer: Could not write to cache file."
			pass