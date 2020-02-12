#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import collections

from com.xebialabs.deployit.plugin.api.reflect import Type

class CIFactory(object):
    def __init__(self, repositoryService, metadataService, cfout):
        self.repositoryService = repositoryService
        self.metadataService = metadataService 
        self.cfout = cfout


    @staticmethod
    def new_instance(repositoryService, metadataService, cfout):
        return CIFactory(repositoryService, metadataService, cfout)


    def createCis(self, root, template):
        print "Creating configuration items in '%s'" % root

        # iterate over list of ci definitions in template
        for ci_tmpl in template:
            ci_info = self._replace_str(ci_tmpl)
            self._create_ci(root, ci_info)


    def deleteCis(self, root, template):
        print "Deleting configuration items in '%s'" % root

        for ci_tmpl in template:
            self._delete_ci(root, ci_tmpl)


    # INTERNAL FUNCTIONS -----------------------------------------

    # scan template for property placeholders, substitute values
    def _replace_str(self, tmpl):
        for k in tmpl:
            val = tmpl[k]
            try:
                # if value is a string, do the replacement if necessary
                if isinstance(val, basestring):
                    # replace values surrounded by single braces, not double braces (those will be replaced by an XLD dictionary)
                    if '{' in val and '{{' not in val:
                        tmpl[k] = val.format(**self.cfout)

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

        return tmpl


    def _create_ci(self, root, ci_info):
        print "Creating '%s' : '%s'" % (ci_info['type'], ci_info['id'])
        id = "%s/%s" % (root, ci_info['id'])
        ci_obj = None
        ci_already_exists = False

        if self.repositoryService.exists(id):
            print ("CI '%s' already exists, skipping creation" % id)
            ci_obj = self.repositoryService.read(id)
            ci_already_exists = True

        else:
            print ("CI '%s' does not exists, creating" % id)
            type_obj = Type.valueOf(ci_info['type'])
            ci_obj = self.metadataService.findDescriptor(type_obj).newInstance(id)

        # populate ci
        for prop in ci_info:
            if prop in ['id', 'type']:
                continue

            val = ci_info[prop]
            if type(val) is list:
                if prop in ['members']:
                    for listVal in val:
                        print("Adding member container %s to %s" % (listVal["ci ref"], ci_info['id'] ))
                        sub_ci_obj = self.repositoryService.read(listVal["ci ref"])
                        ci_obj.addMember(sub_ci_obj)
            else:
                ci_obj.setProperty(prop, val)

        # add or update ci to repository
        if ci_already_exists:
            self.repositoryService.update(id, ci_obj)
        else:
            self.repositoryService.create(id, ci_obj)


    def _delete_ci(self, root, ci_info):
        print "Deleting '%s' : '%s'" % (ci_info['type'], ci_info['id'])
        # We do not delete environments because they must be available for the next time provisioning is run
        if ci_info['type'] == 'udm.Environment':
            print("We found an environment so we will not delete but will delete member containers")
            id = "%s/%s" % (root, ci_info['id'])
            ci_obj = None
            # Creating an empty set
            memberSet= set()
            if self.repositoryService.exists(id):
                ci_obj = self.repositoryService.read(id)
                ci_obj.setMembers(memberSet)
                self.repositoryService.update(id, ci_obj)
        else:
            id = "%s/%s" % (root, ci_info['id'])
            if not self.repositoryService.exists(id):
                print "CI '%s' already deleted, skipping." % id
                return
            self.repositoryService.delete(id)
