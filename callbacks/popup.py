from dash import ctx, no_update,html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from app_instance import app

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