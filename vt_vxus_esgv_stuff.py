# Set paths to files here
path_VT = "vt-stock.json" # Path to JSON file for VT
path_VXUS = "vxus-stock.json" # Path to JSON file for VXUS
path_ESGV = "esgv-stock-2024-06-13.json" # Path to JSON file for ESGV

# Logic to load JSON files for VT and VXUS as JSON objects using paths specified in `path_VT` and
# `path_VXUS`, respectively
#   See here for JSON to Python object conversion table:
#   [JSON to Python object table](https://docs.python.org/3/library/json.html#json-to-py-table)

## Open VT and VXUS as file pointer
file_VT = open(path_VT, 'r') # File pointer for VT
file_VXUS = open(path_VXUS, 'r') # File pointer for VXUS

## Load JSON files as Python objects
import json # Import JSON parser
VT_raw = json.load(file_VT)
VXUS_raw = json.load(file_VXUS)

# Logic to compile the following information from each of VT and VXUS files:
#   For each of the following identifiers: ISIN, SEDOL, "longName", and "shortName"
#   Set of the identifier
#   Duplicate stocks represented by a dict where the key is the duplicate identifier and the
#     value is a list of duplicate stocks sharing that duplicate identifier
#   Output in VT_identifiers and VT_duplicates, see description of
#   get_identifiers() and
#   get_duplicates()
#   for description of respective formats

## Compiles sets of the unique ISINs, SEDOLs, "longName"s, "shortName"s, and tickers for a
## holding list
def get_identifiers(holding_list):
    ISIN_set = set()
    SEDOL_set = set()
    ticker_set = set()
    longName_set = set()
    shortName_set = set()
    for holding_entry in holding_list:
        ISIN_set.add(holding_entry['isin'])
        SEDOL_set.add(holding_entry['sedol'])
        ticker_set.add(holding_entry['ticker'])
        longName_set.add(holding_entry['longName'])
        shortName_set.add(holding_entry['shortName'])
    return {'ISINs': ISIN_set,
            'SEDOLs': SEDOL_set,
            'tickers': ticker_set,
            'longNames': longName_set,
            'shortNames': shortName_set}

## Compiles holdings with duplicate ISINs, SEDOLs, "longName"s, "shortName"s, and tickers for a
## holding list
## Input: List of holdings as an argument, format should match that of the list found at
##        JSON.parse(stock.json).fund.entity where stock.json is the source file downloaded from
##        Vanguard
##        This function reads from the following fields of each individual entry on the list:
##          (key)        (description of value)  (example)
##          'isin'       ISIN                    "US5949181045"
##          'sedol'      SEDOL                   "2588173"
##          'ticker'     ticker                  "MSFT"
##          'longName'   longer name             "Microsoft Corp."
##          'shortName'  shorter name            "MICROSOFT CORP"
## Output: Returns array containing for each of the following identifiers:
##          ISIN, SEDOL, ticker, "longName", "shortName":
##         Each duplicate holding entry from the input holding list (holding_list) as a dictionary
##         where the key is the duplicate identifier and the value is the holding entries with the
##         the same identifier as the duplicate identifier used as a key
##         Format of the dict:
##           Keys are these identifiers: 'isin', 'sedol', 'ticker', 'longName', 'shortName'
##           Values are a dict where the key is the specific duplicate identifier in question and
##           the value is a list of holding entries sharing that duplicate identifier.
def get_duplicates(holding_list):
    ### Logic to build sets of identifiers with duplicates for each identifier type
    ### Input: holding_list
    ### Output: ISIN_duplicates, SEDOL_duplicates, ticker_duplicates, longName_duplicates,
    ###         shortName_duplicates
    ISIN_set = set()
    ISIN_duplicates = set()
    SEDOL_set = set()
    SEDOL_duplicates = set()
    ticker_set = set()
    ticker_duplicates = set()
    longName_set = set()
    longName_duplicates = set()
    shortName_set = set()
    shortName_duplicates = set()
    for holding_entry in holding_list:
        if 'longName' not in holding_entry:
            print("missing longName")
            print(holding_entry)

        if holding_entry['isin'] in ISIN_set:
            ISIN_duplicates.add(holding_entry['isin'])
        if holding_entry['sedol'] in SEDOL_set:
            SEDOL_duplicates.add(holding_entry['sedol'])
        if holding_entry['ticker'] in ticker_set:
            ticker_duplicates.add(holding_entry['ticker'])
        if holding_entry['longName'] in longName_set:
            longName_duplicates.add(holding_entry['longName'])
        if holding_entry['shortName'] in shortName_set:
            shortName_duplicates.add(holding_entry['shortName'])

        ISIN_set.add(holding_entry["isin"])
        SEDOL_set.add(holding_entry["sedol"])
        ticker_set.add(holding_entry['ticker'])
        longName_set.add(holding_entry['longName'])
        shortName_set.add(holding_entry['shortName'])

    ### Logic to build dict of duplicate holdings lists for each identifier
    from collections import defaultdict # This import provides defaultdict(list) objects which are
                                        # dict-like objects that have a default of `[]` instead of
                                        # `None` in values of key-value pairs, which enables this
                                        # program to safely append to values of k/v pairs without
                                        # logic to supply an empty list when the value is `None`
    holding_entries_with_duplicate_ISINs = defaultdict(list)
    holding_entries_with_duplicate_SEDOLs = defaultdict(list)
    holding_entries_with_duplicate_tickers = defaultdict(list)
    holding_entries_with_duplicate_longNames = defaultdict(list)
    holding_entries_with_duplicate_shortNames = defaultdict(list)
    for holding_entry in holding_list:
        if holding_entry['isin'] in ISIN_duplicates:
            holding_entries_with_duplicate_ISINs[holding_entry['isin']].append(holding_entry)
        if holding_entry['sedol'] in SEDOL_duplicates:
            holding_entries_with_duplicate_SEDOLs[holding_entry['sedol']].append(holding_entry)
        if holding_entry['ticker'] in ticker_duplicates:
            holding_entries_with_duplicate_tickers[holding_entry['ticker']].append(holding_entry)
        if holding_entry['longName'] in longName_duplicates:
            holding_entries_with_duplicate_longNames[holding_entry['longName']].append(holding_entry)
        if holding_entry['shortName'] in shortName_duplicates:
            holding_entries_with_duplicate_shortNames[holding_entry['shortName']].append(holding_entry)

    ### Assemble and return dict
    return {'ISIN': holding_entries_with_duplicate_ISINs,
            'SEDOL': holding_entries_with_duplicate_SEDOLs,
            'ticker': holding_entries_with_duplicate_tickers,
            'longName': holding_entries_with_duplicate_longNames,
            'shortName': holding_entries_with_duplicate_shortNames}

