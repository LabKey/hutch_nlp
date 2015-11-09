'''author@esilgard'''
#
# Copyright (c) 2013-2015 Fred Hutchinson Cancer Research Center
#
# Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
#

from OneFieldPerSpecimen import OneFieldPerSpecimen
import global_strings as gb

class PathSpecimenType(OneFieldPerSpecimen):
    ''' extract speciment type (procedure) from path text '''
    __version__ = 'SpecimenType1.0'

    def __init__(self):
        self.specimen_field_name = 'SpecimenFindType'
        self.overall_field_name = 'SpecimenType'
        self.specimen_table = gb.FINDING_TABLE
        self.overall_table = gb.PATHOLOGY_TABLE
        self.specimen_confidence = 0.7
        self.unlabled_specimen_confidence = 0.5
        self.return_d_list = []
        ## reference lists & dictionaries ##
        self.file_name_string = 'procedures'
        self.dz_specific_list = []
        self.dz_specific_standardizations = {}
        self.general_list = []
        self.general_standardizations = {}
        ## relevant sections of the report ##
        self.good_section = \
                r'SPECIMEN|Specimen|IMPRESSION|DIAGNOSIS|COMMENT|DX|DESCRIPTION|DESC|GROSS'
        self.bad_section = r'CLINICAL|Note'
