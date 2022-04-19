from importlib.resources import path
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

content = [html.H2("Startseite"), 
            html.P("Hier könnten Verlinkungen zu den Unterseiten stehen"),
            html.P("Aktuell ist nur Bevölkerung und dort Gemeinden und Kreise gefüllt."),
            html.P("Aber es könnten alle Bevölkerungsstatistiken über Dropdowns erfasst werden"),
            html.P("Unter 'mehr Information' kommt man zum LfStat"),]

layout = html.Div([
   dbc.Row(
       dbc.Col(content, width={"size": 8, "offset": 1}),
       align="center"
   )
])