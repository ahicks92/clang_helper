class ExtractedObject(object):
	def __init__(self, cursor):
		self.cursor = cursor

	def __str__(self):
		return "Undefined extracted object type."

	def __unicode__(self):
		return unicode(self.__str__())

class Macro(ExtractedObject):
	"""An extracted macro of the form #define constant value."""

	def __init__(self, name, value, *args, **kwargs):
		super(Macro, self).__init__(*args, **kwargs)
		self.name = name
		self.value = value

	def __str__(self):
		return "Macro: " + self.name + " " + self.value

	def __repr__(self):
		string = "<"
		string += self.__module__ + "." + self.__class__.__name__
		string += "("
		string += "name=" + self.name.__repr__() + ", "
		string += "value=" + self.value.__repr__() + ", "
		string += "cursor=" + self.cursor.__repr__()
		string += ")"
		return string

class Function(ExtractedObject):
	"""A function."""

	def __init__(self, name, return_type, arguments, *args, **kwargs):
		"""Arguments is a list: [(type1, name1), (type2, name2), ...]."""
		super(Function, self).__init__(*args, **kwargs)
		self.name = name
		self.return_type = return_type
		self.arguments = arguments


	def __str__(self):
		string = "Function: " + self.return_type + " " + self.name + "("
		for i, j in self.arguments:
			string += i + " " + j + ","
		string = string[:-1]
		string += ")"

	def __repr__(self):
		string = "<" +self.__module__ + "." + self.__class__.__name__ + "("
		string += "name=" + self.name.__repr__() + ", "
		string += "return_type=" + self.return_type.__repr__() + ", "
		string += "arguments=" + self.arguments.__repr__() + ", "
		string += "cursor=" + self.cursor.__repr__() + ")>"
		return string