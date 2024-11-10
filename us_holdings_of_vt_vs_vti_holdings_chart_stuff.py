import vt_vxus_esgv_vti_stuff
import vt_vxus_esgv_stuff

from vt_vxus_esgv_vti_stuff import VTI_holdings

from us_holdings_of_vt_except_vti_holdings \
    import US_holdings_of_VT_except_VTI_holdings \
        as US_holdings_of_VT_except_VTI_holdings
from us_holdings_of_vt_except_vti_holdings \
    import US_holdings_of_VT_intersection_VTI_holdings \
        as US_holdings_of_VT_intersection_VTI_holdings
from us_holdings_of_vt_except_vti_holdings \
    import VTI_holdings_intersection_US_holdings_of_VT \
        as VTI_holdings_intersection_US_holdings_of_VT
from us_holdings_of_vt_except_vti_holdings \
    import VTI_holdings_except_US_holdings_of_VT \
        as VTI_holdings_except_US_holdings_of_VT

from us_holdings_of_vt_except_vti_holdings \
    import US_holdings_of_VT_except_VTI_holdings_dict \
        as US_holdings_of_VT_except_VTI_holdings_dict
from us_holdings_of_vt_except_vti_holdings \
    import US_holdings_of_VT_intersection_VTI_holdings_dict \
        as US_holdings_of_VT_intersection_VTI_holdings_dict
from us_holdings_of_vt_except_vti_holdings \
    import VTI_holdings_intersection_US_holdings_of_VT_dict \
        as VTI_holdings_intersection_US_holdings_of_VT_dict
from us_holdings_of_vt_except_vti_holdings \
    import VTI_holdings_except_US_holdings_of_VT_dict \
        as VTI_holdings_except_US_holdings_of_VT_dict

US_holdings_of_VT_intersection_VTI_value = 0
for holding in US_holdings_of_VT_intersection_VTI_holdings:
    US_holdings_of_VT_intersection_VTI_value += holding['marketValue']
#print(US_holdings_of_VT_intersection_VTI_value)

VTI_holdings_intersection_US_holdings_of_VT_value = 0
for holding in VTI_holdings_intersection_US_holdings_of_VT:
    VTI_holdings_intersection_US_holdings_of_VT_value += holding['marketValue']
#print(VTI_holdings_intersection_US_holdings_of_VT_value)

ratio_between_VTI_holdings_and_US_holdings_of_VT = VTI_holdings_intersection_US_holdings_of_VT_value / US_holdings_of_VT_intersection_VTI_value

US_holdings_of_VT_except_VTI_holdings_scaled = list()
for holding in US_holdings_of_VT_except_VTI_holdings:
    temp_dict = holding.copy()
    temp_dict['marketValue'] = temp_dict['marketValue'] * ratio_between_VTI_holdings_and_US_holdings_of_VT
    US_holdings_of_VT_except_VTI_holdings_scaled.append(temp_dict)

fused_holdings = US_holdings_of_VT_except_VTI_holdings_scaled + VTI_holdings
fused_holdings.sort(key=lambda s: s['marketValue'], reverse=True)
#print(fused_holdings)

fused_total = 0
for holding in fused_holdings:
    fused_total += holding['marketValue']

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

iterator_x = 1
from bokeh.palettes import Light3
for holding in fused_holdings:
    chart_data['x_value'].append(iterator_x)
    #chart_data['percentage'].append(holding['marketValue'] * 100
    #                                / fused_total)
    chart_data['percentage'].append(100)
    chart_data['proportion'].append(holding['marketValue']
                                    / fused_total)
    holding_proportion_as_percent_for_tooltip \
        = format(holding['marketValue'] / fused_total, ".10%")
    chart_data['proportion_as_percent_for_tooltip'].append( \
        holding_proportion_as_percent_for_tooltip)
    if (holding['isin'], holding['sedol']) in US_holdings_of_VT_except_VTI_holdings_dict:
        chart_data['color'].append(Light3[0])
        chart_data['funds_in'].append("Only United States holdings of VT")
    elif (holding['isin'], holding['sedol']) in VTI_holdings_intersection_US_holdings_of_VT_dict:
        chart_data['color'].append(Light3[1])
        chart_data['funds_in'].append("United States holdings of VT and holdings of VTI")
    else:
        chart_data['color'].append(Light3[2])
        chart_data['funds_in'].append("Only holdings of VTI")
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
                           len(fused_holdings) + 1,
                           bounds="auto"),
           y_range=Range1d(0,
                           max(chart_data['percentage']),
                           bounds="auto"),

           #y_axis_type="log",
           title="Holdings for United States subset of VT vs VTI",
           toolbar_location="above",
           tools="pan,wheel_zoom,box_zoom,reset,save,box_select",
           active_scroll="wheel_zoom",
           sizing_mode="stretch_both")
p.xaxis.axis_label = "Holding number, sorted by percentage"
p.yaxis.axis_label = "Percentage of stock holdings in combined holding set"
#p.yaxis.axis_label = "ignore this axis"


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
