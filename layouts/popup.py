from dash import html,dcc
import dash_bootstrap_components as dbc
def get_popup():
  return html.Div([
    dbc.Modal( [
      dbc.ModalHeader("More information about selected row"),
      dbc.ModalBody(id="row-selection-modal-content"),
      html.Div([
        html.Div([
        html.Label("tp", style={"display": "inline-block", "width": "150px", "textAlign": "right"}),
        dcc.Input(id='tp', type='number',  min=0, max=1000000, placeholder="tp",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
        html.Span(
                      " ⓘ", 
                      id="tp-target", 
                      style={"cursor": "pointer", "marginLeft": "5px"}
                  ),
                  dbc.Tooltip(
                      "Take Profit",
                      target="tp-target",
                      placement="right",
                  ),
        ]),
        html.Div([
        html.Label("sl", style={"display": "inline-block", "width": "150px", "textAlign": "right"}),
        dcc.Input(id='sl', type='number',  min=0, max=1000000, placeholder="sl",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
        html.Span(
                      " ⓘ", 
                      id="sl-target", 
                      style={"cursor": "pointer", "marginLeft": "5px"}
                  ),
                  dbc.Tooltip(
                      "Stop Loss",
                      target="sl-target",
                      placement="right",
                  ),
        ]),
        html.Div([
        html.Label("ppmax", style={"display": "inline-block", "width": "150px", "textAlign": "right"}),
        dcc.Input(id='ppmax', type='number',  min=0, max=1000000, placeholder="ppmax",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
        html.Span(
                      " ⓘ", 
                      id="ppmax-target", 
                      style={"cursor": "pointer", "marginLeft": "5px"}
                  ),
                  dbc.Tooltip(
                      "Pourcentage du capital que vous etes pret à perdre.",
                      target="ppmax-target",
                      placement="right",
                  ),
        ]),
        html.Div([
        html.Label("capital", style={"display": "inline-block", "width": "150px", "textAlign": "right"}),
        dcc.Input(id='capital', type='number',  min=0, max=1000000, placeholder="capital",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
        html.Span(
                      " ⓘ", 
                      id="capital-target", 
                      style={"cursor": "pointer", "marginLeft": "5px"}
                  ),
                  dbc.Tooltip(
                      "Capital d'investissement",
                      target="capital-target",
                      placement="right",
                  ),
        ]),
        html.Div([
        html.Iframe(srcDoc=open("assets/tradingView.html").read(), width='100%', height='350'),
        ]),
        html.Div(id="output-simulation",style={"width":350,"height":100})
      ]),
      dbc.ModalFooter([dbc.Button("Simulate", id="row-selection-modal-launch-simulation", className="ml-auto",style={'horizontalAlign':'left','color':'lightgreen'}),dbc.Button("Validate", id="row-selection-modal-close", className="ml-auto",style={'color':'orange'})]),
    ],
    id="row-selection-modal",
    ),
      ])