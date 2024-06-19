
import vt_vxus_esgv_stuff
from vt_vxus_esgv_stuff import *

VT_minus_VXUS_chart_y_list = []
for holding in VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict.values():
    VT_minus_VXUS_chart_y_list.append(holding['marketValue'])

VT_minus_VXUS_chart_data = {
    'x_value': [],
    'percentage': [],
    'proportion_as_percent': [],
    'funds_in': [],
    'color': [],
    'ticker': [],
    'longName': [],
    'shortName': [],
    'ISIN': [],
    'SEDOL': [],
    'proportion': [],
    'label': []}

iterator_x = 0
from bokeh.palettes import Light3
for holding in VT_minus_VXUS_holdings:
    VT_minus_VXUS_chart_data['x_value'].append(iterator_x + 1)
    VT_minus_VXUS_chart_data['percentage'].append(holding['marketValue'] * 100
                                                  / VT_minus_VXUS_total_market_value)
    VT_minus_VXUS_chart_data['proportion'].append(holding['marketValue']
                                                  / VT_minus_VXUS_total_market_value)
    holding_proportion_as_percent \
        = format(holding['marketValue'] / VT_minus_VXUS_total_market_value,
                ".10%")
    VT_minus_VXUS_chart_data['proportion_as_percent'].append(holding_proportion_as_percent)
    if (holding['isin'], holding['sedol']) in ESGV_ISIN_plus_SEDOL_holding_dict:
        VT_minus_VXUS_chart_data['color'].append(Light3[0])
        VT_minus_VXUS_chart_data['funds_in'].append("Both ESGV and United States holdings of VT")
    else:
        VT_minus_VXUS_chart_data['color'].append(Light3[1])
        VT_minus_VXUS_chart_data['funds_in'].append("Only United States holdings of VT")
    VT_minus_VXUS_chart_data['ticker'].append(holding['ticker'])
    VT_minus_VXUS_chart_data['longName'].append(holding['longName'])
    VT_minus_VXUS_chart_data['shortName'].append(holding['shortName'])
    VT_minus_VXUS_chart_data['ISIN'].append(holding['isin'])
    VT_minus_VXUS_chart_data['SEDOL'].append(holding['sedol'])
    VT_minus_VXUS_chart_data['label'].append(holding['ticker'] + ", " + holding['longName'])
    iterator_x += 1

from bokeh.plotting import figure, show
from bokeh.models import Range1d
p = figure(x_range=Range1d(0,
                           len(VT_minus_VXUS_ISIN_plus_SEDOL_holding_dict.keys()) + 1,
                           bounds="auto"),
           y_range=Range1d(0,
                           max(VT_minus_VXUS_chart_data['percentage']),
                           bounds="auto"),

           #y_axis_type="log",
           title="United States subset of VT holdings vs ESGV holdings",
           toolbar_location="above",
           tools="pan,wheel_zoom,box_zoom,reset,save,box_select",
           active_scroll="wheel_zoom",
           sizing_mode="stretch_both")
p.xaxis.axis_label = "Holding index, sorted by percentage"
p.yaxis.axis_label = "Percentage of holdings"

VT_minus_VXUS_chart_tooltips = \
    [("index", "$index"),
     ("longName", "@longName"),
     ("ticker", "@ticker"),
     ("Funds in", "@funds_in"),
     ("Color", "$swatch:color"),
     #("shortName", "@shortName"),
     ("Percent", "@proportion_as_percent"),
     ("ISIN", "@ISIN"),
     ("SEDOL", "@SEDOL")
     #("Proportion", "@proportion")
     ]

from bokeh.models import HoverTool, WheelZoomTool, CrosshairTool
VT_minus_VXUS_chart_wheel_zoom_tool \
    = WheelZoomTool(
        #renderers = [p],
        maintain_focus = False)
VT_minus_VXUS_chart_crosshair_tool \
    = CrosshairTool()
VT_minus_VXUS_chart_hover_tool \
    = HoverTool(
        tooltips=VT_minus_VXUS_chart_tooltips,
        mode='vline')
p.add_tools(
    VT_minus_VXUS_chart_wheel_zoom_tool,
    VT_minus_VXUS_chart_crosshair_tool,
    VT_minus_VXUS_chart_hover_tool)
p.toolbar.active_scroll = VT_minus_VXUS_chart_wheel_zoom_tool
p.toolbar.active_inspect = [VT_minus_VXUS_chart_hover_tool]

p.vbar(x='x_value',
       top='percentage',
       bottom=0.000000000001, # This is required to be non-zero because of quirks in logscale charts for
                       # the version I'm using at the time of writing, otherwise it would be zero
                       # or not specified (defaults to zero)
       color='color',
       legend_group='funds_in',
       #line_color='gray',
       width=0.9,
       source=VT_minus_VXUS_chart_data)

p.text(x='x_value',
       y=0,
       y_offset=-10,
       text='label',
       angle_units='deg',
       angle=90,
       anchor='left',
       visible=False,
       source=VT_minus_VXUS_chart_data)

from bokeh.models import LabelSet
VT_minus_VXUS_chart_labels = LabelSet(
    x='x_value',
    y='percentage',
    text='label')
p.add_layout(VT_minus_VXUS_chart_labels)

p.legend.click_policy="hide"
p.xgrid.grid_line_color = None
p.y_range.start = 0
show(p)
