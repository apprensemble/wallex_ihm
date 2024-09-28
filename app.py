import dash
from layout import layout
from app_instance import app
import callbacks.simple_graph
import callbacks.complex_graph
import callbacks.popup
import callbacks.tableau
import pprint


#strategie_vision_famille_position_protocol_bc



app.layout = layout

if __name__ == '__main__':
  #app.run(debug=True,host='0.0.0.0')
  app.run(debug=True)