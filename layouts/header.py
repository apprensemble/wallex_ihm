from dash import html
import dash_daq as daq

def get_header():
  return html.Div([
    html.Div(className='row', children='Wallex: Maquette1', style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}), 
    daq.BooleanSwitch(id='showmemore', on=False),
    html.Button("Reset Filters", id="reset-button", n_clicks=0),
    ])