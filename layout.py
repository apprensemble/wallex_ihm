from dash import html,dcc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import dash_daq as daq
from wallex import TimeSeriesManager
from assets import init_tableau as it

ts = TimeSeriesManager.TimeSeriesManager()
colonnes = ['vision','strategie','protocol','famille','position','bc','wallet','token','ref_date_comparaison','gainNR','old_usd_balance','usd_balance','native_balance','exchange_rate','tp','sl','ppmax','capital','rr','gainEst','perteEst']
#original colonnes_width

sf = it.creation_tableau_de_base(colonnes,ts)
col_def = it.init_coldef(colonnes)
etat_colonnes = it.init_etat_col(colonnes)
# Disposition de l'application
layout = html.Div([
  html.Div(className='row', children='Wallex: Maquette1', style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}), 
  daq.BooleanSwitch(id='showmemore', on=False),
  html.Button("Reset Filters", id="reset-button", n_clicks=0),
  html.Div(className='simple',style={'display': 'flex', 'justify-content': 'space-around'},children=[
  dcc.Loading( id="loading-sunburst", type="circle", children=[dcc.Graph(figure={},id='graph_complexe')]),
  dcc.Loading( id="loading-sunburst2", type="circle", children=[dcc.Graph(figure={},id='graph_simple')]),
  html.Div(children='Valeurs'),
    dcc.RadioItems(options=['usd_balance','gainNR'], value='gainNR',id='values-item',inline=True),
    html.Div(children='Theme'),
      html.Div(className='row', children=[
        dcc.RadioItems(options=['strategie','famille','protocol','position','vision','token'], value='famille',id='theme-item',inline=True),
        ]),
    #html.Div(className='row', children=[ ]),
  ]),
  dcc.Slider(2, 8, 1, value=3, id='profondeur'),
  dag.AgGrid(
      id='ag-grid',
      rowData=sf.to_dict('records'),  # Les données du tableau
      columnDefs=col_def,
      defaultColDef={
          "sortable": True,  # Permet de trier les colonnes
          "filter": True,    # Ajoute des filtres à chaque colonne
          "resizable": True, # Permet de redimensionner les colonnes
          "editable": True
      },
      dashGridOptions={
          "columnDefs": None,
          "rowSelection": "single",  # Permet de sélectionner une seule ligne
          "animateRows": True,  # Ajoute des animations de déplacement
      },
      columnState=etat_colonnes,
      style={'height':'200px'},
  ),
  dcc.Store(id='mes-colonnes',data={'liste_colonnes':colonnes,'initial_df':sf.to_dict('records'),'etat_colonnes':etat_colonnes}),
  html.Div(id="output"),

  dbc.Modal( [
    dbc.ModalHeader("More information about selected row"),
    dbc.ModalBody(id="row-selection-modal-content"),
    html.Div([
      dcc.Input(id='tp', type='number',  min=0, max=1000000, placeholder="tp",style={'marginLeft':'10px','inline':'true'}),
      dcc.Input(id='sl', type='number',  min=0, max=1000000, placeholder="sl",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
      dcc.Input(id='ppmax', type='number',  min=0, max=1000000, placeholder="ppmax",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
      dcc.Input(id='capital', type='number',  min=0, max=1000000, placeholder="capital",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
      html.Iframe(srcDoc=open("assets/tradingView.html").read(), width='100%', height='350'),
    ]),
    dbc.ModalFooter(dbc.Button("Close", id="row-selection-modal-close", className="ml-auto")),
  ],
  id="row-selection-modal",
  ),
])