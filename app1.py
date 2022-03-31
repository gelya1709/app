import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input


data = pd.read_csv("stat_flows.csv")


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Customer Analytics: Understand Your Customers!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="✌️", className="header-emoji"),
                html.H1(
                    children="Customer Flows Analytics", className="header-title"
                ),
                html.P(
                    children="Visualisation tool for analysis customer flows"
                    " and the number of promotions which are held in 2019 year"
                    " in retail supermarket chain",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Customer Flows", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": flows, "value": flows}
                                for flows in np.sort(data.flows.unique())
                            ],
                            value="sleeping_champions",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                
                
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
	html.Div(
                  children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                  ),
		   className="card",      
                ),
                
            ],
            className="wrapper",
        ),
    ]
)


@app.callback([Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("region-filter", "value"),
       
    ],
)
def update_charts(flows):
    mask = (data.flows == flows)
    
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["week"].to_list(),
                "y": filtered_data["coefficient"].to_list(),
                "type": "lines",
               #"hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Coefficients of the chosen flow",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "%", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
	
    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["week"].to_list(),
                "y": filtered_data["count_promo"].to_list(),
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Number of promotions", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True,
                   host='127.0.0.1')