VT_holdings = VT_raw['fund']['entity']

VT_identifiers = get_identifiers(VT_holdings)
VT_duplicates \
  = get_duplicates(VT_holdings)

VXUS_holdings = VXUS_raw['fund']['entity']
VXUS_identifiers = get_identifiers(VXUS_holdings)
VXUS_duplicates \
  = get_duplicates(VXUS_holdings)

# ~~Print various info about both VT and VXUS~~
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

def total_value_by_key(holding_list, value_key):
    total_value = 0
    for holding in holding_list:
        if 'marketValue' not in holding:
            print(holding['ticker'], "has no", value_key)
        elif holding[value_key] == '':
            print(holding['ticker'], "has empty", value_key)
        elif holding[value_key] == "0":
            #print(holding['ticker'], "has", value_key, "of 0")
            pass
        else:
            total_value += float(holding[value_key])
    return total_value

#VT_total_market_value = total_value_by_key(VT_holdings, 'marketValue')
#VT_total_notional_value = total_value_by_key(VT_holdings, 'notionalValue')
#print("VT total market value:", VT_total_market_value)
#print("VT total notional value:", VT_total_notional_value)
#VT_total_percent_weight = total_value_by_key(VT_holdings, 'percentWeight')
#print(VT_total_percent_weight)

VT_minus_VXUS_SEDOLs = VT_identifiers['SEDOLs'].difference(VXUS_identifiers['SEDOLs'])
VT_minus_VXUS_holdings_by_SEDOL = dict()
VT_minus_VXUS_holdings = []
for holding in VT_holdings:
    if holding['sedol'] in VT_minus_VXUS_SEDOLs:
        VT_minus_VXUS_holdings_by_SEDOL[holding['sedol']] = holding
        VT_minus_VXUS_holdings.append(holding)
#print("VT minus VXUS holdings:", len(VT_minus_VXUS_SEDOLs))

VT_minus_VXUS_total_market_value = total_value_by_key(VT_minus_VXUS_holdings, 'marketValue')
#print("VT minus VXUS total market value: ", VT_minus_VXUS_total_market_value)

file_ESGV = open(path_ESGV, 'r') # File pointer for ESGV
ESGV_raw = json.load(file_ESGV)
ESGV_holdings = ESGV_raw['fund']['entity']
ESGV_identifiers = get_identifiers(ESGV_holdings)
ESGV_duplicates \
  = get_duplicates(ESGV_holdings)
#print_fund_stuff('ESGV', ESGV_holdings, ESGV_identifiers, ESGV_duplicates)
#ESGV_total_percent_weight = total_value_by_key(ESGV_holdings, 'percentWeight')
#print(ESGV_total_percent_weight)


VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict = dict()
for holding in VT_minus_VXUS_holdings:
    VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict[holding['isin'], holding['sedol']] \
        = holding

ESGV_ISIN_plus_SEDOL_holding_dict = dict()
for holding in ESGV_holdings:
    ESGV_ISIN_plus_SEDOL_holding_dict[holding['isin'], holding['sedol']] \
        = holding

#print("Is VT minus VXUS a superset of ESGV?",
#      VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict.keys() > ESGV_ISIN_plus_SEDOL_holding_dict.keys())
ESGV_VT_minus_VXUS_key_difference = \
    ESGV_ISIN_plus_SEDOL_holding_dict.keys() - VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict.keys()
#print(len(ESGV_VT_minus_VXUS_key_difference))
#print(ESGV_VT_minus_VXUS_key_difference)
