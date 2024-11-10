import vt_vxus_esgv_stuff
import vt_vxus_esgv_vti_stuff

from vt_vxus_esgv_stuff \
    import VT_minus_VXUS_holdings \
        as US_holdings_of_VT
from vt_vxus_esgv_vti_stuff \
    import VTI_holdings \
        as VTI_holdings

from vt_vxus_esgv_stuff \
    import VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict \
       as US_holdings_of_VT_uid_dict
from vt_vxus_esgv_vti_stuff \
    import VTI_ISIN_plus_SEDOL_holding_dict \
        as VTI_holdings_uid_dict

US_holdings_of_VT_except_VTI_holdings_dict = dict()
US_holdings_of_VT_intersection_VTI_holdings_dict = dict()
for key in US_holdings_of_VT_uid_dict:
    if key in VTI_holdings_uid_dict:
        US_holdings_of_VT_intersection_VTI_holdings_dict[key] = US_holdings_of_VT_uid_dict[key]
    else:
        US_holdings_of_VT_except_VTI_holdings_dict[key] = US_holdings_of_VT_uid_dict[key]
US_holdings_of_VT_except_VTI_holdings = US_holdings_of_VT_except_VTI_holdings_dict.values()
US_holdings_of_VT_intersection_VTI_holdings = US_holdings_of_VT_intersection_VTI_holdings_dict.values()

VTI_holdings_except_US_holdings_of_VT_dict = dict()
VTI_holdings_intersection_US_holdings_of_VT_dict = dict()
US_holdings_of_VT_intersection_VTI_holdings_dict = dict()
for key in VTI_holdings_uid_dict:
    if key in US_holdings_of_VT_uid_dict:
        VTI_holdings_intersection_US_holdings_of_VT_dict[key] = VTI_holdings_uid_dict[key]
    else:
        VTI_holdings_except_US_holdings_of_VT_dict[key] = VTI_holdings_uid_dict[key]
VTI_holdings_except_US_holdings_of_VT = VTI_holdings_except_US_holdings_of_VT_dict.values()
VTI_holdings_intersection_US_holdings_of_VT = VTI_holdings_intersection_US_holdings_of_VT_dict.values()


#print("Number of holdings in US holdings of VT but not VTI:", #len(US_holdings_of_VT_except_VTI_holdings_dict))
