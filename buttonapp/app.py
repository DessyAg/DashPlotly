import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from categoryplot import dfPokemon, getPlot
from dash.dependencies import Input, Output

color_set = ['#000000','#FCE63D']

app = dash.Dash(__name__)

def generate_table(dataframe, max_rows=10) :
    return html.Table(
         # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(str(dataframe[col][i])) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.title = 'Dashboard Pokemon'

# LAYOUT
app.layout = html.Div(children=[
    html.H1(children='Dashboard Pokemon (dari Bronson)',className='titleDashboard'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Pokemon Dataset', value='tab-1',children=[
            html.Div([
                html.H1('Data Pokemon', className='h1'),
                generate_table(dfPokemon)
            ])
        ]),
        dcc.Tab(label='Scatter Plot', value='tab-2',children=[
            html.Div([
                html.H1('Scatter Plot Pokemon', className='h1'),
                dcc.Graph(
                    id='scatterPlot',
                    figure={
                        'data': [
                            go.Scatter(
                                x=dfPokemon[dfPokemon['Legendary'] == col]['Attack'],
                                y=dfPokemon[dfPokemon['Legendary'] == col]['Defense'],
                                mode='markers',
                                marker=dict(color=color_set[i], size=10, line={'width':0.5,'color': 'white'}),
                                name=str(col)
                            ) for col, i in zip(dfPokemon['Legendary'].unique(), range(2))
                        ],
                        'layout': go.Layout(
                            xaxis= {'title': 'Attack'},
                            yaxis={'title': 'Defense'},
                            margin={ 'l': 40, 'b': 40, 't': 10, 'r': 10 },
                            hovermode='closest'
                        )
                    }
                )
            ])
        ]),
        dcc.Tab(label='Categotical Plot', value='tab-3',children=[
            html.Div([
                html.H1('Categorical Plot Pokemon', className='h1'),
                html.Div(children=[
                    html.Div([
                        dcc.Dropdown(
                            id='jenisPlot',
                            options=[{'label': i.capitalize(), 'value': i} for i in ['bar','box','violin']],
                            value='bar',
                            style={'width':'300px'}
                        )
                    ],className='col-6'),
                    html.Div([
                        dcc.Dropdown(
                            id='jenisPok',
                            options=[{'label': i.capitalize(), 'value': i} for i in ['Generation','Legendary']],
                            value='Generation',
                            style={'width':'300px'}
                        )
                     ],className='col-6'),
                    html.Div([
                        dcc.RadioItems(
                            id='radioButt',
                            options=[{'label': i, 'value': i} for i in ['HP','Attack', 'Defense','Sp. Atk','Sp. Def','Speed']],
                            value='Attack',
                            labelStyle={'display': 'inline-block'}
                        )
                    ],className='col-6')
                ],className='row'),
                dcc.Graph(
                    id='categoricalPlot',
                )
            ])
        ]),
    ], style={
        'fontFamily': 'system-ui'
    }, content_style={
        'fontFamily': 'Arial',
        'borderBottom': '1px solid #d6d6d6',
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'padding': '44px'
    })
], style={
    'maxWidth': '1200px',
    'margin': '0 auto'
})

@app.callback(
    Output(component_id='categoricalPlot', component_property='figure'),
    [Input(component_id='jenisPlot', component_property='value'),
    Input(component_id='jenisPok', component_property='value'),
    Input(component_id='radioButt', component_property='value')]
)
def update_graph_categorical(jenisPlot,jenisPok,radioButt):
    return {
        'data': getPlot(jenisPlot,jenisPok,radioButt),
        'layout': go.Layout(
                    xaxis={'title':jenisPok},
                    yaxis={'title':radioButt},
                    margin={'l':40,'b':40,'t':10,'r':10},
                    # legend={'x':0, 'y':1},
                    hovermode='closest',boxmode='group',violinmode='group'
                )
    }
if __name__ == '__main__':    
    app.run_server(debug=True,port=1997)