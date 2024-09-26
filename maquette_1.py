import dash
from dash import html,dcc
from dash.dependencies import Input, Output,State
import dash_ag_grid as dag
import dash_daq as daq
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
from wallex import TimeSeriesManager
import pprint


#strategie_vision_famille_position_protocol_bc
ts = TimeSeriesManager.TimeSeriesManager()


# Créer l'application Dash
app = dash.Dash(__name__)

# Exemple de dataframe
#colonnes = ['','','token','famille','exchange_rate','old_usd_balance','usd_balance','gainNR']
colonnes = ['vision','strategie','protocol','famille','position','bc','wallet','token','exchange_rate','old_usd_balance','usd_balance','gainNR']
colonnes_bis = ['famille','bc','wallet','protocol','token','exchange_rate','old_usd_balance','usd_balance','gainNR']

#fonctions de preparation
def creation_tableau_de_base(colonnes):
    df = ts.get_full_df_with_apr()
    df['old_usd_balance'] = df['ref_exchange_rate'] * df['native_balance'] 
    df['gainNR'] = df['usd_balance'] - df['old_usd_balance']
    df.loc[df['gainNR'] == 0, 'gainNR'] = 0.000001
    #sf = df.groupby(['token','famille','usd_balance','pct'])['gainNR'].sum().reset_index()
    #sf = df.groupby(['token','famille','exchange_rate','old_usd_balance','usd_balance'])['gainNR'].sum().reset_index()
    sf = df.groupby(colonnes[0:-1])[colonnes[-1]].sum().reset_index()
    #sf['usd_balance'] = round(sf['usd_balance'],2)
    #sf['gainNR'] = round(sf['gainNR'],2)
    print(df.sum()['usd_balance'])
    print(sf.sum()['gainNR'])
    return sf

sf = creation_tableau_de_base(colonnes)
zf = creation_tableau_de_base(colonnes_bis)
col_def = []
for col in colonnes:
    col_def.append({"headerName": col, "field": col, "sortable": True, "filter": True})

# Disposition de l'application
app.layout = html.Div([
    html.Div(className='row', children='Wallex: Maquette1',
                style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}), 
        daq.BooleanSwitch(id='showmemore', on=False),
        html.Div(className='simple',style={'display': 'flex', 'justify-content': 'space-around'},children=[
    dcc.Graph(figure={},id='graph_complexe'),
    dcc.Graph(figure={},id='graph_simple'),
html.Div(children='Valeurs'),
  dcc.RadioItems(options=['usd_balance','gainNR'], value='gainNR',id='values-item',inline=True),
html.Div(children='Theme'),
html.Div(className='row', children=[
  dcc.RadioItems(options=['strategie','famille','protocol','position','vision','token'], value='famille',id='theme-item',inline=True),
        ]
        ),
    #html.Div(className='row', children=[ ]),
  ]),
    dag.AgGrid(
        id='ag-grid',
        rowData=sf.to_dict('records'),  # Les données du tableau
        columnDefs=col_def,
        defaultColDef={
            "sortable": True,  # Permet de trier les colonnes
            "filter": True,    # Ajoute des filtres à chaque colonne
            "resizable": True  # Permet de redimensionner les colonnes
        },
        dashGridOptions={
            "rowSelection": "single",  # Permet de sélectionner une seule ligne
            "animateRows": True,  # Ajoute des animations de déplacement
        },
        style={'height':'200px'},
    ),
    dcc.Store(id='mes-colonnes',data={'liste_colonnes':colonnes}),
    html.Div(id="output"),

])

# Callback pour afficher les informations de la ligne sélectionnée
@app.callback(
    Output("mes-colonnes", 'data'),
    Output("output", "children"),
    Input("ag-grid", "selectedRows"),
    Input("ag-grid", "columnState"),
    State("mes-colonnes",'data')
)
def display_selected_row(selected,col,state_data):
    if selected and len(selected) > 0:
        selected_row = selected[0]  # On prend la première ligne sélectionnée
        lst_col = [x['colId'] for x in col]
        state_data['liste_colonnes'] = lst_col
        return state_data,f"Vous avez sélectionné : {selected_row['token']} de famille {selected_row['famille']}, au taux de {selected_row['exchange_rate']} et d'une valeur de {selected_row['usd_balance']} $."
    return state_data,"Aucune ligne sélectionnée."

