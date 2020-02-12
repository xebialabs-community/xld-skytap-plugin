#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

def create_vars(deployed):
    vars = {}
    if deployed:
        vars['deployed'] = deployed
        print ("Server url = %s" % deployed.container["url"])
    if deployed and deployed.template_id:
        vars['template_id'] = deployed.template_id
        print ("Deployed template id = %s" % vars['template_id'])
    if deployed and deployed.project_id:
        vars['project_id'] = deployed.project_id
        print ("Deployed project id = %s" % vars['project_id'])
    if deployed and deployed.environment_id:
        vars['environment_id'] = deployed.environment_id
        print ("Deployed environment id = %s" % vars['environment_id'])
    
    return vars

def populate_mappings(data, mappings):
    outputMappdedDataFromVMs = {}
    for map in mappings:
        #Split the string
        mList = [int(e) if e.isdigit() else e for e in mappings[map].split('_')]
        newData = data
        for jIndex in mList:
            newData = newData[jIndex]
        outputMappdedDataFromVMs.update({str(map): str(newData)})       
    return outputMappdedDataFromVMs