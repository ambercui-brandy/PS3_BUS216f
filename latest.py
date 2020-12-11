#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 00:38:37 2020

@author: erin
"""

import dash
import dash_table
from dash_table import DataTable
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go 
import plotly.express as px
from dash.dependencies import Input, Output, State
from time import strftime
import pickle
import os
import matplotlib.pyplot as plt


##### Layout #####
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


mbrs = ["Claire Dunphy", "Phil Dunphy", "Haley Dunphy", "Alexandria Dunphy", "Lucas Dunphy", 
        "Jay Pritchett", "Gloria Pritchett", "Manny Delgado-Pritchett", "Mitchell Pritchett", 
        "Cameron Tucker", "Lily Tucker-Pritchett", "Joe Pritchett"]

expense = ["Food / Groceries", "Rent / Utilities", "Health / Insurance", "Clothing / Beauty", "Travel / Leisure", "Transport / Auto", "Other"]

income = ["Salary", "Investment", "Refund", "Bonus", "Other"]

### Initialize Account Book ###           
bill = [['2020-12-10','INIT', 10, 'a', 10, 'b', 10000]]
fname = '/tmp/e.data'  # change the name for a new record
if not os.path.exists(fname):
    with open(fname, 'wb') as f:
        pickle.dump(bill, f)
          
data = [['2020-12-8','INIT', 0, '', 0, '', 10000],
        ['2020-12-9','AMBER', 1000, 'Rent / Utilities', 2000, 'Investment', 11000],
        ['2020-12-9','ERIN', 300, 'Clothing / Beauty', 0, '', 10700],
        ['2020-12-10','ERIN', 0, '', 5000, 'Salary', 15700],
        ['2020-12-10','AMBER', 30, 'Food / Groceries', 0, '', 15670]]

df = pd.DataFrame(data,columns=['date', 'name','save', 'save_category', 'check', 'check_category', 'balance'])


controls = dbc.Card(
    [   
     
     
        ### Member Section ###       
        dbc.FormGroup(
            [
                dbc.Label("Name"),
                dcc.Dropdown(
                    id="member",
                    options=[
                        {"label": mbr, "value": mbr}
                        for mbr in mbrs
                    ],
                    value="Please enter your name",
                ),
            ]
        ),
        
        
        ### Check Section ###
        dbc.Button(
            "Check",
            id="check-button",outline=True,color='warning',
            className="mb-3",
        ),
        dbc.Collapse(
            dbc.Card(
                [
                dbc.FormGroup(
                    [
                        dbc.Label("Category"),
                        dcc.Dropdown(
                            id="expense_category",
                            options=[
                                {"label": exp, "value": exp}
                                for exp in expense
                            ],
                            value="Please select...",
                                  ),
                     ]
                ),
                
                dbc.FormGroup(
                    [  
                        dbc.Label("Check Amount"),
                        dbc.Input(id = "expense", type = "number", value = 0),
                        dbc.FormFeedback(valid=True),
                        dbc.FormFeedback("Invalid input", valid = False,
                            ),
                    ]
                ),
                ]  
            ),
            id="check",
        ),
        
        
        ### Save Section ###
        dbc.Button(
            "Save",
            id="save-button",outline=True,color='info',
            className="mb-3",
        ),
        dbc.Collapse(
            dbc.Card(
                [
                dbc.FormGroup(
                    [
                        dbc.Label("Category"),
                        dcc.Dropdown(
                            id="income_category",
                            options=[
                                {"label": inc, "value": inc}
                                for inc in income
                            ],
                            value="Please select...",
                                  ),
                     ]
                ),
                
                dbc.FormGroup(
                    [    
                        dbc.Label("Save Amount"),
                        dbc.Input(id = "income", type = "number", value = 0),
                        dbc.FormFeedback(valid=True),
                        dbc.FormFeedback("Invalid input", valid = False,
                            ),
                    ]
                ),
                ]
            ),
            id="save",
        ),
        
        dbc.Button("Submit", id="submit", outline=True, color="success", className="mr-1"),
    ],
    body = True,
)
        

### Table and Graphs ###
# tabs = dbc.Card(
#     [
#         dbc.CardHeader(
#             dbc.Tabs(
#                 [
#                     dbc.Tab(label="Account Table", tab_id="tab-1"),
#                     dbc.Tab(label="Expense Category Chart", tab_id="tab-2"),
#                     dbc.Tab(label="Income Category Chart", tab_id="tab-3"),
#                 ],
#                 id="3tabs",
#                 card=True,
#                 active_tab="tab-1",
#             )
#         ),
#         dbc.CardBody(html.P(id="tab-content", className="card-text")),
#     ]
# )

visuals = dbc.Card(
            [
                dbc.Row([
                        dbc.Col(dcc.Graph(id="graph1", style={"height": "300px"})),
                        dbc.Col(dcc.Graph(id="graph2", style={"height": "300px"})),
                        ],
                        ),
                dbc.Row([
                        dash_table.DataTable(id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('df'),)
                        ],
                        ),
            ],
            body = True,
            )


###
# dash_table.DataTable(
#     id='table',
#     columns=[{"name": i, "id": i} for i in df.columns],
#     data=df.to_dict('records'),
# )


app.layout = html.Div(
    [   
        dbc.Row(
            html.Img(
            id='logo1',
            src=app.get_asset_url("book_logo.png"),
            height="150px",
            ),
        ),
        dbc.Row([dbc.Col(html.H3(
            children="Family Account Book",
            style={'textAlign':'left',
                    'margin':'20px',
            }))]),
        dbc.Row(
               [
                dbc.Col(controls, width="4"),
                dbc.Col(visuals, width="6"),
               ]
               ),
                    
    ]
    )




### new layout, no tab ###
# app.layout = dbc.Container(
#     fluid=True,
#     children=[
#         html.H1("Family Account Book"),
#         html.Hr(),
#         dbc.Row(
#             [
#                 dbc.Col([dbc.Card(controls, body=True)], md=3),
#                 dbc.Col(dcc.Graph(id="graph1", style={"height": "300px"}), md=4),
#                 dbc.Col(dcc.Graph(id="graph2", style={"height": "300px"}), md=5),
#                 # need one more row to print table
#             ]
#         ),
#     ],
#     style={"margin": "auto"},
# )

##### Callback #####

### Tabs ###
# @app.callback(Output('tab_content','children'),
# 				Input('3tabs','active_tab'))
# def render_content(tab):
# 		if tab == 'tab-1':
# 				return html.Div(id="table1")
# 		elif tab=='tab-2':
# 				return html.Div([dcc.Graph(id='graph1')])

# 		elif tab=='tab-3':
# 				return html.Div([dcc.Graph(id='graph2')])
            
  
### Collapse ###

@app.callback(
    Output("save", "is_open"),
    [Input("save-button", "n_clicks")],
    [State("save", "is_open")],
)
def toggle_collapse1(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("check", "is_open"),
    [Input("check-button", "n_clicks")],
    [State("check", "is_open")],
)
def toggle_collapse2(n, is_open):
    if n:
        return not is_open
    return is_open


### Check Validity ###
@app.callback(
    [Output("expense", "valid"), Output("expense", "invalid")],
    [Input("expense", "value")],
)
def check_validity1(number):
    if number >= 0:
        return True, False
    return False, True

@app.callback(
    [Output("income", "valid"), Output("income", "invalid")],
    [Input("income", "value")],
)
def check_validity2(number):
    if number >= 0:
        return True, False
    return False, True

          
            
### Initialize Account Book ###           
bill = [['2020-12-10','INIT', 10, 'a', 10, 'b', 10000]]
fname = '/tmp/e.data'  # change the name for a new record
if not os.path.exists(fname):
    with open(fname, 'wb') as f:
        pickle.dump(bill, f)
          
data = [['2020-12-8','INIT', 0, '', 0, '', 10000],
        ['2020-12-9','AMBER', 1000, 'Rent / Utilities', 2000, 'Investment', 11000],
        ['2020-12-9','ERIN', 300, 'Clothing / Beauty', 0, '', 10700],
        ['2020-12-10','ERIN', 0, '', 5000, 'Salary', 15700],
        ['2020-12-10','AMBER', 30, 'Food / Groceries', 0, '', 15670]]

df = pd.DataFrame(data,columns=['date', 'name','save', 'save_category', 'check', 'check_category', 'balance'])
        
        

### Tab-1: Account Book ###
@app.callback(
	
		Output('table1', 'children'),
	
	[
		Input("submit","n_clicks")
	],
	[
        State('member', 'value'),
		State('expense', 'value'),
        State('expense_category', 'value'),
		State('income', 'value'),
		State('income_category', 'value'),
	],
)

def update(n_clicks, member, expense, expense_category, income, income_category):
    if n_clicks:
        now_time = strftime('%Y-%m-%d')         
        with open(fname, 'rb') as fobj:
            records = pickle.load(fobj)
            old_balance = int(records[-1][-1])    
            all_balance = old_balance - expense + income               
            new_bill = [now_time, member, income, income_category, expense, expense_category, all_balance]       
            records.append(new_bill)
            with open(fname,'wb') as fobj:
                pickle.dump(records, fobj)
        
          
# def query(fname):
#     print('%-12s%-10s%-8s%-20s%-8s%-20s%-10s' % ('date', 'name','save', 'save_category', 'check', 'check_category', 'balance'))
#     with open(fname, 'rb') as fobj:
#         records = pickle.load(fobj)
#         for i in records:
#             print('%-12s%-10s%-8s%-20s%-8s%-20s%-10s'  % tuple(i))
             
  
def make_table(n_clicks):            
    if n_clicks:                            
        dt = pd.read_pickle(fname)
        df = pd.DataFrame(list(dt), columns = ['date', 'name','save', 'save_category', 'check', 'check_category', 'balance'])
        data = df.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (df.columns)]
        return dt.DataTable(data=data, columns=columns)


### Tab-2: Expense Category Chart ###   
@app.callback(
	
		Output('graph1', 'figure'),
	
	[
		Input("submit","n_clicks")
	],
	[
		State('member', 'value'),
        State('expense_category', 'value'),
		State('expense', 'value'),
		State('income_category', 'value'),
		State('income', 'value'),
	],
)
  
    
def pie_check(n_clicks):
    if n_clicks:
        dt = pd.read_pickle(fname)
        df = pd.DataFrame(list(dt), columns = ['date', 'name','save', 'save_category', 'check', 'check_category', 'balance'])
        df = df.loc[df['check'] > 0]
        df = pd.DataFrame(df[['check','check_category']].groupby(['check_category']).sum())
        fig = px.pie(df,names='check', color_discrete_sequence=px.colors.sequential.matter)
        return fig
    




### Tab-3: Income Category Chart ###
@app.callback(
		Output('graph2', 'figure'),
	[
		Input("submit","n_clicks")
	],
	[
		State('member', 'value'),
        State('expense_category', 'value'),
		State('expense', 'value'),
		State('income_category', 'value'),
		State('income', 'value'),
	],
)


def pie_save(n_clicks):
    if n_clicks:
        dt = pd.read_pickle(fname)
        df = pd.DataFrame(list(dt), columns = ['date', 'name','save', 'save_category', 'check', 'check_category', 'balance'])
        df = df.loc[df['check'] > 0]
        df = pd.DataFrame(df[['save','save_category']].groupby(['save_category']).sum())
        fig = px.pie(df,names='save', color_discrete_sequence=px.colors.sequential.tempo)
        return fig





if __name__ == '__main__':
	app.run_server(debug=True)


