# Requires "import vt_vxus_esgv_stuff" and "import vt_vxus_esgv_print_stuff"

# Set path to file here
path_VTI = "vti-stock.json"

file_VTI = open(path_VTI, 'r')

import json
VTI_holdings = json.load(file_VTI)['fund']['entity']

import vt_vxus_esgv_stuff
import vt_vxus_esgv_print_stuff
VTI_identifiers = vt_vxus_esgv_stuff.get_identifiers(VTI_holdings)
VTI_duplicates = vt_vxus_esgv_stuff.get_duplicates(VTI_holdings)
VTI_stock_total_market_value \
    = vt_vxus_esgv_stuff.total_value_by_key(VTI_holdings, 'marketValue')

VTI_ISIN_plus_SEDOL_holding_dict = dict()
for holding in VTI_holdings:
    VTI_ISIN_plus_SEDOL_holding_dict[holding['isin'], holding['sedol']] \
        = holding

#vt_vxus_esgv_print_stuff.print_fund_stuff("VTI", VTI_holdings, VTI_identifiers, VTI_duplicates)

from vt_vxus_esgv_stuff     import VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict \
                                     as VT_US_holdings_ISIN_plus_SEDOL_holding_dict

VT_US_holdings_VTI_key_difference = \
    VT_US_holdings_ISIN_plus_SEDOL_holding_dict.keys() - VTI_ISIN_plus_SEDOL_holding_dict.keys()

# print(len(VT_US_holdings_VTI_key_difference))
# print(VT_US_holdings_VTI_key_difference)

VTI_VT_US_holdings_key_difference = \
    VTI_ISIN_plus_SEDOL_holding_dict.keys() - VT_US_holdings_ISIN_plus_SEDOL_holding_dict.keys()

# print(len(VTI_VT_US_holdings_key_difference))
# print(VTI_VT_US_holdings_key_difference)

#for key in VT_US_holdings_VTI_key_difference:
#    if VT_US_holdings_ISIN_plus_SEDOL_holding_dict[key]['ticker'] == '':
#        print("<empty ticker>")
#    else:
#        print(VT_US_holdings_ISIN_plus_SEDOL_holding_dict[key]['ticker'])
#    print(" ", VT_US_holdings_ISIN_plus_SEDOL_holding_dict[key]['longName'])
#    print(" ", key)
