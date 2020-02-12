#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from skytap.Skytap import SkytapClient
from skytap_rules.ci_factory import CIFactory
from skytap_rules.common import create_vars
from skytap_rules.common import populate_mappings
import json

def process(task_vars):
    print("create_infrastructure_1")
    deployed = task_vars['deployed']

    vars = create_vars(deployed)
    
    skytap = SkytapClient.get_client(deployed.container)
    capturedVMOutput = skytap.skytap_environmentvmlist(vars)

    creationMetadata = []
    for vm in capturedVMOutput:
        mappingObj = {}
        metadata_dict = {}
        variableMappings = {}
        foundMetadata = False
        # TODO need to add check to make sure this is a Metadata note
        for note in vm["notes"]: 
            try:
                # TODO review the following
                metadata_dict = json.loads(note["text"])
                if metadata_dict['Metadata']:
                    foundMetadata = True
                    # We assume for this vm there is only one note with metadata, we will continue if and when we find it.
                    continue
            except KeyError:
                print("Can't find metadata")

        if foundMetadata:
            # process individually to guarantee order
            # have decided not to add applications at this time. 
            
            if 'XLD::VariableMappings' in metadata_dict['Metadata']:
                variableMappings = metadata_dict['Metadata']['XLD::VariableMappings']
                mappingObj = populate_mappings(vm, variableMappings)

            # populate the output variable creationMetadata. This info will be used when this provisioning package is undeployed
            creationMetadata.append(note["text"])
            ci_fact = CIFactory.new_instance(repositoryService, metadataService, mappingObj)
            
            if 'XLD::Infrastructure' in metadata_dict['Metadata']:
                ci_tmpl = metadata_dict['Metadata']['XLD::Infrastructure']
                ci_fact.createCis('Infrastructure', ci_tmpl)
                
            if 'XLD::Environments' in metadata_dict['Metadata']:
                ci_tmpl = metadata_dict['Metadata']['XLD::Environments']
                ci_fact.createCis('Environments', ci_tmpl)
                
    deployed.creationMetadata = creationMetadata
    


   

if __name__ == '__main__' or __name__ == '__builtin__':
    process(locals())

