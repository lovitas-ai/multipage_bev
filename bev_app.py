import dash
from dash import dcc, html, Output, Input, State
import dash_labs as dl
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    plugins=[dl.plugins.pages],
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)

for page in dash.page_registry.values():
    print("Name ", page["name"])
    print("Pfad ", page["path"])


header=dbc.Row([
            dbc.Col(html.H1("Bevölkerung in Bayern Dashboard",
            className='text-center text-primary mb-4 '), width={'size':9,'offset':1,'order':1})
            ], justify = 'start')



navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    dbc.Col(dbc.NavbarBrand("Startseite", className="ms-2")),
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.Row(
                [
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.DropdownMenu([
                                    dbc.DropdownMenuItem("Kreise",href="/kreis/bevkreis"),
                                    dbc.DropdownMenuItem("Gemeinden",href="/gem/bevgem")],
                                
                                nav=True,label="Bevölkerung",)),
                                dbc.NavItem(
                                    dbc.DropdownMenu(dbc.DropdownMenuItem("Kreise",href="/land/histo"),nav=True,label="Wanderung",),
                                    # add an auto margin after page 2 to
                                    # push later links to end of nav
                                    className="me-auto",
                                ),
                                dbc.NavItem(dbc.NavLink("Hilfe")),
                                dbc.NavItem(dbc.NavLink("mehr Informationen", href="https://www.statistik.bayern.de/",target="_blank",external_link=True)),
                            ],
                            # make sure nav takes up the full width for auto
                            # margin to get applied
                            className="w-100",
                        ),
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ],
                # the row should expand to fill the available horizontal space
                className="flex-grow-1",
            ),
        ],
        fluid=True,
    ),
    dark=False,
    color="white",
    className="border",
)






app.layout = dbc.Container(
    [header,
        navbar,
        dl.plugins.page_container
    ],
    fluid=True,
)



if __name__ == "__main__":
    app.run_server(debug=True)