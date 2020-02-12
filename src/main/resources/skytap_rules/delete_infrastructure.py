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
    print("delete_infrastructure")
    deployed = task_vars['previousDeployed']
    
    for metadata in deployed.creationMetadata:
        metadata_dict = json.loads(metadata)
        
        ci_fact = CIFactory.new_instance(repositoryService, metadataService, metadata_dict)
        
        # process individually to guarantee order
        if 'XLD::Environments' in metadata_dict['Metadata']:
            ci_tmpl = metadata_dict['Metadata']['XLD::Environments']
            ci_fact.deleteCis('Environments', ci_tmpl)

        if 'XLD::Infrastructure' in metadata_dict['Metadata']:
            ci_tmpl = metadata_dict['Metadata']['XLD::Infrastructure']
            ci_fact.deleteCis('Infrastructure', ci_tmpl)

    print "Done"


if __name__ == '__main__' or __name__ == '__builtin__':
    process(locals())