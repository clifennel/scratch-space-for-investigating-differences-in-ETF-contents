# Requires "import vt_vxus_esgv_vti_stuff" and "import vt_vxus_esgv_stuff"

import vt_vxus_esgv_vti_stuff
import vt_vxus_esgv_stuff

# For VTI vs VT US holdings vs ESGV
chart_data = {
    'x_value': [],
    'percentage': [],
    'proportion_as_percent_for_tooltip': [],
    'proportion': [],
    'funds_in': [],
    'color': [],
    'ticker': [],
    'longName': [],
    'shortName': [],
    'ISIN': [],
    'SEDOL': [],
    'label': []}

from vt_vxus_esgv_vti_stuff import VTI_holdings, \
                                   VTI_stock_total_market_value, \
                                   VTI_ISIN_plus_SEDOL_holding_dict

from vt_vxus_esgv_stuff     import VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict \
                                     as VT_US_holdings_ISIN_plus_SEDOL_holding_dict, \
                                   ESGV_ISIN_plus_SEDOL_holding_dict


iterator_x = 1
from bokeh.palettes import Light3
for holding in VTI_holdings:
    chart_data['x_value'].append(iterator_x)
    chart_data['percentage'].append(holding['marketValue'] * 100
                                    / VTI_stock_total_market_value)
    chart_data['proportion'].append(holding['marketValue']
                                    / VTI_stock_total_market_value)
    holding_proportion_as_percent_for_tooltip \
        = format(holding['marketValue'] / VTI_stock_total_market_value, ".10%")
    chart_data['proportion_as_percent_for_tooltip'].append( \
        holding_proportion_as_percent_for_tooltip)
    if (holding['isin'], holding['sedol']) in ESGV_ISIN_plus_SEDOL_holding_dict:
        chart_data['color'].append(Light3[0])
        chart_data['funds_in'].append("ESGV, United States holdings of VT, and VTI")
    elif (holding['isin'], holding['sedol']) in VT_US_holdings_ISIN_plus_SEDOL_holding_dict:
        chart_data['color'].append(Light3[1])
        chart_data['funds_in'].append("United States holdings of VT and VTI")
    else:
        chart_data['color'].append(Light3[2])
        chart_data['funds_in'].append("Only VTI")
    chart_data['ticker'].append(holding['ticker'])
    chart_data['longName'].append(holding['longName'])
    chart_data['shortName'].append(holding['shortName'])
    chart_data['ISIN'].append(holding['isin'])
    chart_data['SEDOL'].append(holding['sedol'])
    chart_data['label'].append(holding['ticker'] + ", " + holding['longName'])
    iterator_x += 1

from bokeh.plotting import figure, show
from bokeh.models import Range1d
p = figure(x_range=Range1d(0,
                           len(VTI_ISIN_plus_SEDOL_holding_dict.keys()) + 1,
                           bounds="auto"),
           y_range=Range1d(0,
                           max(chart_data['percentage']),
                           bounds="auto"),

           #y_axis_type="log",
           title="Holdings for ESGV vs United States subset of VT vs VTI",
           toolbar_location="above",
           tools="pan,wheel_zoom,box_zoom,reset,save,box_select",
           active_scroll="wheel_zoom",
           sizing_mode="stretch_both")
p.xaxis.axis_label = "Holding number, sorted by percentage"
p.yaxis.axis_label = "Percentage of stock holdings in VTI"

chart_tooltips = \
    [("index", "$index"),
     ("longName", "@longName"),
     ("ticker", "@ticker"),
     ("Funds in", "@funds_in"),
     ("Color", "$swatch:color"),
     #("shortName", "@shortName"),
     ("Percent", "@proportion_as_percent_for_tooltip"),
     ("ISIN", "@ISIN"),
     ("SEDOL", "@SEDOL")
     #("Proportion", "@proportion")
     ]

from bokeh.models import HoverTool, WheelZoomTool, CrosshairTool
chart_wheel_zoom_tool \
    = WheelZoomTool(
        #renderers = [p],
        maintain_focus = False)
chart_crosshair_tool \
    = CrosshairTool()
chart_hover_tool \
    = HoverTool(
        tooltips=chart_tooltips,
        mode='vline')
p.add_tools(
    chart_wheel_zoom_tool,
    chart_crosshair_tool,
    chart_hover_tool)
p.toolbar.active_scroll = chart_wheel_zoom_tool
p.toolbar.active_inspect = [chart_hover_tool]

p.vbar(x='x_value',
       top='percentage',
       bottom=0.000000000001, # This is required to be non-zero because of quirks in logscale charts for
                       # the version I'm using at the time of writing, otherwise it would be zero
                       # or not specified (defaults to zero)
       color='color',
       legend_group='funds_in',
       #line_color='gray',
       width=0.9,
       source=chart_data)

p.text(x='x_value',
       y=0,
       y_offset=-10,
       text='label',
       angle_units='deg',
       angle=90,
       anchor='left',
       visible=False,
       source=chart_data)

from bokeh.models import LabelSet
chart_labels = LabelSet(
    x='x_value',
    y='percentage',
    text='label')
p.add_layout(chart_labels)

p.legend.click_policy="hide"
p.xgrid.grid_line_color = None
p.y_range.start = 0
show(p)
