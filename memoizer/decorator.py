"""Main Decorator"""

import inspect
from os.path import basename, join
from functools import wraps

from memoizer.config import BACKENDS, CACHE_DIR
from memoizer.cache import FunctionCache

def memoize(path=None, backend='pickle', volatile=False):
	"""Memoization Decorator.
	
	Functions that are decorated by this decorator are cached and only evaluated
	if its return value can not be retrieved from the cache.
	
	path=None
		Path to a file storing the function cache. If path is ``None`` the cache
		is not saved to a file. If it is ``'auto'`` a path is generated from the
		function's name.
		
	backend='pickle'
		Cache backend that manages the function cache. See cache backends.
		
	volatile=False
		If ``True`` the cache file is updated on each evaluation of the 
		function. Otherwise it is updated on exit or when memoizer.sync() is
		called."""
	def g(func):
		cache = [] #declare pointer to function cache
		@wraps(func)
		def h(*args, **kwargs):
			if not cache: #initialize function cache
				cache_cls = BACKENDS[backend]
				if path == 'auto':
					filepath = _getPath(func, *args)
				else:
					filepath = path
				cache.append(
					FunctionCache(func, cache_cls(filepath, volatile))
				)
			return cache[0](*args, **kwargs)
		return h
	return g

def _getPath(func, *args):
	"""Default path to cache file"""
	return join(CACHE_DIR, _getName(func, *args))

def _getName(func, *args):
	"""Default name of cache file"""
	if hasattr(func, "im_class"): 
		#bound class method 
		if func.im_class.__module__ != "__main__":
			name = func.im_class.__module__ 
		else:
			name = basename(inspect.getfile(func))
		name += "." + func.im_class.__name__ + "." + func.__name__
	
	elif func.func_code.co_varnames and func.func_code.co_varnames[0] == 'self': 
		#unbound class method
		if args[0].__class__.__module__ != "__main__":
			name = args[0].__class__.__module__ 
		else:
			name = basename(inspect.getfile(func))
		name += "." + args[0].__class__.__name__ + "." + func.__name__
	
	else: 
		#top-level function
		if func.__module__ != "__main__":
			name = func.__module__
		else:
			name = basename(inspect.getfile(func))
		name += "." + func.__name__
	
	return name +".cache"