from assets.filtering.P_AinHART import *

#
# Available Safety Areas
#
safetyAreas = {
  '+H06': 'Distn'
}

#
# Available Typicals
#
typicals = {
  'P_AinHART': [P_AinHART_Filter, ['AI', 'DI', 'FI', 'LI', 'PDI', 'PI', 'SI', 'TI', 'XI']]
}

#
# Sheet Row & Column Locations
#
firstRow  = 8
pidColumn = 3