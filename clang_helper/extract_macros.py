"""Utilities for extracting macros and preprocessor definitions from C files.  Depends on Clang's python bindings.
Note that cursors have children, which are also cursors.  They are not iterators, they are nodes in a tree.
Everything here uses iterators.  The general strategy is to have multiple passes over the same cursor to extract everything needed, and this entire file can be viewed as filters over raw cursors."""
import itertools
import clang.cindex as cindex
import re
from . flatten_cursor import flatten_cursor
from .extracted_features import Macro

def extract_preprocessor_cursors(cursor):
	"""Get all preprocessor definitions from a cursor."""
	for i in flatten_cursor(cursor):
		if i.kind.is_preprocessing():
			yield i

def extract_macro_cursors(c):
	"""Get all macros from a cursor."""
	return itertools.ifilter(lambda x: x.kind == cindex.CursorKind.MACRO_DEFINITION, extract_preprocessor_cursors(c))

def transform_token(token):
	"""Returns a string representation of token.  If it is a C numeric constant, it is transformed into a python numeric constant."""
	#these are from python docs.
	find_float = "[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?"
	find_int = "[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)"
	untransformed_string = token.spelling
	try_find_int = re.match(find_int, untransformed_string)
	try_find_float = re.match(find_float, untransformed_string)
	new_string = untransformed_string
	if try_find_int is not None:
		new_string = try_find_int.group()
	elif try_find_float is not None:
		new_string = try_find_float.group()
	return new_string

def extract_macros(c):
	"""Uses eval and some regexp magic and general hackiness to extract as many macros as it possibly can.
Returns a tuple.  The first element is a list of Macro objects; the second is a list of strings that name macros we couldn't handle."""
	handled_macros = []
	currently_known_macros = dict()
	failed_macros = []
	possible_macro_cursors = extract_macro_cursors(c)
	#begin the general awfulness.
	for i in possible_macro_cursors:
		desired_tokens = list(i.get_tokens())[:-1] #the last one is something we do not need.
		name_token = desired_tokens[0]
		name = name_token.spelling
		desired_tokens = desired_tokens[1:]
		if len(desired_tokens) == 0:
			#the value of this macro is none.
			value = None
			m = Macro(name = name, value = value, cursor = i)
			handled_macros.append(m)
			currently_known_macros[m.name] = m.value
			continue
		#otherwise, we have to do some hacky stuff.
		token_strings = [transform_token(j) for j in desired_tokens]
		eval_string = "".join(token_strings)
		try:
			print name + ":", eval_string
			value = eval(eval_string, currently_known_macros)
			if isinstance(value, type):
				raise ValueError("Value resolved to class, not instance.")
		except:
			failed_macros.append(name)
			continue
		m = Macro(value = value, name = name, cursor = i)
		handled_macros.append(m)
		currently_known_macros[m.name] = m.value
	return handled_macros, failed_macros
