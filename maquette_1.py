import dash
from dash import ctx, no_update,html,dcc
import dash_bootstrap_components as dbc
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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
# Exemple de dataframe
#colonnes = ['','','token','famille','exchange_rate','old_usd_balance','usd_balance','gainNR']
#colonnes = ['vision','strategie','protocol','famille','position','bc','wallet','token','exchange_rate','old_usd_balance','usd_balance','gainNR']
colonnes = ['vision','strategie','protocol','famille','position','bc','wallet','token','ref_date_comparaison','gainNR','old_usd_balance','usd_balance','native_balance','exchange_rate','tp','sl','ppmax','capital','rr','gainEst','perteEst']
#original colonnes_width
cw = {'vision': 107, 'strategie': 146, 'protocol': 125, 'famille': 112, 'position': 119, 'bc': 110, 'wallet': 191, 'token': 168, 'ref_date_comparaison': 202, 'exchange_rate': 186, 'old_usd_balance': 217, 'usd_balance': 209, 'gainNR': 200, 'tp': 200, 'sl': 200, 'ppmax': 200, 'capital': 200, 'rr': 200, 'gainEst': 200, 'perteEst': 200}
#auto updated cw
cw = {c:cw[c] if c in cw else 200 for c in colonnes}
etat_colonnes = [{'aggFunc': None, 'colId': c[0], 'flex': None, 'hide': False, 'pinned': None, 'pivot': False, 'pivotIndex': None, 'rowGroup': False, 'rowGroupIndex': None, 'sort': None, 'sortIndex': None, 'width': c[1]} for c in cw.items()]


#fonctions de preparation
def creation_tableau_de_base(colonnes):
    df = ts.get_full_df_with_rr()
    df['old_usd_balance'] = df['ref_exchange_rate'] * df['native_balance'] 
    df['gainNR'] = df['usd_balance'] - df['old_usd_balance']
    df.loc[df['gainNR'] == 0, 'gainNR'] = 0.000001
    df.loc[df['usd_balance'] == 0, 'usd_balance'] = 0.000001
    df.loc[df['old_usd_balance'] == 0, 'old_usd_balance'] = 0.000001
    df['ref_date_comparaison'] = df['ref_date_comparaison'].apply(ts.convert_seconds_to_rdate)
    #sf = df.groupby(['token','famille','usd_balance','pct'])['gainNR'].sum().reset_index()
    #sf = df.groupby(['token','famille','exchange_rate','old_usd_balance','usd_balance'])['gainNR'].sum().reset_index()
    sf = df.groupby(colonnes[0:-1])[colonnes[-1]].sum().reset_index()
    #sf['usd_balance'] = round(sf['usd_balance'],2)
    #sf['gainNR'] = round(sf['gainNR'],2)
    return sf

sf = creation_tableau_de_base(colonnes)
col_def = []
for col in colonnes:
    if col == "sl":
       col_def.append(
        {
        'headerName': 'sl',
        'field': 'sl',
        'cellStyle': {
            # Set of rules
            "styleConditions": [
                {
                    "condition": "params.value > params.data.exchange_rate",
                    "style": {"backgroundColor": "sandybrown"},
                },
            ],
            # Default style if no rules apply
            "defaultStyle": {"backgroundColor": "white"},
        }
    }
       )
    elif col == "tp":
       col_def.append(
        {
        'headerName': 'tp',
        'field': 'tp',
        'cellStyle': {
            # Set of rules
            "styleConditions": [
                {
                    "condition": "params.value < params.data.exchange_rate",
                    "style": {"backgroundColor": "white"},
                },
            ],
            # Default style if no rules apply
            "defaultStyle": {"backgroundColor": "mediumaquamarine"},
        }
    }
       )
    elif col == "usd_balance":
       col_def.append(
        {
        'headerName': 'usd_balance',
        'field': 'usd_balance',
        'cellStyle': {
            # Set of rules
            "styleConditions": [
                {
                    "condition": "params.value >= params.data.old_usd_balance",
                    "style": {"backgroundColor": "mediumaquamarine"},
                },
            ],
            # Default style if no rules apply
            "defaultStyle": {"backgroundColor": "lightPink"},
        }
    }
       )
    else:
      col_def.append({"headerName": col, "field": col })

