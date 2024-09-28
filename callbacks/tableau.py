from dash.dependencies import Input, Output,State
from app_instance import app
# Callback pour afficher les informations de la ligne sélectionnée
@app.callback(
    Output("output", "children"),
    Input("ag-grid", "selectedRows"),
    Input("ag-grid", "columnState"),
)
def display_selected_row(selected,col):
    if selected and len(selected) > 0:
        selected_row = selected[0]  # On prend la première ligne sélectionnée
        lst_col = [x['colId'] for x in col]
        return f"Vous avez sélectionné : {selected_row['token']} de famille {selected_row['famille']}, au taux de {selected_row['exchange_rate']} et d'une valeur de {selected_row['usd_balance']} $."
    return "Aucune ligne sélectionnée."
