.. Memoizer documentation master file, created by
   sphinx-quickstart on Sat Feb 27 09:23:24 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Memoizer's documentation!
====================================

Memoizer is a Python module that allows to cache a functions return value in 
order to prevent repeated calculation. (also known as `Memoization 
<http://en.wikipedia.org/wiki/Memoization>`_)

An Example
----------

Consider a recursive function ``fib`` that computes the n-th Fibonacci number::

	def fib(n):
	    return (n<=2) and 1 or fib(n-1)+fib(n-2)

When calling e.g. ``fib(10)`` the value of ``fib(5)`` is actually calculated 8 
times. That's just useless since the value of ``fib(5)`` will never change. So,
why not caching it::

	from memoizer import memoize
	
	@memoize()
	def fib(n):
	    return (n<=2) and 1 or fib(n-1)+fib(n-2)
		
Now, when calling ``fib(10)`` again, the value of ``fib(5)`` and all other 
``fib(n)`` functions are calculated only once. Each subsequent call is 
intercepted and the cached result is returned instead.
