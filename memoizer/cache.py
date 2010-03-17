
from inspect import getfile
from os.path import basename, join
from memoizer.config import BACKENDS, CACHE_DIR
from memoizer.config import DEFAULT_PATH, DEFAULT_BACKEND
from memoizer.config import DEFAULT_HASH, DEFAULT_VOLATILE

try: #try to import module decorator
	from decorator import decorator
except ImportError: #load included decorator module
	from lib.decorator import decorator


class FunctionCache:
	
	def __init__(self, path=None, backend=None, hash=None, volatile=False):
		self.path = path
		self.backend = backend
		self.hash = hash
		self.volatile = volatile
		self.dict = {}
		self.cache = None
		self.callable = None
	
	def __call__(self, func, args, kwargs):
		if not self.callable:
			self.callable = func #remember callable
		if not self.cache and self.backend: 
			#initialize persistent cache backend
			cache_cls = BACKENDS[self.backend]
			if self.path == 'auto':
				filepath = _getPath(self.callable, args)
			else:
				filepath = self.path
			self.cache = cache_cls(filepath, self.volatile)
		#lookup caches
		key = self.getKey(*args, **kwargs)
		try:
			result = self.dict[key] #try to load from memory cache
		except KeyError:
			if self.cache: 
				try: #if not in memory cache try persistent cache
					result = self.cache[key]
				except KeyError:
					result = self.callable(*args, **kwargs)
					self.cache[key] = result #store in persistent cache
					self.dict[key] = result  #store in memory cache
			else: 
				result = self.callable(*args, **kwargs)
				self.dict[key] = result #only store in memory cache
		return result
	
	def sync(self):
		if self.cache:
			self.cache.sync()
	
	def getKey(self, *args, **kwargs):
		if self.hash:
			return str(self.hash(*args, **kwargs))
		return str((tuple(args), frozenset(kwargs)).__hash__())


def _getPath(func, args=[]):
	"""Default path to cache file"""
	return join(CACHE_DIR, _getName(func, args))


def _getName(func, args=[]):
	"""Default name of cache file"""
	if hasattr(func, "im_class"): 
		#bound class method 
		if func.im_class.__module__ != "__main__":
			name = func.im_class.__module__ 
		else:
			name = basename(getfile(func))
		name += "." + func.im_class.__name__ + "." + func.__name__
	
	elif func.func_code.co_varnames and func.func_code.co_varnames[0] == 'self': 
		#unbound class method
		if args[0].__class__.__module__ != "__main__":
			name = args[0].__class__.__module__ 
		else:
			name = basename(getfile(func))
		name += "." + args[0].__class__.__name__ + "." + func.__name__
	
	else: 
		#top-level function
		if func.__module__ != "__main__":
			name = func.__module__
		else:
			name = basename(getfile(func))
		name += "." + func.__name__
	
	return name +".cache"


def memoize(path=DEFAULT_PATH, hash=DEFAULT_HASH, backend=DEFAULT_BACKEND, 
		volatile=DEFAULT_VOLATILE):
	"""Memoization Decorator.
	
	Functions that are decorated by this decorator are cached and only evaluated
	if its return value can not be retrieved from the cache.
	
	path=None
		Path to a file storing the function cache. If path is ``None`` the cache
		is not saved to a file. If it is ``'auto'`` a path is generated from the
		function's name.
		
	hash=None
		Function that returns the hash value for a set of arguments and key-word
		arguments.
	
	backend=None
		Cache backend that manages permanent function cache. See cache backends.
	
	volatile=False
		If ``True`` the cache file is updated on each evaluation of the 
		function. Otherwise it is updated on exit or when memoizer.sync() is
		called."""
	cache = FunctionCache(path, backend, hash, volatile)
	def g(f):
		@decorator
		def h(func, *args, **kwargs):
			return cache(func, args, kwargs)
		wrapper = h(f)
		wrapper.sync = cache.sync
		return wrapper
	return g
