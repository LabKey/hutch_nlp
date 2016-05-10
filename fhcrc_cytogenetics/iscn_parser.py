#
# Copyright (c) 2015-2016 Fred Hutchinson Cancer Research Center
#
# Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
#
import re,global_strings,json

'''author@esilgard'''
__version__='iscn_parser1.0'
import global_strings as gb

def get(karyotype_string,karyo_offset):
    '''
    parse ISCN cytogenetic information from a short string of text containing only information
    about the genetic variation/karyotype in the ISCN format
    refer to http://www.cydas.org/Docs/ISCNAnalyser/Analysis.html for ISCN formatting guidelines
    return a normal cell count (this could be 0) and
    a list of abnormal cell types that include the number of cells and a dictionary of any genetic abnormalities    
    '''
    return_list = []    
    seperate_cell_types = karyotype_string.split('/')    
    cell_type_order = 0

    for each_cell_type in seperate_cell_types:        
        d = {}
        d[gb.OFFSET] = karyo_offset+karyotype_string.find(each_cell_type)
        d[gb.ABNORMALITIES] = []
        d[gb.CELL_ORDER] = cell_type_order
        cell_count = re.match('.*(\[c?p?([\d]+)\]).*', each_cell_type)
        if cell_count:
            try:                
                d[gb.CELL_COUNT] = cell_count.group(2)
                each_cell_type = each_cell_type[:each_cell_type.find(cell_count.group(1))]                
            ## catches error when there is no cell count
            except:               
                d[gb.WARNING] = 1
            cell_description = each_cell_type.split(',')           
            try:
                d[gb.CHROMOSOME_NUM] = cell_description[0].strip()
                if re.search('[\d]n', cell_description[1]):
                    d[gb.CHROMOSOME_NUM] += cell_description[1]
                    cell_description = cell_description[1:]
                d[gb.CHROMOSOME] = cell_description[1].strip()
                d[gb.WARNING] = None               
            except:
                ## catches error when there is no chromosome type number and type                
                d[gb.WARNING] = 1
            ## if the length of the cell_description is greater than 2, then there are one or more abnormalities
            if len(cell_description) > 2:                
                d[gb.ABNORMALITIES] = cell_description[2:]
                if (d[gb.CHROMOSOME] == 'sl' or 'idem' in d[gb.CHROMOSOME]) and len(seperate_cell_types)>1:
                    try:
                        d[gb.CHROMOSOME] = return_list[0][gb.CHROMOSOME]
                    except:
                         d[gb.WARNING] = 1
                         d[gb.CHROMOSOME] = 'UNK'                    
                    d[gb.ABNORMALITIES] += return_list[0][gb.ABNORMALITIES]
                ## catch this typo - where the XX and XY is included in the idem/sl cell line reference - exclude the reference itself from the list of abnormalities
                elif (d[gb.ABNORMALITIES][0] == 'sl' or 'idem' in d[gb.ABNORMALITIES][0]) and len(seperate_cell_types) > 1:
                    d[gb.ABNORMALITIES] = return_list[0][gb.ABNORMALITIES] + d[gb.ABNORMALITIES][1:]
                
                ## when sdl is used to refer back to sl
                elif d[gb.CHROMOSOME] == 'sdl' and len(seperate_cell_types) > 2:                    
                    d[gb.CHROMOSOME] = return_list[1][gb.CHROMOSOME]
                    d[gb.ABNORMALITIES] += return_list[1][gb.ABNORMALITIES]
                ## catch the specific cell line references like sdl1 or sdl2 ##
                elif 'sdl' in d[gb.CHROMOSOME]:                    
                    try:                       
                        d[gb.CHROMOSOME] = return_list[cell_type_order-1][gb.CHROMOSOME]
                        d[gb.ABNORMALITIES] = return_list[cell_type_order-1][gb.ABNORMALITIES] + d[gb.ABNORMALITIES]
                    except:
                        d[gb.WARNING] = 1                        
               
            ## further parse abnormalities into dictionaries of type of mutation:chromosome specifics (number, location) ##
            for i in range(len(d[gb.ABNORMALITIES])):                
                if type(d[gb.ABNORMALITIES][i]) == str:
                    loss_gain = re.match('[ ]?([+-])[ ]?([\d\w\~\?]+)', d[gb.ABNORMALITIES][i])
                    ## should capture chromosome numbers, sex chromosomes, and 'or's/'?'s for ambiguous chromosomes
                    abnormal_chromosome = re.match('(.*)[(]([.\d;XY\?or ]+)[)](.*)', d[gb.ABNORMALITIES][i])                       
                    if loss_gain:
                        d[gb.ABNORMALITIES][i] = {loss_gain.group(1): (loss_gain.group(2), '')}
                    elif abnormal_chromosome:                       
                        d[gb.ABNORMALITIES][i] = {abnormal_chromosome.group(1): (abnormal_chromosome.group(2), abnormal_chromosome.group(3))}
                    else:
                        ## catches the case where there's no "type" of abnormality (eg del,der, +) because it's inferred
                        abnormal_chromosome = re.match('[ ]?([\d\-\~?\ ]*)[ ]?(mar|r|dmin|pstk+|inc)[ ]?', d[gb.ABNORMALITIES][i])
                        if abnormal_chromosome:
                            d[gb.ABNORMALITIES][i] = {'other aberration': (abnormal_chromosome.group(1), abnormal_chromosome.group(2))}
                        else:
                            d[gb.WARNING] = 1                  
                              
        else:
            d[gb.WARNING] = 1 
        return_list.append(d)                
        cell_type_order += 1
    return return_list, None, list
