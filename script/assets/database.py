from assets.filtering.P_AinHART import *

#
# --------------------------------------------------------------------------------------------------------- Available Safety Areas
#
safetyAreas = {
  '+H06': 'Distn'
}

#
# --------------------------------------------------------------------------------------------------------- Available Typicals
#
typicals = {
  'P_AinHART': [P_AinHART_Filter, ['AI', 'DI', 'FI', 'LI', 'PDI', 'PI', 'SI', 'TI', 'XI']]
}

#
# --------------------------------------------------------------------------------------------------------- Sheet Variables/Infos - Row & Column Locations
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