import vt_vxus_esgv_stuff
from vt_vxus_esgv_stuff import *

# Print various info about VT, VXUS, or ESGV
## Print info about duplicate entries
def print_duplicate_entries(duplicate_entries, identifier_type, limit_printed_duplicates=True):
    #print("  " + identifier_type + ":", identifier)

    def print_holding(holding):
      print("    Ticker:",      "\"" + holding['ticker']           + "\"",
            "\"marketValue\":", "\"" + str(holding['marketValue']) + "\"",
            "\"longName\":",    "\"" + holding['longName']         + "\"",
            "ISIN:",            "\"" + holding['isin']             + "\"",
            "SEDOL:",           "\"" + holding['sedol']            + "\"")

    def print_holding_list(holding_list, limit_printed_duplicates):
        if limit_printed_duplicates and len(holding_list) > 3:
            start_section = holding_list[:2]
            for holding in start_section:
                print_holding(holding)

            middle_section_length = len(holding_list) - 3
            if middle_section_length == 1:
                print("    ...", 1, "more holding not shown", "...")
            else:
                print("    ...", middle_section_length, "more holdings not shown", "...")

            end_section = holding_list[-1:]
            for holding in end_section:
                print_holding(holding)
        else:
            for holding in holding_list:
                print_holding(holding)

    def print_duplicate_entry(holding_list, identifier_type, identifier,
                              limit_printed_duplicates):
        print("  " + identifier_type + ": \"" + identifier + "\",",
              "Count:", len(holding_list))
        print_holding_list(holding_list, limit_printed_duplicates)

    if limit_printed_duplicates and len(duplicate_entries) > 3:
        start_section_keys = list(duplicate_entries.keys())[:2]
        for identifier in start_section_keys:
            print_duplicate_entry(duplicate_entries[identifier],
                                  identifier_type,
                                  identifier,
                                  limit_printed_duplicates)

        middle_section_length = len(duplicate_entries) - 3
        if middle_section_length == 1:
            print("  ...", 1, "more identifier not shown", "...")
        else:
            print("  ...", middle_section_length, "more identifiers not shown", "...")

        end_section_keys = list(duplicate_entries.keys())[-1:]
        for identifier in end_section_keys:
            print_duplicate_entry(duplicate_entries[identifier],
                                  identifier_type,
                                  identifier,
                                  limit_printed_duplicates)
    else:
        for identifier in duplicate_entries.keys():
            print_duplicate_entry(duplicate_entries[identifier],
                                  identifier_type,
                                  identifier,
                                  limit_printed_duplicates)
    print()

def print_fund_stuff(fund_ticker, fund_holdings, fund_identifiers, fund_duplicates):
    print("#", fund_ticker, "section")
    print("Number of holdings:", len(fund_holdings))
    print("Number of unique ISINs:", len(fund_identifiers['ISINs']))
    print("Number of unique SEDOLs:", len(fund_identifiers['SEDOLs']))
    print("Number of unique tickers:", len(fund_identifiers['tickers']))
    print("Number of unique \"longName\"s:", len(fund_identifiers['longNames']))
    print("Number of unique \"shortName\"s:", len(fund_identifiers['shortNames']))
    print()
    print("## Holdings with duplicate identifiers in", fund_ticker)
    print ("### Number of duplicate ISINs:", len(list(fund_duplicates['ISIN'])))
    print("Duplicate ISINs:")
    print_duplicate_entries(fund_duplicates['ISIN'], "ISIN")
    print ("### Number of duplicate SEDOLs:", len(list(fund_duplicates['SEDOL'])))
    print("Duplicate SEDOLs:")
    print_duplicate_entries(fund_duplicates['SEDOL'], "SEDOL")
    print("### Number of duplicate tickers:", len(list(fund_duplicates['ticker'])))
    print("Duplicate tickers:")
    print_duplicate_entries(fund_duplicates['ticker'], "ticker")
    print("### Number of duplicate \"longName\"s:", len(list(fund_duplicates['longName'])))
    print("Duplicate \"longName\"s:")
    print_duplicate_entries(fund_duplicates['longName'], "longName")
    print("### Number of duplicate \"shortName\"s:", len(list(fund_duplicates['shortName'])))
    print("Duplicate \"shortName\"s:")
    print_duplicate_entries(fund_duplicates['shortName'], "shortName")

#print_fund_stuff("VT", VT_holdings, VT_identifiers, VT_duplicates)
#print_fund_stuff("VXUS", VXUS_holdings, VXUS_identifiers, VXUS_duplicates)

VT_total_market_value = total_value_by_key(VT_holdings, 'marketValue')
VT_total_notional_value = total_value_by_key(VT_holdings, 'notionalValue')
VT_total_percent_weight = total_value_by_key(VT_holdings, 'percentWeight')
# print(VT_total_percent_weight)

#print("VT total market value:", VT_total_market_value)
#print("VT total notional value:", VT_total_notional_value)

#print("VT minus VXUS holdings:", len(VT_minus_VXUS_SEDOLs))
#print("VT minus VXUS total market value: ", VT_minus_VXUS_total_market_value)

#print_fund_stuff('ESGV', ESGV_holdings, ESGV_identifiers, ESGV_duplicates)
#ESGV_total_percent_weight = total_value_by_key(ESGV_holdings, 'percentWeight')
#print(ESGV_total_percent_weight)

#print("Is VT minus VXUS a superset of ESGV?",
#      VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict.keys() > ESGV_ISIN_plus_SEDOL_holding_dict.keys())

# print(len(ESGV_VT_minus_VXUS_key_difference))
# print(ESGV_VT_minus_VXUS_key_difference)