# Disposition de l'application
app.layout = html.Div([
    html.Div(className='row', children='Wallex: Maquette1',
                style={'textAlign': 'center', 'color': 'black', 'fontSize': 30}), 
        daq.BooleanSwitch(id='showmemore', on=False),
        html.Button("Reset Filters", id="reset-button", n_clicks=0),
        html.Div(className='simple',style={'display': 'flex', 'justify-content': 'space-around'},children=[
          dcc.Loading(
        id="loading-sunburst",
        type="circle",
        children=[dcc.Graph(figure={},id='graph_complexe')]),
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
    dcc.Slider(2, 8, 1,
               value=3,
               id='profondeur'
    ),
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
    dcc.Store(id='mes-colonnes',data={'liste_colonnes':colonnes,'initial_df':sf.to_dict('records')}),
    html.Div(id="output"),

        dbc.Modal(
            [
                dbc.ModalHeader("More information about selected row"),
                dbc.ModalBody(id="row-selection-modal-content"),
                html.Div([
                dcc.Input(id='tp', type='number',  min=0, max=1000000, placeholder="tp",style={'marginLeft':'10px','inline':'true'}),
                dcc.Input(id='sl', type='number',  min=0, max=1000000, placeholder="sl",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
                dcc.Input(id='ppmax', type='number',  min=0, max=1000000, placeholder="ppmax",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
                dcc.Input(id='capital', type='number',  min=0, max=1000000, placeholder="capital",style={'marginRight':'10px','marginLeft':'10px','inline':'true'}),
            html.Iframe(srcDoc=open("assets/tradingView.html").read(), 
                width='100%', 
                height='350'),
            ]),
                dbc.ModalFooter(dbc.Button("Close", id="row-selection-modal-close", className="ml-auto")),
            ],
            id="row-selection-modal",
        ),
])

@app.callback(
  Output(component_id='graph_simple', component_property='figure'),
  Input(component_id='values-item',component_property='value'),
  Input(component_id='theme-item',component_property='value'),
  Input('ag-grid','virtualRowData'),
  State('mes-colonnes','data')
)

def update_graph(values_chosen,theme_chosen,filtered,data):
  if not filtered:
    df = pd.DataFrame(data['initial_df'])
  else:
    df = pd.DataFrame(filtered)
  titre_suffixe = f"- total = {round(df['usd_balance'].sum(),2)} / gainNR = {round(df['gainNR'].sum(),2)}"
  fig_front = px.pie(df, names=theme_chosen, values=values_chosen, title=f"vue simple {theme_chosen}/{values_chosen} {titre_suffixe}", labels={"value":values_chosen,"variable":theme_chosen})
  #fig = px.sunburst(sf, path=[theme_chosen], values=values_chosen, color='gainNR')
  fig_front.update_traces(textposition='inside', textinfo='percent+label')
  fig_front.update_layout(
  autosize=True,
  width=800,
  height=600,
  #paper_bgcolor='rgba(0,0,0,0)',  # Transparent background to match CSS
  #plot_bgcolor='rgba(0,0,0,0)'    # Transparent plot area background
)
  return fig_front
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
  Output(component_id='graph_complexe', component_property='figure'),
  Input('profondeur',component_property='value'),
  Input('showmemore','on'),
  Input("ag-grid", "columnState"),
  Input('mes-colonnes','data'),
  Input('ag-grid','rowData'),
  Input('ag-grid','virtualRowData')
)

def update_graph_complexe(profondeur,show_wallets,cols,state_data,rowData,filtered):

  if not filtered:
    df = pd.DataFrame(rowData)
    state_data['data'] = rowData
  else:
    df = pd.DataFrame(filtered)
    state_data['data'] = filtered
  if not cols:
    lst_col = state_data['liste_colonnes']
  else:
    lst_col = [x['colId'] for x in cols]
  jf = df.loc[(df['old_usd_balance'] != 0) & (df['usd_balance'] != 0) & (df['exchange_rate'] != 0) ]
  #jf = df
  masque = len(lst_col) - profondeur
  affiche = lst_col[0:-masque]
  bonus = affiche.copy()
  bonus.append('bc')
  bonus.append('wallet')
  titre_suffixe = f" - total = {round(jf['usd_balance'].sum(),2)} / gainNR = {round(jf['gainNR'].sum(),2)}"
  titre_affiche = "/".join(affiche)
  titre_affiche += titre_suffixe
  titre_bonus = "/".join(bonus)
  titre_bonus += titre_suffixe
  #fig_gain = px.sunburst(jf, path=lst_col[0:-9], values='gainNR', color='gainNR', title='Strategie/protocol/token', branchvalues='total',labels={"value":values_chosen,"variable":theme_chosen})
  #fig_gain = px.sunburst(jf, path=lst_col[0:-9], values='gainNR', color='gainNR', title='Strategie/protocol/token', branchvalues='total',labels={"value":values_chosen,"variable":theme_chosen})
  #fig_usd = px.sunburst(jf, path=lst_col[0:-9], values='usd_balance', color='gainNR', title="/".join(lst_col[0:-9]), branchvalues='total',labels={"value":values_chosen,"variable":theme_chosen})
  if show_wallets:
    fig_gain = px.sunburst(jf, path=bonus, values='gainNR', color='gainNR', title='Strategie/protocol/token')
    fig_usd = px.sunburst(jf, path=bonus, values='usd_balance', color='gainNR', title=titre_bonus)
  else:
    fig_gain = px.sunburst(jf, path=affiche, values='gainNR', color='gainNR', title='Strategie/protocol/token')
    fig_usd = px.sunburst(jf, path=affiche, values='usd_balance', color='gainNR', title=titre_affiche)

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
  height=600,
  #paper_bgcolor='rgba(0,0,0,0)',  # Transparent background to match CSS
  #plot_bgcolor='rgba(0,0,0,0)'    # Transparent plot area background
)
  return fig_front


@app.callback(
    Output("row-selection-modal", "is_open"),
    Output("row-selection-modal-content", "children"),
    Input("ag-grid", "selectedRows"),
    Input("row-selection-modal-close", "n_clicks"),
)
def open_modal(selection, _):
    if ctx.triggered_id == "row-selection-modal-close":
        return False, no_update
    if selection:
        return True, "You selected " + ", ".join(
            [
                f"{s['token']} of family {s['famille']} at price {s['exchange_rate']} and quantity {s['native_balance']}"
                f"for a total of {s['usd_balance']}"
                for s in selection
            ]
        )

    return no_update, no_update

@app.callback(
    Output('ag-grid', 'filterModel'),
    Output('reset-button', 'n_clicks'),
    Output('ag-grid', 'columnState'),
    Input('reset-button', 'n_clicks'),
    Input('ag-grid', 'filterModel'),
    Input('ag-grid', 'columnState')
)
def reset_filters(n_clicks,options,cols):
  if n_clicks > 0:
    options = {}
    cols = etat_colonnes
    n_clicks = 0
    return options,n_clicks,cols
  # If no clicks, return None (no changes)
  return no_update, no_update, no_update
# Lancer l'application

#def add_tp_sl(tp,sl,ppmax):
if __name__ == '__main__':
  #app.run(debug=True,host='0.0.0.0')
  app.run(debug=True)
