import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import pymongo
import seed

db=seed.db







df=pd.DataFrame(db.queryValLog({}))




print df.columns.values.tolist()

print df.groupby('studyID')


print df.studyID.unique()


app=dash.Dash()





app.layout=html.Div(children=[
    html.H1(children="hello dash"),

    html.Div(children='''
    Dash: a Weba pplication framework for python
    '''),

    dcc.Input(id='my-id', value='initial value', type="text"),
    html.P(),

    html.Div(id='my-div'),


##for date visuzlaiton, server side rendering#
##    html.Img(id='my-img',src="data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7"),


    html.P(children="SelecViz"),

    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL',
        multi=True

    ),

    dcc.Graph(id='example-graph',
              figure={
                    'data':[
                        go.Scatter(
                            x=df[df['studyID'] == i]['epoch'],
                            y=df[df['studyID'] == i]['acc'],
                            text=df[df['studyID'] == i]['time'],
                            mode='markers',
                            opacity=0.7,
                            marker={
                                'size': 10,
                                'line': {'width': 0.5, 'color': 'white'}
                            },
                            name=i
                        ) for i in df.studyID.unique()
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
