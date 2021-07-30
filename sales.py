import pandas
from bokeh.layouts import layout
from bokeh.models.glyphs import Circle
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import curdoc, show
from numpy import source
import pandas
from bokeh.sampledata.iris import flowers
from bokeh.models import Range1d, PanTool, ResetTool, HoverTool, Band, Toggle
from bokeh.models.annotations import Label, LabelSet, Span, BoxAnnotation
from bokeh.models.widgets import Select, Slider, RadioButtonGroup
from bokeh.layouts import gridplot

data = pandas.read_csv("DATA/DATA.csv", sep=",")

data = data.dropna()

data["PREM_DIFF"] = data["SALES REV PREMIUM"]-data["SALES BUDG PREMIUM"]
#data["SALES PROFIT PREMIUM"] = data["SALES PROFIT PREMIUM"].str.replace(",",".").astype(float)
#data["SALES PROFIT ECO"] = data["SALES PROFIT ECO"].str.replace(",",".").astype(float)

Max_val_x = data["SALES REV PREMIUM"].max()
Max_val_x = Max_val_x*1.1
#Max_val_x = Max_val_x.round(decimals=0)
Max_val_x2 = data["SALES REV ECO"].max()
Max_val_x2 = Max_val_x2*1.1
#Max_val_x2 = Max_val_x2.round(decimals=0)

Ave_prof_Prem = data["SALES PROFIT PREMIUM"].mean()
Ave_prof_Prem_hi_band = Ave_prof_Prem*1.2
Ave_prof_Prem_lo_band = Ave_prof_Prem/1.2

Ave_prof_Eco = data["SALES PROFIT ECO"].mean()
Ave_prof_Eco_hi_band = Ave_prof_Eco*1.2
Ave_prof_Eco_lo_band = Ave_prof_Eco/1.2

#For F3 calculations
dealers = data[["REGION", "NUMBER OF DEALERS", "NUMBER OF NEW DEALERS", "NUMBER OF ON-BUDGET DEALERS", "NUMBER OF PERFORMANCE DEALERS"]].copy()
dealers["NUMBER OF NEW DEALERS_magn"] = dealers["NUMBER OF NEW DEALERS"]*10
dealers["NUMBER OF PERFORMANCE DEALERS_magn"] = dealers["NUMBER OF PERFORMANCE DEALERS"]*10
dealers["NUMBER OF DEALERS_magn"] = dealers["NUMBER OF DEALERS"]*2
dealers["NUMBER OF ON-BUDGET DEALERS_magn"] = dealers["NUMBER OF ON-BUDGET DEALERS"]*2

dealers["NEW_TO_TOT_DEALER"] = dealers["NUMBER OF NEW DEALERS"]/dealers["NUMBER OF DEALERS"]
dealers["ONBD_TO_TOT_DEALER"] = dealers["NUMBER OF ON-BUDGET DEALERS"]/dealers["NUMBER OF DEALERS"]
dealers["PERF_TO_TOT_DEALER"] = dealers["NUMBER OF PERFORMANCE DEALERS"]/dealers["NUMBER OF DEALERS"]

#-------- burasını geliştirebiliriz..
dealers["PERF_TO_TOT_DEALER"] = dealers["PERF_TO_TOT_DEALER"]*100
dealers["PERF_TO_TOT_DEALER"] = (dealers["PERF_TO_TOT_DEALER"]).round(decimals=0)
dealers["test_df"] = "%"
dealers["PERF_TO_TOT_DEALER"] = dealers["PERF_TO_TOT_DEALER"].astype(int)
dealers["PERF_TO_TOT_DEALER"] = dealers["PERF_TO_TOT_DEALER"].astype(str)

dealers["PERF_TO_TOT_DEALER_perc"] = dealers["PERF_TO_TOT_DEALER"] + dealers["test_df"]

