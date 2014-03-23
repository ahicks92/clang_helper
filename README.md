clang_helper
============

This is a python module for the extraction of interesting features from source files.  At the moment, macro definitions and function definitions are supported.  This project depends on libclang's python bindings.

Macros of the form `#define constant 1234` can be extracted into python dicts: `{'constant': 1234}`

And functions are turned into lists as follows:

~~~Python
C:\projects\clang_helper>python
Python 2.7.6 (default, Nov 10 2013, 19:24:18) [MSC v.1500 32 bit (Intel)] on win
32
Type "help", "copyright", "credits" or "license" for more information.
>>> import clang.cindex as cindex
>>> import clang_helper
>>> from clang_helper import extract_functions
>>> ind = cindex.Index.create()
>>> tu = ind.parse('../camlorn_audio_rewrite/all_open_al.h')
>>> func = list(extract_functions.extract_functions(tu.cursor))[5]
>>> print func
(<clang.cindex.Cursor object at 0x022872B0>, ('alDisable', ('int', 'capability')
))
>>> print list(extract_functions.extract_functions(tu.cursor))[7]
(<clang.cindex.Cursor object at 0x02287B70>, ('alGetString', ('int', 'param')))
>>>
~~~