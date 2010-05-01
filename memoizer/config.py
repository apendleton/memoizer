"""Some basic settings"""

import os, tempfile
from os.path import join, normpath
from memoizer.backends import pickle, sqlite

BACKENDS = {
	'pickle': pickle.PickleCache,
	'sqlite': sqlite.SQLiteCache,
}

DEFAULT_PATH	 = None
DEFAULT_BACKEND  = None
DEFAULT_HASH	 = None
DEFAULT_VOLATILE = None
DEFAULT_VERBOSE	 = False

CACHE_DIR = normpath(join(tempfile.gettempdir(), "memoizer"))

# make sure CACHE_DIR exists
if not os.path.exists(CACHE_DIR): os.mkdir(CACHE_DIR)