@app.callback(
  Output(component_id='graph_simple', component_property='figure'),
  Input(component_id='values-item',component_property='value'),
  Input(component_id='theme-item',component_property='value'),
  Input("ag-grid", "columnState"),
  Input('mes-colonnes','data')
)

def update_graph(values_chosen,theme_chosen,cols,state_data):
  if not cols:
     lst_col = state_data['liste_colonnes']
  else:
    lst_col = [x['colId'] for x in cols]
  fig_front = px.pie(sf, names=theme_chosen, values=values_chosen, title=f"vue des gains non realisés {theme_chosen}/{values_chosen}", labels={"value":values_chosen,"variable":theme_chosen})
  #fig = px.sunburst(sf, path=[theme_chosen], values=values_chosen, color='gainNR')
  fig_front.update_traces(textposition='inside', textinfo='percent+label')
  fig_front.update_layout(
  autosize=True,
  width=800,
  height=800,
)
  return fig_front

@app.callback(
  Output(component_id='graph_complexe', component_property='figure'),
  Input(component_id='values-item',component_property='value'),
  Input(component_id='theme-item',component_property='value'),
  Input('showmemore','on'),
  Input("ag-grid", "columnState"),
  Input('mes-colonnes','data'),
  Input('ag-grid','rowData'),
  Input('ag-grid','virtualRowData')
)

def update_graph_complexe(values_chosen,theme_chosen,show_wallets,cols,state_data,rowData,filtered):
  if not filtered:
    df = pd.DataFrame(rowData)
  else:
     df = pd.DataFrame(filtered)
  if not cols:
     lst_col = state_data['liste_colonnes']
  else:
    lst_col = [x['colId'] for x in cols]
  jf = df[df['old_usd_balance'] != 0 ]
  jf = jf[jf['usd_balance'] != 0 ]
  jf = jf[jf['exchange_rate'] != 0 ]
  #jf = df
  masque = len(lst_col) - 3
  affiche = lst_col[0:-masque]
  bonus = affiche.copy()
  bonus.append('bc')
  bonus.append('wallet')
  #fig_gain = px.sunburst(jf, path=lst_col[0:-9], values='gainNR', color='gainNR', title='Strategie/protocol/token', branchvalues='total',labels={"value":values_chosen,"variable":theme_chosen})
  #fig_gain = px.sunburst(jf, path=lst_col[0:-9], values='gainNR', color='gainNR', title='Strategie/protocol/token', branchvalues='total',labels={"value":values_chosen,"variable":theme_chosen})
  #fig_usd = px.sunburst(jf, path=lst_col[0:-9], values='usd_balance', color='gainNR', title="/".join(lst_col[0:-9]), branchvalues='total',labels={"value":values_chosen,"variable":theme_chosen})
  if show_wallets:
    fig_gain = px.sunburst(jf, path=bonus, values='gainNR', color='gainNR', title='Strategie/protocol/token')
    fig_usd = px.sunburst(jf, path=bonus, values='usd_balance', color='gainNR', title="/".join(bonus))
  else:
    fig_gain = px.sunburst(jf, path=affiche, values='gainNR', color='gainNR', title='Strategie/protocol/token')
    fig_usd = px.sunburst(jf, path=affiche, values='usd_balance', color='gainNR', title="/".join(affiche))

  dg=fig_gain.to_dict()
  du=fig_usd.to_dict()
  trace_g = []
  trace_u = []
  for trace in dg['data']:
    #trace['marker']['colors']=trace['values']
    trace_g = trace['values']
  for trace in du['data']:
    trace['marker']['colors']=trace_g
  #plotly.offline.plot(d, validate=False)
  fig_front = go.Figure(du)
  #fig_front = fig_row
  fig_front.update_traces()
  fig_front.update_layout(
  autosize=True,
  width=800,
  height=800,
)
  return fig_front

# Lancer l'application
if __name__ == '__main__':
  #app.run(debug=True,host='0.0.0.0')
  app.run(debug=True)
