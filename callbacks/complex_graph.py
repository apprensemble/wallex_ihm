from dash import no_update
from dash.dependencies import Input, Output
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
from app_instance import app

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
  else:
    df = pd.DataFrame(filtered)
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
    Output('ag-grid', 'filterModel'),
    Output('reset-button', 'n_clicks'),
    Output('ag-grid', 'columnState'),
    Input('reset-button', 'n_clicks'),
    Input('ag-grid', 'filterModel'),
    Input('ag-grid', 'columnState'),
    Input('mes-colonnes', 'data')
)
def reset_filters(n_clicks,options,cols,data):
  if n_clicks > 0:
    options = {}
    cols = data['etat_colonnes']
    n_clicks = 0
    return options,n_clicks,cols
  # If no clicks, return None (no changes)
  return no_update, no_update, no_update
# Lancer l'application
