from dash import html,dcc
def get_figures():
  return html.Div([
    html.Div(className='simple',style={'display': 'flex', 'justify-content': 'space-around'},children=[
    dcc.Loading( id="loading-sunburst", type="circle", children=[dcc.Graph(figure={},id='graph_complexe')]),
    dcc.Loading( id="loading-sunburst2", type="circle", children=[dcc.Graph(figure={},id='graph_simple')]),
    html.Div(children='Valeurs'),
      dcc.RadioItems(options=['usd_balance','gainNR','gainEst','perteEst'], value='gainNR',id='values-item',inline=True),
      html.Div(children='Theme'),
        html.Div(className='row', children=[
          dcc.RadioItems(options=['strategie','famille','protocol','position','vision','token'], value='famille',id='theme-item',inline=True),
          ]),
      #html.Div(className='row', children=[ ]),
    ]),
    dcc.Slider(2, 8, 1, value=3, id='profondeur'),
  ])
