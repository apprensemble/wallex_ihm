from dash.dependencies import Input, Output,State
import pandas as pd
import plotly_express as px
from app_instance import app

@app.callback(
  Output(component_id='graph_simple', component_property='figure'),
  Input(component_id='values-item',component_property='value'),
  Input(component_id='theme-item',component_property='value'),
  Input('ag-grid','virtualRowData'),
  Input('ag-grid','rowData')
)

def update_graph(values_chosen,theme_chosen,filtered,data):
  if not filtered:
    df = pd.DataFrame(data)
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