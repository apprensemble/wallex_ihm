from dash import ctx, no_update,html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from app_instance import app

@app.callback(
    Output("row-selection-modal", "is_open"),
    Output("row-selection-modal-content", "children"),
    Output("tp","value"),
    Output("sl","value"),
    Output("ppmax","value"),
    Output("capital","value"),
    Input("ag-grid", "selectedRows"),
    Input("row-selection-modal-close", "n_clicks"),
)
def open_modal(selection, _):
    if ctx.triggered_id == "row-selection-modal-close":
        return False, no_update, no_update, no_update, no_update, no_update
    if selection:
        return True, "You selected " + ", ".join(
            [
                f"{s['token']} of family {s['famille']} at price {s['exchange_rate']} and quantity {s['native_balance']}"
                f"for a total of {s['usd_balance']}"
                for s in selection
            ]
        ),selection[0]['tp'],selection[0]['sl'],selection[0]['ppmax'],selection[0]['capital']

    return no_update, no_update, no_update, no_update, no_update, no_update

@app.callback(
    Output("ag-grid","rowData"),
    Input("row-selection-modal-close", "n_clicks"),
    State("ag-grid","selectedRows"),
    State("tp","value"),
    State("sl","value"),
    State("ppmax","value"),
    State("capital","value"),
    State("ag-grid","rowData"),
)
def update_tableau(on_click,selectedRows,tp,sl,ppmax,capital,rowData):
    if selectedRows and on_click:
        row_to_update = selectedRows[0]
        for row in rowData:
            if row == row_to_update:
                row['tp'] = tp
                row['sl'] = sl
                row['ppmax'] = ppmax
                row['capital'] = capital
        return rowData
    return rowData
