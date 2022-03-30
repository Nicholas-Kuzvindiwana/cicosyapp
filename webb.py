from ast import Return
from turtle import width
from click import option
import dash
from dash import  dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from matplotlib.pyplot import figure
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from plotly import graph_objects as go

#FOR IMPORTING JSON file
import urllib.request
import json


url="http://127.0.0.1:5000/cicosy"
df = pd.read_json(url)
dff=df.groupby('OrderDate',as_index=False)[['Sales','Revenue','Quantity','Profit']].sum()
df1=df.groupby('Sub-Category',as_index=False)[['Sales']].sum()
df2 = df1.sort_values(['Sales'], ascending=False)


fig = go.Figure(go.Indicator(
    mode = "number+delta",
    value = df['Quantity'].sum(),
    delta = {"reference": 10000, "valueformat": ".0f"},
    title = {"text": "Daily Users online"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]}))
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
                
app.layout=dbc.Container([
             dbc.Row([
                 html.Div(
                children= 'Market Place Dashboard',
                style = dict(backgroundColor="#1C4E80",
                color='#ffffff ',
                textAlign='center',
                fontSize=25),
                 className='eight columns'),
                 
             ],className="row", style={'backgroundColor':'#1C4E80'}),

             html.Div([
                 html.Br(),
                 dbc.Card(
                     dbc.CardBody([
                         dbc.Row([
                             dbc.Col([
                 html.H4("total sales", className="card-title"),
                html.P(df['Sales'].sum(),
                className="card-value"),
                html.I(className="fa-solid fa-cart-shopping-fast"),
                 html.Span([
                     html.I(className="fa-solid fa-landmark"),
                     html.Span(" 5.5% vs Last Year",
                     className="up")
                 ])
                             ],width=3),
                             dbc.Col([
                 html.H4("Total views", className="card-title"),
                html.P(df['Quantity'].sum(),
                className="card-value"),
                html.I(className="fa-solid fa-cart-shopping-fast"),
                 html.Span([
                     html.I(className="fa-solid fa-landmark"),
                     html.Span(" 6.7% vs yesterday",
                     className="up")
                 ])
                             ],width=3),
                             dbc.Col([
                html.H4("Yearly Revenue", className="card-title"),
                html.P(df['Revenue'].sum(),
                className="card-value"),
                html.I(className="fa-solid fa-cart-shopping-fast"),
                 html.Span([
                     html.I(className="fa-solid fa-landmark"),
                     html.Span(" 12.0% vs last year",
                     className="up")
                 ])
                             ],width=3),
                             dbc.Col([
 dcc.Dropdown(
                id='Date',
                value='OrderDate',
                multi=False,
                options=[{'value': x, 'label': x} 
                         for x in ['OrderDate']],
            ),
                             ],width=3)
                         ], align='center')                         
                     ])
                 ),
                 html.Br(),
                 
    dbc.Row([
        dbc.Col([
            html.P(
                dbc.Badge(
                    "Select ",
                    pill=True,
                    color="primary",
                    className="me-4",
                )
            ),
            dcc.Dropdown(
                id='names',
                value='Region',
                multi=False,
                 options=[{'value': x, 'label': x} 
                         for x in ['Category', 'Region', 'ShipMode','Sub-Category','Segment','State']],
            ),
            

            
            dcc.Graph(id='line-fig',figure={},clickData=None, hoverData=None)           
                                  
         
        ],width={'size':4}) ,
        dbc.Col([
            html.P(
                dbc.Badge(
                   "Sales value",
                   color="white",
                   text_color="primary",
                   className="border me-6",
                )
            ), 
            dcc.Dropdown(
                id='Revenue',
                value='Revenue',
                multi=False,
                options=[{'value': x, 'label': x} 
                         for x in ['Quantity', 'Profit', 'Revenue', 'Sales','Discount']],
            ),
            dcc.Graph(id='pie-chart', figure={}),
            

        ],width={'size':4, 'offset':0, 'order':2}),

        dbc.Col([
                                 html.H4(['Top Selling Products'],
                                    style = dict(backgroundColor="#1C4E80",
                                    color='#ffffff ' ,
                                     className = 'display-4')), 
       
       dash_table.DataTable(df2.to_dict('records'))
        #dcc.Graph(id="liner-chart"),
        ],width={'size':3, 'offset':0, 'order':3}),
        
        
    ]),
    dbc.Row([
        dbc.Col([
            # dcc.Dropdown(
            #     id='Values',
            #     value='Revenue',
            #     multi=False,
            #     options=[{'value': x, 'label': x} 
            #              for x in ['Quantity', 'Profit', 'Revenue', 'Sales']],
            # ),dcc.Graph(id='time-series', figure={}),
            dcc.Graph(id ='ind', figure=(fig.add_trace(go.Scatter(y=dff['Revenue']))))

        ],width=12)
         
        
    

    ])

             ])
],fluid=True,) 


##Connecting the components
@app.callback(
    Output('line-fig','figure'),
    [Input('names','value'),
    Input('Revenue','value')]
)
def update_graph(names,Revenue):
    fig=px.bar(df,x=names,y=Revenue, title="bar charts",hover_data=[Revenue, names], color=Revenue)
    return fig
    
@app.callback(
    Output("pie-chart", "figure"),
    [Input("names", "value"), 
    Input("Revenue", "value")]
)

def generate_chart(names, Revenue):
   fig2 = px.pie(df, values=Revenue, names=names,color_discrete_sequence=px.colors.sequential.RdBu, hole=.2 )
   return fig2
# @app.callback(
#     Output("time-series", "figure"),
#     [Input('Values', "value")]
# )
# def display_time_series(Revenue):
#     fig3 = px.line(dff, x='OrderDate', y=Revenue)
#     return fig3

# @app.callback(
#     Output("liner-chart", "figure"), 
#      [Input('names','value'),
#     Input('Revenue','value')])
# def update_line_chart(names, Revenue):
#     fig4 =px.violin(df, x=names, y=Revenue,)
#     return fig4   


    



             
            


if __name__=='__main__':
    app.run_server(debug=True,port=2000 )