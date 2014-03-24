class ExtractedObject(object):
	def __init__(self, cursor):
		self.cursor = cursor

class Macro(ExtractedObject):
	"""An extracted macro of the form #define constant value."""

	def __init__(self, name, value, *args, **kwargs):
		super(Macro, self).__init__(*args, **kwargs)
		self.name = name
		self.value = value

class Function(ExtractedObject):
	"""A function."""

	def __init__(self, name, return_type, arguments, *args, **kwargs):
		"""Arguments is a list: [(type1, name1), (type2, name2), ...]."""
		super(ExtractedFunction, self).__init__(*args, **kwargs)
		self.name = name
		self.return_type = return_type
		self.arguments = arguments

