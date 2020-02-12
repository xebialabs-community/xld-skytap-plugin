#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import inspect

class InspectVarsUtil():
	def __init__(self):
		pass

	def dig(self, i,obj):
		if not inspect.ismodule(obj) and not inspect.isclass(obj) and not inspect.isroutine(obj):
			if isinstance(obj, str) or isinstance(obj, unicode):	
				print "STRING OBJECT : " + i + " || VALUE : " + str(obj)
			else:
				print "COMPLEX OBJECT : " + i + " || TYPE : " + str(type(obj))	
			if dir(obj).__contains__("_delegate"):
				try:
					for item in inspect.getmembers(obj._delegate):
						if not inspect.isroutine(item[1]) and not inspect.isclass(item[1]) and (str(item[0]) not in ["__doc__"]):
							print "Property : "  + i + "." + item[0] + " || VALUE : " + str(item[1])
						if inspect.ismethod(item[1]) and (str(item[0]) not in ["hashCode","getClass","notify","notifyAll","equals","toString","wait","__init__","compareTo"]):
							print "Method : "  + i + "." + item[0] + "(...)"
				except :
					print "ERROR : Can't review properties on object " + i + " due to exception" 			

	def inspectGlobals(self):
		for i in globals():
			self.dig(i, globals()[i])

	def inspectVars(self, vars):
		for i in vars:
			self.dig(i, vars[i])