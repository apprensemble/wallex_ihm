def init_etat_col(colonnes):
  #predefined col-width
  cw = {'vision': 107, 'strategie': 146, 'protocol': 125, 'famille': 112, 'position': 119, 'bc': 110, 'wallet': 191, 'token': 168, 'ref_date_comparaison': 202, 'exchange_rate': 186, 'old_usd_balance': 217, 'usd_balance': 209, 'gainNR': 200, 'tp': 200, 'sl': 200, 'ppmax': 200, 'capital': 200, 'rr': 200, 'gainEst': 200, 'perteEst': 200}
  #auto updated cw
  cw = {c:cw[c] if c in cw else 200 for c in colonnes}
  etat_colonnes = [{'aggFunc': None, 'colId': c[0], 'flex': None, 'hide': False, 'pinned': None, 'pivot': False, 'pivotIndex': None, 'rowGroup': False, 'rowGroupIndex': None, 'sort': None, 'sortIndex': None, 'width': c[1]} for c in cw.items()]
  return etat_colonnes


def init_coldef(colonnes):
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
  return col_def

#fonctions de preparation
def creation_tableau_de_base(colonnes,ts):
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