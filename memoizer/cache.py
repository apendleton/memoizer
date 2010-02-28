

class FunctionCache:
	
	def __init__(self, func, cache):
		self.cache = cache
		self.func = func
	
	def __call__(self, *args, **kwargs):
		key = self.getKey(*args, **kwargs)
		try:
			result = self.cache[key]
		except KeyError:
			result = self.func(*args, **kwargs)
			self.cache[key] = result
		return result
	
	def getKey(self, *args, **kwargs):
		return str((tuple(args), frozenset(kwargs)).__hash__())
