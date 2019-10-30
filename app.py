#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yeonji
"""

import dash

import dash_core_components as dcc

import dash_daq as daq

import dash_html_components as html

from dash.dependencies import Input, Output

 

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

 

df = pd.read_csv("clean_data.csv")

X = df[df.columns.difference(['FinalGrade])]
Y = df['FinalGrade']

 

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

 

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

 

regressor = LinearRegression() 

regressor.fit(X_train, Y_train)

 

 

 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

 

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server=app.server

 

app.layout = html.Div([

       

    html.H1('Student Performance Predictor'),

       

    html.Div([  

    html.Label('Travel Time (Home to School) Score'),

    dcc.Slider(id='traveltime-slider',

            min=0, max=4, step=1, value=3,

               marks={
                
        1: {'label': '1 ( <15 min)'},

        2: {'label': '2 (15 to 30 min)'},

        3: {'label': '3 (30 min to 1 hour)'},

        4: {'label': '4 ( > 1 hour)'},                        

    }),

 

html.Br(),

    html.Label('Weekly Study Time Score'),

    dcc.Slider(id='studytime-slider',

            min=0, max=4, step=1, value=3,

               marks={
                
        1: {'label': '1 ( <2 hours)'},

        2: {'label': '2 (2 to 5 hours)'},

        3: {'label': '3 (5 to 10 hours)'},

        4: {'label': '4 ( > 10 hours)'},                        

    }),

 

html.Br(),

    html.Label('Past Failure Experiences'),

    dcc.Slider(id='failures-slider',

            min=0, max=3, step=1, value=2,

               marks={
                
        0: {'label': '0'},

        1: {'label': '1'},

        2: {'label': '2'},

        3: {'label': '3'},                        

    }),


 

html.Br(),

    html.Label('Quality of Family Relationship (from 1: very bad to 5: excellent),

    dcc.Slider(id='famrel-slider',

            min=1, max=5, step=1, value=2,

               marks={
                
        1: {'label': '1'},

        2: {'label': '2'},

        3: {'label': '3'},

        4: {'label': '4'},    

        5: {'label': '5'}                    

    }),


html.Br(),

    html.Label('Free Time After School (from 1: very low to 5: very high),

    dcc.Slider(id='freetime-slider',

            min=1, max=5, step=1, value=2,

               marks={
                
        1: {'label': '1'},

        2: {'label': '2'},

        3: {'label': '3'},

        4: {'label': '4'},    

        5: {'label': '5'}                    

    }),

 html.Br(),

    html.Label('Going out With Friends Extent (from 1: very low to 5: very high),

    dcc.Slider(id='goout-slider',

            min=1, max=5, step=1, value=2,

               marks={
                
        1: {'label': '1'},

        2: {'label': '2'},

        3: {'label': '3'},

        4: {'label': '4'},    

        5: {'label': '5'}                    

    }),

 html.Br(),

    html.Label('Health Status Score (from 1: very bad to 5: very good),

    dcc.Slider(id='health-slider',

            min=1, max=5, step=1, value=2,

               marks={
                
        1: {'label': '1'},

        2: {'label': '2'},

        3: {'label': '3'},

        4: {'label': '4'},    

        5: {'label': '5'}                    

    }),


html.Br(),

html.Label('First Period Grade'),

dcc.Slider(id='FirstPeriodGrade-slider',

            min=0, max=20, step=1, value=10,

               marks={
                
        0: {'label': '0'},

        5: {'label': '5'},

        10: {'label': '10'},

        15: {'label': '15'},

        20: {'label': '20'}                            

    }),

 

html.Br(),

html.Label('Second Period Grade'),

dcc.Slider(id='SecondPeriodGrade-slider',

            min=0, max=20, step=1, value=10,

               marks={
                
        0: {'label': '0'},

        5: {'label': '5'},

        10: {'label': '10'},

        15: {'label': '15'},

        20: {'label': '20'}                            

    }),



],className="pretty_container four columns"),

 

  html.Div([

 

    daq.Gauge(

        id='FinalGrade-gauge',

        showCurrentValue=True,

        color={"gradient":True,"ranges":{"red":[0,5],"yellow":[5,15],"green":[15,20]}},

        label="Final Grade",

        max=20,

        min=0,

        value=10

    ),

])

    ])

 

 

@app.callback(

    Output('FinalGrade-gauge', 'value'),

    [Input('traveltime-slider', 'value'),

     Input('studytime-slider', 'value'),

     Input('failures-slider', 'value'),

     Input('famrel-slider', 'value'),

     Input('freetime-slider', 'value'),

     Input('health-slider', 'value'),

     Input('FirstPeriodGrade-slider', 'value'),

     Input('SecondPeriodGrade-slider', 'value')

     ])

def update_output_div(traveltime,
                      studytime,
                      failures,
                      famrel,
                      freetime,
                      goout,
                      health,
                      FirstPeriodGrade,
                      SecondPeriodGrade):

   X_case = pd.DataFrame({'traveltime':[traveltime],'studytime':[studytime],
                          'failures':[failures],'famrel':[famrel],'freetime':[freetime],
                          'goout':[goout],'health':[health],
                          'FirstPeriodGrade':[FirstPeriodGrade],'SecondPeriodGrade':[SecondPeriodGrade],})

   Y_case = regressor.predict(X_case)


   return Y_case[0]

 

 

if __name__ == '__main__':

    app.run_server()
