#
# Copyright (c) 2015 Fred Hutchinson Cancer Research Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys,json

'''
    read in full json metadata dictionary from resource file
    return metadata dictionary of relevant fields for the given
    document and disease group
'''

def get(nlp_engine_path,arguments):

    ## path to file containing the metadata dictionary (in json format) ##
    try:
        meta_data_file=open(nlp_engine_path+'metadata.json','r')
        try:
            metadata_d=json.load(meta_data_file)
            meta_data_file.close()
        except:
            sys.stderr.write('FATAL ERROR: json could not load metadata dictionary file, potential formatting error.  program aborted.')
            sys.exit(1)
    except:
        sys.stderr.write('FATAL ERROR: metadata dictionary file not found.  program aborted.')
        sys.exit(1)

    ## only output the appropriate metadata for the given document type
    metadata_d = metadata_d.get(arguments.get('-t'))
       
    return metadata_d