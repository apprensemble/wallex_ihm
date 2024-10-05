from dash import html,dcc
import dash_ag_grid as dag
from assets import init_tableau as it
from assets import init_data as inid

ts = inid.ts
colonnes = inid.colonnes
#original colonnes_width

sf = it.creation_tableau_de_base(colonnes,ts)
col_def = it.init_coldef(colonnes)
etat_colonnes = it.init_etat_col(colonnes)
def get_tableau():
  return html.Div([
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
        style={'height':'600px'},
    ),
    dcc.Store(id='mes-colonnes',data={'liste_colonnes':colonnes,'initial_df':sf.to_dict('records'),'etat_colonnes':etat_colonnes}),
    html.Div(id="output"),
  ])