dealers["ONBD_TO_TOT_DEALER"] = dealers["ONBD_TO_TOT_DEALER"]*100
dealers["ONBD_TO_TOT_DEALER"] = dealers["ONBD_TO_TOT_DEALER"].astype(int)
dealers["ONBD_TO_TOT_DEALER"] = dealers["ONBD_TO_TOT_DEALER"].astype(str)

dealers["ONBD_TO_TOT_DEALER_perc"] = dealers["ONBD_TO_TOT_DEALER"] + dealers["test_df"]


dealers["NEW_TO_TOT_DEALER"] = dealers["NEW_TO_TOT_DEALER"]*100
dealers["NEW_TO_TOT_DEALER"] = dealers["NEW_TO_TOT_DEALER"].astype(int)
dealers["NEW_TO_TOT_DEALER"] = dealers["NEW_TO_TOT_DEALER"].astype(str)

dealers["NEW_TO_TOT_DEALER_perc"] = dealers["NEW_TO_TOT_DEALER"] + dealers["test_df"] 

print(dealers["PERF_TO_TOT_DEALER_perc"])

#Best Performer____________TTTTTTTTTTTTTTTTT
def find_max_performer(df):
    max_val = df.max()
    max_val_index=df.idxmax(axis=0)
    data.iloc[:,0]
    #print(max_val_index)
    #print(data.iloc[max_val_index,0])
    return max_val_index

max_sales_rev_pre_ind = find_max_performer(data["SALES VOLUME PREMIUM"])
max_sales_rev_eco_ind = find_max_performer(data["SALES VOLUME ECO"])
max_sales_rev_prev_period = find_max_performer(data["PREVIOUS CYCLE TOTAL SALES REVENUES"])

#Best Performer____________TTTTTTTTTTTTTTTTT
source = ColumnDataSource(data)
source2 = ColumnDataSource(dealers) #For F3


f = figure(title="aBc cO. - Premium product sales figures across sales experts")
f2 = figure(title="aBc cO. - Eco product sales figures across sales experts")

f.x_range = Range1d(start=500, end=Max_val_x)
f.y_range = Range1d(start=40, end=200)

f.xaxis.axis_label = "Premium product sales revenues and budgets in 000 USD"
f.yaxis.axis_label = "Premium product sales profits in 000 USD"
f.xaxis.axis_label_text_font_size = "10px"
f.yaxis.axis_label_text_font_size = "10px"

f2.x_range = Range1d(start=2000, end=Max_val_x2)
f2.y_range = Range1d(start=40, end=200)

f2.xaxis.axis_label = "Eco product sales revenues and budgets in 000 USD"
f2.yaxis.axis_label = "Eco product sales profits in 000 USD"
f2.xaxis.axis_label_text_font_size = "10px"
f2.yaxis.axis_label_text_font_size = "10px"

f.circle(x="SALES BUDG PREMIUM", y="SALES PROFIT PREMIUM", color="darkblue", 
size= 10, fill_alpha=.4, source=source, legend_label="Budget set by sales expert")
f.circle(x="SALES REV PREMIUM", y="SALES PROFIT PREMIUM", color="orangered", 
size=12, fill_alpha=.4, source=source, legend_label="Actual revenue by sales expert")

f2.square(x="SALES BUDG ECO", y="SALES PROFIT ECO", color="lime", 
size= 10, fill_alpha=.4, source=source, legend_label="Budget set by sales expert")
f2.square(x="SALES REV ECO", y="SALES PROFIT ECO", color="gold", 
size=12, fill_alpha=.4, source=source, legend_label="Actual revenue by sales expert")

labels1=LabelSet(x="SALES BUDG PREMIUM", y="SALES PROFIT PREMIUM", text="REGION", text_font_size="5pt",
    x_offset=-20, y_offset=10, render_mode='canvas', source=source)
f.add_layout(labels1)

labels2=LabelSet(x="SALES BUDG ECO", y="SALES PROFIT ECO", text="REGION", text_font_size="5pt",
    x_offset=-20, y_offset=10, render_mode='canvas', source=source)
