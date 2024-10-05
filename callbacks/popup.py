from dash import ctx, no_update,html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from app_instance import app
from assets import init_data as inid

ts = inid.ts

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
                r = simulate_rr(row['token'].split("_")[-1],row['exchange_rate'],row['usd_balance'],row['native_balance'],tp,sl,ppmax,capital)
                row['tp'] = tp
                row['sl'] = sl
                row['ppmax'] = ppmax
                row['capital'] = capital
                row['rr'] = r['rr']
                row['gainEst'] = r['ge']
                row['perteEst'] = r['pe']
        return rowData
    return rowData

@app.callback(
    Output("output-simulation","children"),
    Input("row-selection-modal-launch-simulation", "n_clicks"),
    State("ag-grid","selectedRows"),
    State("tp","value"),
    State("sl","value"),
    State("ppmax","value"),
    State("capital","value"),
    State("ag-grid","rowData"),
)
def update_simulation(on_simulation,selectedRows,tp,sl,ppmax,capital,rowData):
    if selectedRows and on_simulation:
        token = selectedRows[0]['token'].split("_")[-1]
        prix = selectedRows[0]['exchange_rate']
        usd_balance = selectedRows[0]['usd_balance']
        native_balance = selectedRows[0]['native_balance']
        r = simulate_rr(token,prix,usd_balance,native_balance,tp,sl,ppmax,capital)
        return f"{r}"
    else:
        return no_update
        

def simulate_rr(token,prix,usd_balance,native_balance,tp,sl,ppmax,capital):
    ts.rr.set_capital(ppmax,capital,token)
    r = ts.rr.simulation_rr(token,tp,sl,prix,investissement=usd_balance,save_rr=True)[token]
    rr = r['rr']
    ge = r['gainEst']
    pe = r['perteEst']
    rc = ts.rr.simulation_rr(token,tp,sl,prix=prix)[token]
    taille_position = rc['taille_position']
    gec = rc['gainEst']
    pec = rc['perteEst']
    ts.rr.save_rr()
    return {"taille_position_reelle":native_balance,"rr":rr,"ge":ge,"pe":pe,"gec":gec,"pec":pec,"taille_position":taille_position}