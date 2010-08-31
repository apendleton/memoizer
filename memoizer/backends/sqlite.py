import sqlite3, cPickle, zlib, logging

log = logging.getLogger("memoizer")

class SQLiteCache:
	"""File-based database cache using SQLite3
	
	Stores and retrieves cache in/from an SQLite3 database using cPickle
	and zlib compression. Buffers updates into chunks until synchronization
	request."""
	
	def __init__(self, path=":memory:", volatile=False, protocol=-1, compression=7):
		"""Creates or loads database from file.
		
		path=:memory: <string>
			Path to file used to store SQLite database. If not specified,
			data will be created in memory only.
			
		volatile=False <boolean>
			Write updates to database on every change.
		
		protocol=-1 <integer>
			Pickle protocol. See documentation of module pickle.
			
		compression=7 <integer>
			Level of compression. See zlib documentation. If zero, compression
			is omitted."""
		self._path = path
		self._volatile = volatile
		self._protocol = protocol
		self._compression = compression
		self._cache = {}
		self._connection = sqlite3.connect(path)
		self._c =  self._connection.cursor()
		self._createTable()
		
	def _createTable(self):
		"""Creates memoizer table in SQLite database"""
		try:
			self._c.execute(SQL_CREATE)
		except IOError, err:
			log.exception(err)
	
	def __getitem__(self, key):
		"""Return cached value for key"""
		if self._cache.has_key(key):
			value = self._cache[key]
		else:
			self._c.execute(SQL_GET, (key,))
			result = self._c.fetchall()
			if len(result) == 1:
				value = result[0][0]
			else:
				raise KeyError(key)
		return vloads(value, self._compression)
	
	def __setitem__(self, key, value):
		"""Set cached value for key and update database if volatile mode"""
		self._cache[key] = vdumps(value, self._protocol, self._compression)
		if self._volatile:
			self.sync()
		
	def sync(self):
		"""Update database with buffered cache"""
		self._c.executemany(SQL_INSERT, self._cache.items())
		self._connection.commit()
		self._cache = {}
		
	def __del__(self):
		"""Make sure to close connection to SQLite database"""
		self._c.close()
		self._connection.close()
	

def vdumps(value, protocol, compression):
	if compression:
		return sqlite3.Binary(zlib.compress(cPickle.dumps(value, protocol), compression))
	else:
		return cPickle.dumps(value, protocol)

def vloads(value, compression):
	if compression:
		return cPickle.loads(zlib.decompress(value))
	else:
		return cPickle.loads(value)
		

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS memoizer (key STRING PRIMARY KEY, value BLOB)
"""

SQL_GET = """
SELECT value FROM memoizer WHERE key = ?
"""

SQL_INSERT = """
INSERT OR REPLACE INTO memoizer (key, value) VALUES (?, ?)
"""

if __name__ == "__main__":
	cache = SQLiteCache(path=":memory:")
	cache["abc"] = 123.5
	cache["def"] = "456"*50
	cache.sync()
	print cache["abc"]
	print cache["dff"]
	del cache