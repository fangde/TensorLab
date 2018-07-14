import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


import pymongo


app=dash.Dash()


df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')



app.layout=html.Div(children=[
    html.H1(children="hello dash"),

    html.Div(children='''
    Dash: a Weba pplication framework for python
    '''),

    dcc.Input(id='my-id', value='initial value', type="text"),
    html.P(),

    html.Div(id='my-div'),


##for date visuzlaiton, server side rendering#
    html.Img(id='my-img',src="data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7"),



    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    dcc.Graph(id='example-graph',
              figure={
                    'data':[
                        go.Scatter(
                            x=df[df['continent'] == i]['gdp per capita'],
                            y=df[df['continent'] == i]['life expectancy'],
                            text=df[df['continent'] == i]['country'],
                            mode='markers',
                            opacity=0.7,
                            marker={
                                'size': 15,
                                'line': {'width': 0.5, 'color': 'white'}
                            },
                            name=i
                        ) for i in df.continent.unique()
                    ],
                  'layout':{
                      'title':'Dash visulization'
                  }


              }

    )

])


@app.callback(
    Output(component_id='my-div',   component_property='children'),
    [Input(component_id='my-id',    component_property='value')]
)
def update_output_div(input_value):
    print "server call back"
    return "{}".format(input_value)

if __name__ =='__main__':
    app.run_server(debug=True)
