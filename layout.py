from dash import html
from layouts.header import get_header
from layouts.figures import get_figures
from layouts.tableau import get_tableau
from layouts.popup import get_popup

layout = html.Div([
  get_header(),
  get_figures(),
  get_tableau(),
  get_popup(),

])