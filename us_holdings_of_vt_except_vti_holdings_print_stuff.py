import us_holdings_of_vt_except_vti_holdings

from us_holdings_of_vt_except_vti_holdings \
    import US_holdings_of_VT_uid_dict \
        as US_holdings_of_VT_uid_dict

from us_holdings_of_vt_except_vti_holdings \
    import US_holdings_of_VT_except_VTI_holdings \
        as US_holdings_of_VT_except_VTI_holdings

print("Number of holdings in US holdings of VT but not VTI:", len(US_holdings_of_VT_except_VTI_holdings))
print()

for holding in US_holdings_of_VT_except_VTI_holdings:
    print(holding["longName"] + ",",
          holding["ticker"])
