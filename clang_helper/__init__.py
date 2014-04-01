import clang.cindex
from .extract_functions import extract_functions
from .extract_macros import extract_macro_constants
import collections
import blist
import itertools

class FeatureExtractor(object):
	"""This object is the interface to all of this module's functions.  Usage is simple; instanciate it with a ist of files, and then use the functions or macros attributes.
Most properties are available in two variants: *_dict and *_list.  The dict variant maps names of entities to their defining object, and the list variant simply returns the objects of that type in some undefined order.
"""

	def __init__(self, files, exclude_others = False, macros = ()):
		"""Extracts features only from those files passed in files, an iterable or a string.
macros allows one to pass a list of macros to define."""
		extra_args = ['-D'+i for i in macros]
		if isinstance(files, str) or isinstance(files, unicode):
			files = [files]
		self.files = set(files)
		self.index = clang.cindex.Index.create()
		self.translation_units = [self.index.parse(i, options = clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD, args = extra_args) for i in self.files]
		self.cursors = [i.cursor for i in self.translation_units]
		raw_functions = [func for i in self.cursors for func in extract_functions(i)]
		raw_macros = [macro for i in self.cursors for macro in extract_macro_constants(i)]
		#remove any files we aren't interested in.
		raw_macros = filter(lambda x: x.file in self.files or not exclude_others, raw_macros)
		raw_functions = filter(lambda x: x.file in self.files or not exclude_others, raw_functions)
		raw_file_contents = collections.defaultdict(lambda:blist.sortedlist(key = lambda x: x.line))
		#create the index of things by which file they're in.
		for i in itertools.chain(raw_functions, raw_macros):
			raw_file_contents[i.file].add(i)
		self.file_contents = raw_file_contents
		self.macros_dict = dict([(i.name, i) for i in raw_macros])
		self.functions_dict = dict([(i.name, i) for i in raw_functions])
		self.macros_list = raw_macros
		self.functions_list = raw_functions

	def get_functions_from_file(file):
		"""Generator.  Yields functions defined in a specific file."""
		return itertools.ifilter(lambda x: x.file == file, self.functions)

	def get_macros_from_file(file):
		"""Generator.  Yields macros from a given file."""
		return itertools.ifilter(lambda x: x.file == file, self.macros)
