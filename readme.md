clang_helper
============

*Important*: As of this writing (Clang 3.3) the Clang bindings on Pypi are missing an important and necessary attribute, `Type.spelling`.  Use the bindings included with this repository or the bindings included with the llvm and clang repositories if this error comes up.

This is a python module for the extraction of interesting features from source files.  At the moment, macro definitions and function definitions are supported.  This project depends on libclang's python bindings.


Rather than reading about me discussing the functionality of this library, consider instead the following informative example which prints information about the OpenAL headers.

~~~Python
import clang_helper
info = clang_helper.FeatureExtractor(['../camlorn_audio_rewrite/all_open_al.h'])
for i in info.functions_list[5:15]:
	print i
for i in filter(lambda  x: 'AL_' in x.name, info.macros_list)[5:15]:
	print i
~~~

For me, this yields:

~~~
Function: void alDisable(int capability)
Function: char alIsEnabled(int capability)
Function: const char * alGetString(int param)
Function: void alGetBooleanv(int param,char * values)
Function: void alGetIntegerv(int param,int * values)
Function: void alGetFloatv(int param,float * values)
Function: void alGetDoublev(int param,double * values)
Function: char alGetBoolean(int param)
Function: int alGetInteger(int param)
Function: float alGetFloat(int param)
Macro: 'AL_TRUE' 1
Macro: 'AL_SOURCE_RELATIVE' 514
Macro: 'AL_CONE_INNER_ANGLE' 4097
Macro: 'AL_CONE_OUTER_ANGLE' 4098
Macro: 'AL_PITCH' 4099
Macro: 'AL_POSITION' 4100
Macro: 'AL_DIRECTION' 4101
Macro: 'AL_VELOCITY' 4102
Macro: 'AL_LOOPING' 4103
Macro: 'AL_BUFFER' 4105


~~~

Note that the slicing operations and filter operations are not needed in real code. They simply print out an interesting subset.  The total list of everything being extracted is easily a few hunred items, much too long to print here.