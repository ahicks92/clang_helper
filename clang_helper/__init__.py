import clang.cindex
from .extract_functions import extract_functions
from .extract_macros import extract_macros

class FeatureExtractor(object):
	"""This object is the interface to all of this module's functions.  Usage is simple.
Note that many of these properties are lazy, in order to facilitate wasted time.  The rational for this is that the intent of this library is to be incorporated into build systems, and half of the information is only used in specific circumstances.
"""

	def __init__(self, files):
		"""Extracts features only from those files passed in files, an iterable."""
		self.files = set(files)
		self.index = clang.cindex.Index.create()
		self.translation_units = [self.index.parse(i) for i in self.files]
		self.cursors = [i.cursor for i in self.translation_units]
		raw_functions = func for i in self.cursors for func in extract_functions(i)]
		raw_macros = [macro for i in self.cursors for macro in extract_macros(i)]
		#remove any files we aren't interested in.
		raw_macros = filter(lambda x: x.file in self.files, raw_macros)
		raw_functions = filter(lambda x: x.file in self.files, raw_functions)
