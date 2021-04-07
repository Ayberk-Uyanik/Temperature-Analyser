# Importing the necessary libraries
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import math

# Application building codes
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

button_style = {
    "textAlign": "center",
    "backgroundColor": "#3283FE",
    "color": "#E2E2E2",
    "display": "inline-block"
}

colours = ["black", "red", "blue", "green", "orange", "yellow", "brown", "purple", "magenta", "goldenrod"]

# Lists for pre-drill prediction #
md_predict = []
tvd_predict = []
tvdss_predict = []
temp_predict90 = []
temp_predict50 = []
temp_predict10 = []

# Lists for post-drill prediction #
md_list = []
bht_list = []
tvd_list = []
tvdss_list = []
aapg_f = []
aapg_c = []
harr_f = []
harr_c = []
grad_aapg = []
grad_harr = []

# Shared Lists #
region_depths = {
    "Onshore":["TVDkb (m.)", "TVDgl (m.)"],
    "Offshore":["TVDbml (m.)"]
}

depth_types = ["Measured Depth - MD(m.)", "True Vertical Depth below sea level - TVDss (m.)",
               "True Vertical Depth below mudline - TVDbml (m.)"]

# Lists for helpful calculations #
conversion_types = ["Meters to Feet", "Feet to Meters", "Fahrenheit to Celsius", "Celsius to Fahrenheit",
                    "Meters to Miles", "Miles to Meters", "Meters to Yards", "Yards to Meters",
                    "Fahrenheit to Kelvin", "Kelvin to Fahrenheit", "Celsius to Kelvin", "Kelvin to Celsius"]

