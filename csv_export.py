import vt_vxus_esgv_stuff
import csv

field_names = ['index', 'ticker', 'longName', 'percent', 'funds_in']
csv_file_to_write_to = open('VT_minus_VXUS_vs_ESGV_stuff.csv', 'w', newline='')
writer = csv.DictWriter(csv_file_to_write_to, fieldnames = field_names)
writer.writeheader()

holdings = vt_vxus_esgv_stuff.VT_minus_VXUS_holdings
total_market_value = vt_vxus_esgv_stuff.VT_minus_VXUS_total_market_value

iterator = 1
for holding in holdings:
    ESGV_ISIN_plus_SEDOL_holding_dict = vt_vxus_esgv_stuff.ESGV_ISIN_plus_SEDOL_holding_dict
    if (holding['isin'], holding['sedol']) in ESGV_ISIN_plus_SEDOL_holding_dict:
        funds_in = "Both_ESGV_and_VT_minus_VXUS"
    else:
        funds_in = "VT_minus_VXUS_only"

    writer.writerow({
        'index': iterator,
        'ticker': holding['ticker'],
        'longName': holding['longName'],
        'percent': format(holding['marketValue'] / total_market_value, ".12%"),
        'funds_in': funds_in})
    iterator += 1

csv_file_to_write_to.close()
