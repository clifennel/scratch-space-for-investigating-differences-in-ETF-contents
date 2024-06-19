# Requires "import vt_vxus_esgv_stuff"

# Set path to file here
path_VTI = "vti-stock.json"

file_VTI = open(path_VTI, 'r')

import json
VTI_holdings = json.load(file_VTI)['fund']['entity']

import vt_vxus_esgv_stuff
import vt_vxus_esgv_print_stuff
VTI_identifiers = vt_vxus_esgv_stuff.get_identifiers(VTI_holdings)
VTI_duplicates = vt_vxus_esgv_stuff.get_duplicates(VTI_holdings)

vt_vxus_esgv_print_stuff.print_fund_stuff("VTI", VTI_holdings, VTI_identifiers, VTI_duplicates)
