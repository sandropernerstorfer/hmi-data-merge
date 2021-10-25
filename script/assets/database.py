from assets.filtering.P_AInHART import P_AInHART_Filter, P_AInHART_Merge

#
# --------------------------------------------------------------------------------------------------------- Available Safety Areas
#
safetyAreas = {
  '+H00': 'OSBL',
  '+H01': 'GC',
  '+H04': 'CIP',
  '+H05': 'PSA',
  '+H06': 'Distn',
  '+H07': 'CW',
  '+H08': 'Cogen',
  '+H09': 'WWT',
  '+H10': 'EtOH',
  '+H11': 'Civil',
  '+H12': 'OSBL',
  '+H14': 'Civil',
  '+H16': 'Civil',
  '+H17': 'FF',
  '+H19': 'ISBL',
  '+H20': 'ISBL',
  '+H21': 'ISBL',
  '+H22': 'WT',
  '+H23': 'GC',
  '+H24': 'WT',
  '+H25': 'WT',
  '+H26': 'AnalyC'
}

#
# --------------------------------------------------------------------------------------------------------- Available Typicals
#
typicals = {
  'P_AInHART': [P_AInHART_Filter, ['AI', 'DI', 'FI', 'LI', 'PDI', 'PI', 'SI', 'TI', 'XI'], P_AInHART_Merge]
}

#
# --------------------------------------------------------------------------------------------------------- Master Instrument List - Sheet Variables/Infos - Row & Column Locations
#
sheetName         = 'Index'
firstRow          = 8
pidColumn         = 3
locationColumn    = 5
typeColumn        = 6
tagColumn         = 7
descColumn        = 10
rangeColumn       = 46
unitColumn        = 47
routeColumn       = 29
safetyColumn1     = 34
safetyColumn2     = 35
safetyColumn3     = 36

#
# --------------------------------------------------------------------------------------------------------- ProcessLibraryOnlineConfigTool - Sheet Variables/Infos - Row & Column Locations
#
xls_key           = 3
xls_desc          = 5
xls_label         = 6
xls_tag           = 7
xls_area          = 8
xls_unit          = 9
xls_min           = 11
xls_max           = 12