f2.add_layout(labels2)

f.legend.location = (300, 10)
f2.legend.location = (300, 10)

#create a box annotation
box_pro_pre = BoxAnnotation(top=Ave_prof_Prem_hi_band, bottom=Ave_prof_Prem_lo_band, 
fill_color="Lime", fill_alpha=0, level="underlay")
f.add_layout(box_pro_pre)

#create a span annotation
span_aver_pro_pre = Span(location=Ave_prof_Prem, dimension='width',
line_color='orange',line_alpha = 0, line_width=1.5, level="underlay")
f.add_layout(span_aver_pro_pre)

#________
description1=Label(x=505,y=Ave_prof_Prem, text=("Average profit: " + str(int(Ave_prof_Prem))),render_mode="css", 
text_font_style="italic", text_font_size="5pt")
f.add_layout(description1)

description2=Label(x=505,y=Ave_prof_Prem_hi_band, text=("Av. Profit +%20: " + str(int(Ave_prof_Prem_hi_band))),render_mode="css", 
text_font_style="italic", text_font_size="5pt")
f.add_layout(description2)

description3=Label(x=505,y=Ave_prof_Prem_lo_band, text=("Av. Profit -%20: " + str(int(Ave_prof_Prem_lo_band))),render_mode="css", 
text_font_style="italic", text_font_size="5pt")
f.add_layout(description3)

description4=Label(x=2005,y=Ave_prof_Eco, text=("Average profit: " + str(int(Ave_prof_Eco))),render_mode="css", 
text_font_style="italic", text_font_size="5pt")
f2.add_layout(description4)

description5=Label(x=2005,y=Ave_prof_Eco_hi_band, text=("Av. Profit +%20: " + str(int(Ave_prof_Eco_hi_band))),render_mode="css", 
text_font_style="italic", text_font_size="5pt")
f2.add_layout(description5)

description6=Label(x=2005,y=Ave_prof_Eco_lo_band, text=("Av. Profit -%20: " + str(int(Ave_prof_Eco_lo_band))),render_mode="css", 
text_font_style="italic", text_font_size="5pt")
f2.add_layout(description6)

#create a box annotation
box_pro_eco = BoxAnnotation(top=Ave_prof_Eco_hi_band, bottom=Ave_prof_Eco_lo_band, 
fill_color="Lime", fill_alpha=0, level="underlay")
f2.add_layout(box_pro_eco)

#create a span annotation
span_aver_pro_eco = Span(location=Ave_prof_Eco, dimension='width',
line_color='orange', line_alpha = 0, line_width=1.5, level="underlay")
f2.add_layout(span_aver_pro_eco)

#______
show_average_decision = 0
def show_average(arg):
    global show_average_decision
    show_average_decision = show_average_decision +1
    span_aver_pro_pre.line_alpha = (show_average_decision%2)
    span_aver_pro_eco.line_alpha = (show_average_decision%2)

show_band_decision = 0
def show_band(arg):
    global show_band_decision
    show_band_decision = show_band_decision +1
    box_pro_eco.fill_alpha = (show_band_decision%2)/10
    box_pro_pre.fill_alpha = (show_band_decision%2)/10


toggle1 = Toggle(label="Switch on the average band", button_type="success", active=True)
toggle1.on_click(show_band)

toggle2 = Toggle(label="Switch on the average value", button_type="success", active=True)
toggle2.on_click(show_average)


#options1 = [("0", "Off"), ("1", "On")]
#select1 = Select(title="Toggle average value", value="1", options = options1)
#select1.on_change("value", show_average)
#select2.on_change("value", show_band)
#options1 = [("0", "Off"), ("1", "On")]
#select1 = Select(title="Toggle average value", value="1", options = options1)


#______
lay_out2 = layout([[toggle1, toggle2]])

lay_out = gridplot([[f,f2]],plot_width=600, plot_height=400)
#show(lay_out)

curdoc().add_root(lay_out)
curdoc().add_root(lay_out2)