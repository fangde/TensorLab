import dash
   di=numpy.array([w[i].ravel() for w in weights])
   d.append(di)



app=dash.Dash()

app.layout=html.Div(children=[
    html.H1(children="TensorLab Visualization"),

    html.H2(children="Parameter Longitudinal Analysis"),

    dcc.Input(id='my-id', value='initial value', type="text"),
    html.P(),

    html.Div(id='my-div'),


##for date visuzlaiton, server side rendering#
##    html.Img(id='my-img',src="data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7"),




    dcc.Graph(id='ParametersPlot',
              figure={
                    'data':[
                        go.Scattergl(
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
                      'title':'Loss of all the  Parameters'
                  }


              }

    ),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL',
        multi=True

    ),

    html.Div(children=[

     dcc.Graph( id='pt1'+str(uuid.uuid4()),
              figure={
                  'data': [
                      go.Surface(
                          z=numpy.abs(di.transpose()),
                          opacity=0.7,

                          name="hello"
                      ) ],
                  'layout': {
                      'title': 'Weight Longitudinal Visualization'

                  }

              }

              ) for di in d ])


]
)


@app.callback(
    Output(component_id='my-div',   component_property='children'),
    [Input(component_id='my-id',    component_property='value')]
)
def update_output_div(input_value):
    print "server call back"
    return "{}".format(input_value)

if __name__ =='__main__':
    app.run_server(debug=True)
