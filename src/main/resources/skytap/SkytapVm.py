#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import json
import collections

class SkytapVm(object):
    def __init__(self, ip, hostname, template):
        self.ip = ip
        self.hostname = hostname
        self.template = template
        #self._replace_str()



    
    # INTERNAL FUNCTIONS -----------------------------------------

    # scan template for property placeholders, substitute values
    def _replace_str(self):
        tmpl = self.template
        for k in tmpl:
            val = tmpl[k]
            '''
            try:
                # if value is a string, do the replacement if necessary
                if isinstance(val, basestring):
                    if '{' in val:
                        tmpl[k] = val.format(self)

                # if the value is a list, iterate over each item and process
                elif type(val) is list:
                    newval = []
                    for item in val:
                        newval.append(self._replace_str(item))
                    tmpl[k] = newval

                # if its iterable, recursively process
                elif isinstance(val, collections.Iterable):
                    tmpl[k] = self._replace_str(val)

            except KeyError:
                print "WARN: Property placeholder '%s' was not found in the output dictionary." % val
                '''

        return tmpl

    