# App Layout Codes #
app = dash.Dash (__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div ([
        html.Label("Temperature Analyser v1.0", style={"font-size": "22px", "font-weight": "bold", "color":"black", "display":"inline-block"}),
        html.A ("GitHub Repository", href="https://github.com/Ayberk-Uyanik/Temperature-Analyser", style=        {"text-decoration":"none",
                                                                                                       "color":"black",
                                                                                                       "margin-left":"50em",
                                                                                                       "font-weight":"bold"})
    ], style={"display":"flex", "background-color":"inherit", "align-items":"center", "align-content":"space-between", "height":"50px"}),

    html.H2("Hi there!", style={"textAlign": "left", "font-size": "18px", "font-weight": "bold"}),
    html.P("Welcome to the Temperature Analyser v1.0! This application helps you to assess pre&post drill temperature conditions for vertical exploration wells."),
    html.Hr(),

    dcc.Tabs([
        dcc.Tab(label="Well registration", children=[
            html.Br(),
            html.Div(className="flex-container", children=[
                html.Label("Well Name:", style={"font-weight": "bold"}),
                dcc.Input(value="Well-1", id="Well_name", style={"width": "10%", "padding-left":"3%", "margin-left":"1em"}),

                html.Label("Well Region:", style={"font-weight": "bold", "padding-left":"10%"}),
                dcc.RadioItems(id="regions",
                               options=[{"label": "Onshore", "value": "Onshore"},
                                        {"label": "Offshore", "value": "Offshore"}],
                               value="Onshore",
                               labelStyle={"display": "inline-block"},
                               style={"margin-left":"0.5em"}),

                html.Label("Kelly Bushing Level (m.):", style={"font-weight": "bold", "padding-left":"10%"}),
                dcc.Input(id="KB", type="number", value=0, style={"textAlign": "center", "width": "10%", "margin-left":"1em"})

            ], style={"display":"flex", "flex-direction":"row", "align-content":"space-between",
                      "justify-content":"flex-start", "align-items":"center"}),

            html.Br(),
            html.Div(className="flex-container", children=[
                html.Label("Ground Level / Water Depth (m.):", style={"font-weight": "bold"}),
                dcc.Input(id="GL", type="number", value=0, style={"textAlign": "center", "width": "10%", "margin-left":"1em"}),

                html.Label((["Mean Annual Surface/Sea Floor Temperature", "", "(", html.Sup("o"), "C)"]), id="mast_id",
                                                           style={"font-weight": "bold", "padding-left":"3%"}),
                dcc.Input(type="number", value=0, id="mast_prediction", style={"textAlign": "center", "width": "10%",
                                                                               "margin-left":"1em"}),
                dcc.ConfirmDialogProvider (children=[html.Button ("Input Check", style={"margin-left":"23em","textAlign":"center",
                                                                                        "backgroundColor":"#3283FE", "color":"#E2E2E2"})],
                                           id="confirm_registration",
                                           message="Welcome!"),
            ], style={"display":"flex", "flex-direction":"row", "flex-wrap":"wrap", "align-content":"space-between",
                      "align-self":"center", "margin-bottom":"2em", "align-items":"center"}),
        ]),

        dcc.Tab(label="Pre-drill prediction", children=[
            html.Div([
                html.Br(),
                html.H2(["Geothermal gradients", "(", html.Sup("o"), "C/km)"], style={"font-size": "16px",
                                                              "font-weight": "bold", "display": "inline-block"}),

                html.Label("P90:", style={"font-weight": "bold", "display": "inline-block",
                                          "padding": "1%"}),
                dcc.Input(type="number", value=0, id="P90", style={"textAlign": "center",
                                                                   "width": "10%"}),

                html.Label("P50:", style={"font-weight": "bold", "display": "inline-block",
                                          "padding": "1%"}),
                dcc.Input(type="number", value=0, id="P50", style={"textAlign": "center",
                                                                   "width": "10%",
                                                                   "display": "inline-block"}),

                html.Label("P10:", style={"font-weight": "bold", "display": "inline-block",
                                          "padding": "1%"}),
                dcc.Input(type="number", value=0, id="P10", style={"textAlign": "center",
                                                                   "width": "10%",
                                                                   "display": "inline-block"}),
                dcc.ConfirmDialogProvider (children=[html.Button ("?", style={"margin-left":"2em","textAlign":"center","backgroundColor":"#3283FE",
                                                                              "color":"#E2E2E2", "text-align":"center", "font-size":"16px",
                                                                              "border-radius":"10em", "width":"0.2em", "font-weight":"bold"})],
                                           id="confirm_prediction",
                                           message="You have not entered any gradient value! The correct order should be; p90 < p50 < p10!"),
                html.Label("Total Depth (m.):", style={"font-weight": "bold", "padding-left":"3%", "display":"inline-block"}),
                dcc.Input(type="number", value=0, id="md_prediction", style={"textAlign": "center", "width": "10%",
                                                                             "display":"inline-block", "margin-left":"1em"})
            ], style={"display":"flex", "align-items":"center", "margin-top":"2em"}),

            html.Div ([
                html.Label("Depth Type", style={"font-weight": "bold", "padding-left":"3%", "display":"inline-block", "margin-left":"25em"}),
                html.Label("Change Colours", style={"font-weight": "bold", "padding-left":"3%", "display":"inline-block", "margin-left":"30em"}),
            ], style={"display":"flex", "margin-top":"3em"}),

            html.Div([
                html.Br(),
                html.Button("Calculate & Display", id="calculate", style=button_style, n_clicks=0),
                html.Br (),
                dcc.Dropdown (id="pre_drill_dropdown",
                              style={"width":"450px", "margin-left":"1em"},
                              value="True Vertical Depth below sea level - TVDss (m.)",
                              clearable=False),
                html.Label("P90:", style={"font-weight": "bold", "padding-left":"3%", "display":"inline-block", "margin-left":"5em"}),
                dcc.Dropdown (id="colourp90",
                              options=[{"label": i, "value": i} for i in colours],
                              style={"width":"100px", "margin-left":"0.5em"},
                              value="green",
                              clearable=False),
                html.Label("P50:", style={"font-weight": "bold", "padding-left":"3%", "display":"inline-block"}),
                dcc.Dropdown (id="colourp50",
                              options=[{"label": i, "value": i} for i in colours],
                              style={"width":"100px", "margin-left":"0.5em"},
                              value="orange",
                              clearable=False),
                html.Label("P10:", style={"font-weight": "bold", "padding-left":"3%", "display":"inline-block"}),
                dcc.Dropdown (id="colourp10",
                              options=[{"label": i, "value": i} for i in colours],
                              style={"width":"100px", "margin-left":"0.5em"},
                              value="red",
                              clearable=False)
            ], style={"display":"flex", "margin-top":"1em", "align-items":"center"}),

            html.Div ([
                dcc.Graph(id="prediction_table", style={"width":"40%"}),
                dcc.Graph(id="prediction_graph", style={"width":"60%"}),
            ], style={"display":"flex", "margin-bottom":"2em", "margin-top":"1.5em"}),
        ]),

        dcc.Tab(label="Post-drill analysis", children=[
                html.Br (),
                html.Div ([
                    html.Button("Calculate & Display", id="post_calculate", style={"textAlign": "center", "backgroundColor": "#3283FE",
                                                                         "color": "#E2E2E2", "display": "inline-block"}, n_clicks=0),
                    dcc.ConfirmDialogProvider (children=[html.Button ("Input Check", style={"margin-left":"5em","textAlign":"center",
                                                                                            "backgroundColor":"#3283FE", "color":"#E2E2E2"})],
                                               id="confirm_postdrill",
                                               message="")
                ], style={"display":"flex", "flex-direction":"row"}),

                html.Div ([
                    html.Div ([
                        html.Br (),
                        html.Label ("MD (m.)", style={"font-weight":"bold", "display":"inline-block",
                                                  "margin-left":"12em", "margin-top":"2em"}),
                        html.Label(["BHT", "(", html.Sup("o"), "F)"], style={"font-weight": "bold", "display": "inline-block",
                                                 "margin-left":"9.5em", "margin-top":"2em"}),
                        # MD-1, BHT-1 #
                        html.Br (style={"margin-top":"0.1px"}),
                        html.Label ("Run 1", style={"font-weight": "bold", "display": "inline-block", "margin-left":"2em"}),
                        dcc.Input (id="md1", type="number", value=0, style={"width":"20%", "text-align":"center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        dcc.Input(id="bht1", type="number", value=0, style={"width": "20%", "text-align": "center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        # MD-2, BHT-2 #
                        html.Br (style={"margin-top":"0.1px"}),
                        html.Label ("Run 2", style={"font-weight": "bold", "display": "inline-block", "margin-left":"2em"}),
                        dcc.Input (id="md2", type="number", value=0, style={"width":"20%", "text-align":"center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        dcc.Input(id="bht2", type="number", value=0, style={"width": "20%", "text-align": "center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        # MD-3, BHT-3 #
                        html.Br (style={"margin-top":"0.1px"}),
                        html.Label ("Run 3", style={"font-weight": "bold", "display": "inline-block", "margin-left":"2em"}),
                        dcc.Input (id="md3", type="number", value=0, style={"width":"20%", "text-align":"center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        dcc.Input(id="bht3", type="number", value=0, style={"width": "20%", "text-align": "center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        # MD-4, BHT-4 #
                        html.Br (style={"margin-top":"0.1px"}),
                        html.Label ("Run 4", style={"font-weight": "bold", "display": "inline-block", "margin-left":"2em"}),
                        dcc.Input (id="md4", type="number", value=0, style={"width":"20%", "text-align":"center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        dcc.Input(id="bht4", type="number", value=0, style={"width": "20%", "text-align": "center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        # MD-5, BHT-5 #
                        html.Br (style={"margin-top":"0.1px"}),
                        html.Label ("Run 5", style={"font-weight": "bold", "display": "inline-block", "margin-left":"2em"}),
                        dcc.Input (id="md5", type="number", value=0, style={"width":"20%", "text-align":"center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        dcc.Input(id="bht5", type="number", value=0, style={"width": "20%", "text-align": "center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        # MD-6, BHT-6 #
                        html.Br (style={"margin-top":"0.1px"}),
                        html.Label ("Run 6", style={"font-weight": "bold", "display": "inline-block", "margin-left":"2em"}),
                        dcc.Input (id="md6", type="number", value=0, style={"width":"20%", "text-align":"center", "display":"inline-block",
                                                        "margin-left":"5em"}),
                        dcc.Input(id="bht6", type="number", value=0, style={"width": "20%", "text-align": "center", "display":"inline-block",
                                                        "margin-left":"5em"})
                    ], style={"display":"inline-block"}),

                    html.Div ([
                        dcc.Graph(id="post_table", style={"min-width":"100%"})
                    ]),
                ], style={"display":"flex"}),

                html.Hr (),
                html.Div ([
                    html.Br (),
                    html.Label("Change Colours", style={"font-weight": "bold", "padding-left":"3%", "display":"inline-block", "margin-left":"1em"}),
                    html.Label("AAPG:", style={"font-weight": "bold", "padding-left":"3%", "display":"inline-block"}),
                    dcc.Dropdown (id="colouraapg",
                                options=[{"label": i, "value": i} for i in colours],
                                style={"width":"100px", "margin-left":"0.5em"},
                                value="red",
                                clearable=False),
                    html.Label("Harr.:", style={"font-weight": "bold", "padding-left":"3%", "display":"inline-block"}),
                    dcc.Dropdown (id="colourharr",
                                options=[{"label": i, "value": i} for i in colours],
                                style={"width":"100px", "margin-left":"0.5em"},
                                value="blue",
                                clearable=False),
                ], style = {"display":"flex", "align-items":"center"}),

                html.Div ([
                    html.Br (),
                    dcc.Graph (id="postdrill_graph", style={"width":"50%", "margin-top":"2%",
                                                            "margin-right":"5%"}),
                    html.Br (),
                    dcc.Graph (id="postdrill_grads", style={"width":"50%", "margin-left":"3em", "margin-top":"2%"})
                ], style={"display":"flex"}),

                html.Div (id="datatable"),
                html.Div([
                    html.Br(),
                ])
        ]),

        dcc.Tab(label="Unit conversions", children=[
            html.Br (),
            html.Div ([
                html.Div ([
                    html.Br (),
                    html.Label ("Conversion Type", style={"font-weight": "bold"}),
                    dcc.Dropdown (id="conversion_dropdown",
                                options=[{"label": i, "value": i} for i in conversion_types],
                                style={"width":"250px"}, placeholder="Please select a conversion type")
                ], style={"display":"flex", "flex-direction":"column", "margin-left":"2em"}),

                html.Div ([
                    html.Br (),
                    html.Label ("Value", style={"font-weight": "bold"}),
                    dcc.Input (id='conversion_input', type='number', value=0, style={"text-align": "center"})
                ], style={"display":"flex", "flex-direction":"column", "margin-left":"10em"}),

                html.Div ([
                    html.Br (),
                    html.Label ("Conversion Result", style={"font-weight": "bold"}),
                    html.Div (id="conversion_display")
                ], style={"display":"flex", "flex-direction":"column", "margin-left":"10em"})
            ], style={"display":"flex", "align-items":"flex-start", "margin-bottom":"2.5em"})
        ])
    ]),
], style={"backgroundColor": "rgb(217,217,217)", "padding-left": "1%", "padding-right":"1%"})

@app.callback (
    Output (component_id="confirm_registration", component_property="message"),
    [Input(component_id="Well_name", component_property="value"),
     Input("KB", "value"),
     Input("GL", "value"),
     Input (component_id="confirm_registration", component_property="submit_n_clicks"),
     Input (component_id="regions", component_property="value")]
)

def registration_errors (well_name, kb, gl, clicks, region):
    if clicks:
        if gl == kb:
            return "KB and GL can not be equal to each other!"
        elif kb < 0 or gl < 0:
            return "KB or GL can not be lower than 0!"
        elif region == "Onshore" and kb < gl:
            return "KB can not be lower than GL for onshore wells!"
        elif well_name == "":
            return "Well name is empty, name will not be shown on the graphs!"
        else:
            return "All Inputs seem fine!"

@app.callback (
    Output (component_id="confirm_prediction", component_property="message"),
    [Input("P90", "value"),
     Input("P50", "value"),
     Input("P10", "value"),
     Input (component_id="confirm_prediction", component_property="submit_n_clicks")]
)

def prediction_errors (p90, p50, p10, clicks):
    if clicks:
        if p90 < p50 < p10:
            return "Your inputs satisfy the condition of p90 < p50 < p10!"
        elif p90 == p50 == p10 == 0:
            return "You have not entered any gradient value! The correct order should be; p90 < p50 < p10!"
        else:
            return "Your inputs does not satisfy p90 < p50 < p10 trend! Please check them!"

@app.callback (
    Output (component_id="confirm_postdrill", component_property="message"),
    [Input ("md1", "value"),
     Input ("md2", "value"),
     Input ("md3", "value"),
     Input ("md4", "value"),
     Input ("md5", "value"),
     Input ("md6", "value"),
     Input (component_id="confirm_postdrill", component_property="submit_n_clicks")]
)

def post_errors (md1, md2, md3, md4, md5, md6, clicks):
    if clicks:
        user_data = [md1, md2, md3, md4, md5, md6]
        conditional_data = [user_data[i] for i in range(len(user_data)) if user_data[i] > 0]
        print (conditional_data)
        print ("Length of conditional data is:", len(conditional_data)) 

        if len (conditional_data) == 1:
            return "Please enter more than one MD value for comparison!"       
        elif len(conditional_data) >= 2:       
            for i in range (1, len (conditional_data), 1):
                if conditional_data[i] <= conditional_data[i-1]:
                    return "Your inputs does not satisfy md1 < md2 < md3 < md4 < md5 < md6 trend! Please check them!"
                else:
                    continue    

@app.callback (
    Output (component_id="pre_drill_dropdown", component_property="options"),
    [Input (component_id="regions", component_property="value")]
)

def depth_type_selection (region):
    if region == "Onshore":
        return [{"label": i, "value": i} for i in region_depths["Onshore"]]
    elif region == "Offshore":
        return [{"label": i, "value": i} for i in region_depths["Offshore"]]

@app.callback(
    [Output(component_id="prediction_table", component_property='figure'),
    Output(component_id="prediction_graph", component_property="figure")],
    [Input("P90", "value"),
    Input("P50", "value"),
    Input("P10", "value"),
    Input("md_prediction", "value"),
    Input("KB", "value"),
    Input("GL", "value"),
    Input("calculate", "n_clicks"),
    Input("mast_prediction", "value"),
    Input(component_id="Well_name", component_property="value"),
    Input(component_id="colourp90", component_property="value"),
    Input(component_id="colourp50", component_property="value"),
    Input(component_id="colourp10", component_property="value"),
    Input(component_id="pre_drill_dropdown", component_property="value"),
    Input (component_id="regions", component_property="value")]
)

def calculate_temperatures(p90, p50, p10,
                           md, kb, gl, clicks, mast, name,
                           colourp90, colourp50, colourp10, depth_type, region):
    tvdss = md - (kb - gl)
    tvdbml = md - (kb + gl)

    def depth_listing(value):
        value_list = []
        if value % 500 == 0:
            for i in range(0, value + 500, 500):
                value_list.append(i)
        elif value % 500 != 0:
            for i in range(0, (value - (value % 500)) + 500, 500):
                value_list.append(i)
        value_list.append(value)

        for i in value_list:
            if value == md:
                md_predict.append(i)
            elif value == tvdss:
                tvdss_predict.append(i)
            elif value == tvdbml:
                tvd_predict.append(i)

        if value == md:
            return md_predict
        elif value == tvdss:
            return tvdss_predict
        elif value == tvdbml:
            return tvd_predict

    def calculate():
        if region == "Offshore":
            for i in range(len(tvd_predict)):
                t90 = ((tvd_predict[i] * p90) / 1000) + mast
                t50 = ((tvd_predict[i] * p50) / 1000) + mast
                t10 = ((tvd_predict[i] * p10) / 1000) + mast
                temp_predict90.append(t90)
                temp_predict50.append(t50)
                temp_predict10.append(t10)
        elif region == "Onshore":
            for i in range(len(tvdss_predict)):
                t90 = ((tvdss_predict[i] * p90) / 1000) + mast
                t50 = ((tvdss_predict[i] * p50) / 1000) + mast
                t10 = ((tvdss_predict[i] * p10) / 1000) + mast
                temp_predict90.append(t90)
                temp_predict50.append(t50)
                temp_predict10.append(t10)
        return temp_predict90, temp_predict50, temp_predict10

    if clicks == 1:
        depth_listing(md)
        depth_listing(tvdss)
        depth_listing(tvdbml)
        calculate()
    elif clicks > 1:
        md_predict.clear ()
        tvdss_predict.clear ()
        tvd_predict.clear()
        temp_predict90.clear()
        temp_predict50.clear()
        temp_predict10.clear()
        depth_listing(md)
        depth_listing(tvdss)
        depth_listing(tvdbml)
        calculate()

    if region == "Onshore":
        fig1 = go.Figure(data=[go.Table(header=dict(values=["TVDgl (m.)", 'P90', 'P50', 'P10']),
                                        cells=dict(values=[tvdss_predict, temp_predict90, temp_predict50, temp_predict10]))])
    elif region == "Offshore":
        fig1 = go.Figure(data=[go.Table(header=dict(values=["TVDbml (m.)", 'P90', 'P50', 'P10']),
                                        cells=dict(values=[tvd_predict, temp_predict90, temp_predict50, temp_predict10]))])

    fig2 = go.Figure()
    if depth_type == "TVDbml (m.)":
        fig2.add_trace(go.Scatter(x=temp_predict90, y=tvd_predict, name="P90", line_color=colourp90))
        fig2.add_trace(go.Scatter(x=temp_predict50, y=tvd_predict, name="P50", line_color=colourp50))
        fig2.add_trace(go.Scatter(x=temp_predict10, y=tvd_predict, name="P10", line_color=colourp10))
        fig2.update_yaxes(title="TVDbml (m.)")
    elif depth_type == "TVDkb (m.)":
        fig2.add_trace(go.Scatter(x=temp_predict90, y=md_predict, name="P90", line_color=colourp90))
        fig2.add_trace(go.Scatter(x=temp_predict50, y=md_predict, name="P50", line_color=colourp50))
        fig2.add_trace(go.Scatter(x=temp_predict10, y=md_predict, name="P10", line_color=colourp10))
        fig2.update_yaxes(title="TVDkb (m.)")
    elif depth_type == "TVDgl (m.)":
        fig2.add_trace(go.Scatter(x=temp_predict90, y=tvdss_predict, name="P90", line_color=colourp90))
        fig2.add_trace(go.Scatter(x=temp_predict50, y=tvdss_predict, name="P50", line_color=colourp50))
        fig2.add_trace(go.Scatter(x=temp_predict10, y=tvdss_predict, name="P10", line_color=colourp10))
        fig2.update_yaxes(title="TVDgl (m.)")

    fig2.update_yaxes(autorange="reversed")
    fig2.update_layout(title="Temperature prediction graph of {}".format(name),
                       xaxis_title="Temperatures (C)", legend_title="Legend")
    return fig1, fig2

# Functions for post-drill analysis #
@app.callback(
    [Output (component_id="post_table", component_property="figure"),
    Output(component_id="postdrill_graph", component_property="figure"),
    Output(component_id="postdrill_grads", component_property="figure")],
    [Input ("post_calculate", "n_clicks"),
    Input ("md1", "value"),
    Input ("md2", "value"),
    Input ("md3", "value"),
    Input ("md4", "value"),
    Input ("md5", "value"),
    Input ("md6", "value"),
    Input("bht1", "value"),
    Input("bht2", "value"),
    Input("bht3", "value"),
    Input("bht4", "value"),
    Input("bht5", "value"),
    Input("bht6", "value"),
    Input("KB", "value"),
    Input("GL", "value"),
    Input("mast_prediction", "value"),
    Input(component_id="Well_name", component_property="value"),
    Input(component_id="colouraapg", component_property="value"),
    Input(component_id="colourharr", component_property="value"),
    Input (component_id="regions", component_property="value")]
)

def post_drill_analysis (add, md1, md2, md3, md4, md5, md6,
                         bht1, bht2, bht3, bht4, bht5, bht6, kb, gl, mast, name,
                         colouraapg, colourharr, region):

    m_list = [md1, md2, md3, md4, md5, md6]
    b_list = [bht1, bht2, bht3, bht4, bht5, bht6]

    def calculation ():
        for i in range (len (m_list)):
            if m_list[i] > 0:
                md_list.append (m_list[i])

        for j in range(len(b_list)):
            if b_list[j] > 0:
                bht_list.append(b_list[j])

        for i in range(len(md_list)):
            if region == "Onshore":
                tvd = md_list[i] - (kb - gl)
                tvd_list.append(tvd)
            elif region == "Offshore":
                tvd = md_list[i] - (kb + gl)
                tvdss_list.append(tvd)

        if region == "Onshore":
            for i in range(len(tvd_list)):
                bht = ((1.878 / 1000 * tvd_list[i]) + (8.476e-07 * (tvd_list[i] ** 2)) - (5.091e-11 * (tvd_list[i] ** 3)) - (1.681e-14 * (tvd_list[i] ** 4))) + bht_list[i]
                c = (bht - 32) / 1.8
                bht_harr = -(math.exp(((tvd_list[i] ** 2) * -6))) + (0.01826842109 * tvd_list[i]) - 16.51213476 + bht_list[i]
                c_harr = (bht_harr - 32) / 1.8

                aapg_f.append(bht)
                aapg_c.append(c)
                harr_f.append(bht_harr)
                harr_c.append(c_harr)
        elif region == "Offshore":
            for i in range(len(tvdss_list)):
                bht = ((1.878 / 1000 * tvdss_list[i]) + (8.476e-07 * (tvdss_list[i] ** 2)) - (5.091e-11 * (tvdss_list[i] ** 3)) - (1.681e-14 * (tvdss_list[i] ** 4))) + bht_list[i]
                c = (bht - 32) / 1.8
                bht_harr = -(math.exp(((tvdss_list[i] ** 2) * -6))) + (0.01826842109 * tvdss_list[i]) - 16.51213476 + bht_list[i]
                c_harr = (bht_harr - 32) / 1.8

                aapg_f.append(bht)
                aapg_c.append(c)
                harr_f.append(bht_harr)
                harr_c.append(c_harr)

        md_list.insert (0, 0)
        tvd_list.insert(0, 0)
        tvdss_list.insert(0, 0)
        aapg_c.insert(0, mast)
        harr_c.insert(0, mast)

        if region == "Onshore":
            for i in range (len(aapg_c)):
                grad1 = ((aapg_c[i]-aapg_c[i-1])/(tvd_list[i]-tvd_list[i-1]))*1000
                grad_aapg.append (grad1)

                grad2 = ((harr_c[i]-harr_c[i-1])/(tvd_list[i]-tvd_list[i-1]))*1000
                grad_harr.append (grad2)
        if region == "Offshore":
            for i in range(len(aapg_c)):
                grad1 = ((aapg_c[i] - aapg_c[i - 1]) / (tvdss_list[i] - tvdss_list[i - 1])) * 1000
                grad_aapg.append(grad1)

                grad2 = ((harr_c[i] - harr_c[i - 1]) / (tvdss_list[i] - tvdss_list[i - 1])) * 1000
                grad_harr.append(grad2)

        return md_list, tvd_list, tvdss_list, aapg_c, harr_c, grad_aapg, grad_harr

    if add == 1:
        calculation()
    elif add > 1:
        md_list.clear ()
        bht_list.clear ()
        tvd_list.clear ()
        tvdss_list.clear()
        aapg_f.clear()
        aapg_c.clear()
        harr_f.clear()
        harr_c.clear()
        grad_aapg.clear ()
        grad_harr.clear ()

        calculation()

    aapg1 = []
    aapg2 = []
    harr1 = []
    harr2 = []
    for i in range (len (aapg_c)):
        aapg1.append ("%.2f" % aapg_c[i])
        aapg2.append ("%.2f" % grad_aapg[i])
        harr1.append ("%.2f" % harr_c[i])
        harr2.append ("%.2f" % grad_harr[i])

    if region == "Onshore":
        fig1 = go.Figure(data=[go.Table(header=dict(values=['TVDgl (m.)', 'AAPG (C)', 'Harr (C)', 'AAPG Grads (C/km)', 'Harr Grads (C/km)']),
                                        cells=dict(values=[tvd_list, aapg1, harr1, aapg2, harr2]))])
    elif region == "Offshore":
        fig1 = go.Figure(data=[go.Table(header=dict(values=['TVDbml (m.)', 'AAPG (C)', 'Harr (C)', 'AAPG Grads (C/km)', 'Harr Grads (C/km)']),
                                        cells=dict(values=[tvdss_list, aapg1, harr1, aapg2, harr2]))])

    fig2 = go.Figure()
    if region == "Offshore":
        fig2.add_trace(go.Scatter(x=aapg_c, y=tvdss_list, name="AAPG", line_color=colouraapg))
        fig2.add_trace(go.Scatter(x=harr_c, y=tvdss_list, name="Harrison et al. (1983)", line_color=colourharr))
        fig2.update_yaxes(title_text="TVDbml (m.)")
    elif region == "Onshore":
        fig2.add_trace(go.Scatter(x=aapg_c, y=tvd_list, name="AAPG", line_color=colouraapg))
        fig2.add_trace(go.Scatter(x=harr_c, y=tvd_list, name="Harrison et al. (1983)", line_color=colourharr))
        fig2.update_yaxes(title_text="TVDgl (m.)")
    fig2.update_yaxes(autorange="reversed")
    fig2.update_layout(title="Post-drill temperature analysis of {}".format(name),
                       xaxis_title="Temperatures (C)", legend_title="Legend")

    fig3 = go.Figure()
    if region == "Offshore":
        fig3.add_trace(go.Scatter(x=grad_aapg, y=tvdss_list, name="AAPG Gradients", line_color=colouraapg))
        fig3.add_trace(go.Scatter(x=grad_harr, y=tvdss_list, name="Harrison et al. (1983)", line_color=colourharr))
        fig3.update_yaxes(title_text="TVDbml (m.)")
    elif region == "Onshore":
        fig3.add_trace(go.Scatter(x=grad_aapg, y=tvd_list, name="AAPG Gradients", line_color=colouraapg))
        fig3.add_trace(go.Scatter(x=grad_harr, y=tvd_list, name="Harrison et al. (1983)", line_color=colourharr))
        fig3.update_yaxes(title_text="TVDgl (m.)")
    fig3.update_yaxes(autorange="reversed")
    fig3.update_layout(title="Post-drill geothermal gradient analysis of {}".format(name),
                       xaxis_title="Geothermal Gradients (C/km)", legend_title="Legend")

    return fig1, fig2, fig3

@app.callback(
    Output(component_id="conversion_display", component_property="children"),
    [Input(component_id="conversion_dropdown", component_property="value"),
    Input(component_id="conversion_input", component_property="value")]
)

def conversion (dropdown, input):
    result = 0
    if dropdown == "Feet to Meters":
        result = input / 3.28084
    elif dropdown == "Meters to Feet":
        result = input * 3.28084
    elif dropdown == "Fahrenheit to Celsius":
        result = (input-32) / 1.8
    elif dropdown == "Celsius to Fahrenheit":
        result = (input*1.8) + 32
    elif dropdown == "Meters to Miles":
        result = input * 0.00062137
    elif dropdown == "Miles to Meters":
        result = input / 0.00062137
    elif dropdown == "Meters to Yards":
        result = input * 1.0936
    elif dropdown == "Yards to Meters":
        result = input / 1.0936
    elif dropdown == "Fahrenheit to Kelvin":
        result = ((input-32) / 1.8) + 273.15
    elif dropdown == "Kelvin to Fahrenheit":
        result = ((input - 273.15) * 1.8) + 32
    elif dropdown == "Celsius to Kelvin":
        result = input + 273.15
    elif dropdown == "Kelvin to Celsius":
        result = input - 273.15
    return "%.2f" % result

if __name__ == "__main__":
    app.run_server(debug=True)
