import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output
from categoryplot import dfPokemon,getPlot


# untuk link database csv
# dfPokemon = pd.read_csv('Pokemon.csv')

color_set=['#000000','#FCE63D',]
esti_func ={
    'Count':len,
    'Sum':sum,
    'Average':np.mean,
    'Standard Deviation' :np.std
}

disabledEsti ={
    'Count':True,
    'Sum':False,
    'Average':False,
    'Standard Deviation' :False
}


# max,rows untuk menampilkan data default 10
#dataframe = untuk list comprehensip
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        #knapa ada str=> karena datanya boolean 
        [html.Tr([
            html.Td(str(dataframe.iloc[i][col])) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


print(dfPokemon.head())

#app =sebuah objek 
app = dash.Dash(__name__) 


#html.Div (terluar)
app.title ='Dashboard Pokemon'
app.layout = html.Div(children=[
    html.H1(children='Dashboard Pokemon', className='titledashboard'),
    #tabs = untuk global sedangankan tab = untuk satu baris
    dcc.Tabs(id="tabs", value='tab-1', children=[
        
        dcc.Tab(label='Pokemon Dataset', value='tab-1', children=[
            html.Div([
                html.H1('Data Pokemon', className='h1'),
                #html.table di return dari atas
                generate_table(dfPokemon)
            ])
        ]),
        
        dcc.Tab(label='Scatter Plot', value='tab-2',children=[
            html.Div([
                html.H1('Scatter Plot Pokemon', className='h1'),

                dcc.Graph(
                    id='ScatterPlot',
                    figure={
                        'data': [
                            #go itu objek kenudian memiliki method scatter
                            go.Scatter(
                                x=dfPokemon[dfPokemon['Legendary'] == col]['Attack'],
                                y=dfPokemon[dfPokemon['Legendary'] == col]['Defense'],
                                mode='markers',
                                marker=dict(color=color_set[i], size=10, line={'width' :0.5, 'color':'white'}),
                                name=str(col)
                            ) for col, i in zip(dfPokemon['Legendary'].unique(),range(2))
                        ], 
                        'layout':go.Layout(
                                xaxis={'title' :' Attack'},
                                yaxis={'title': 'Defense'},
                                margin={'l' : 40, 'b':40, 't':10, 'r':10},
                                #fungsi untuk menangkap data yang di zoom
                                hovermode='closest'
                        )

                    }
                )
            ])
        ]),

        dcc.Tab(label='Categorical Plot', value='tab-3', children=[
            html.Div([
                html.H1('Categorical Plot Pokemon', className='h1'),
                #untuk tambah kolom input
                html.Div(children=[
                    #untuk buat dropdown
                    html.Div([
                        dcc.Dropdown(
                            id='jenisPlot',
                            options=[{'label': i.capitalize(), 
                            'value': i} for i in ['bar','box','violin']],
                            #default value nya adalah bar
                            value='bar'
                            #style dropdown kecil
                            # style={'width': '300px'}
                        )   
                    ],className ='col-6'),  

                    html.Div([
                        dcc.Dropdown(
                            id='xax',
                            options=[{'label': i.capitalize(), 'value': i} for i in ['Generation','Legendary']],
                            value='Generation' 
                        )   
                    ],className ='col-6'),

                    html.Div([
                        dcc.RadioItems(
                            id='radioButt',
                            options=[{'label': i, 'value': i} for i in ['HP','Attack', 'Defense','Sp. Atk','Sp. Def','Speed']],
                            value='Attack',
                            labelStyle={'display': 'inline-block'}
                        )
                    ],className='col-6')
                ],className ='row'),

                dcc.Graph(
                    id='categoricalPlot',
                )
                
            ])
        ]),

        dcc.Tab(label='Pie Chart', value='tab-4', children=[
            html.Div([
                html.H1('Pie Chart Pokemon', className='h1'),
                #untuk tambah kolom input
                html.Div(children=[
                    #untuk buat dropdown
                    html.Div([
                        html.P('Category :'),
                        dcc.Dropdown(
                            id='catFilterPie',
                            options=[{'label': i.capitalize(),'value': i} for i in ['Generation','Legendary']],
                            value='Generation'
                        )   
                    ],className ='col-4'),  

                    html.Div([
                        html.P('Estimator :'),
                        dcc.Dropdown(
                            id='estiFilterPie',
                            options=[{'label': i,'value': i} for i in ['Count','Sum','Average','Standard Deviation']],
                            value='Count'
                        )   
                    ],className ='col-4'),  

                    html.Div([
                        html.P('Column :'),
                        dcc.Dropdown(
                            id='colFilterPie',
                            options=[{'label': i,'value': i} for i in dfPokemon.describe().drop(['#','Generation'],axis=1).columns],
                            value='Total'
                        )   
                    ],className ='col-4'),   
                ],className ='row'),

                dcc.Graph(
                    id='pieChart',
                )
                
            ])
        ])




       #merubah untuk dari luar tab nya 
    ], style={
        'fontFamily':'system-ui'
        #meruabah untuk dari dalam tab nya
    }, content_style={
        'font-family': 'Arial',
        'borderBottom':'1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'borderLeft': '1px solid #d6d6d6',
        #padding = jarak border ke content
        'padding': '44px'

    })
], style={
    'maxWidth': '1200px',
    'margin' : '0 auto'

})

#list comprehesion
@app.callback(
    Output(component_id='categoricalPlot', component_property='figure'),
    
    [Input(component_id='jenisPlot', component_property='value'),
    Input(component_id='xax', component_property='value'),
    Input(component_id='radioButt',component_property='value')]
  
    
)
def update_graph_categorical(jenisPlot,xax,radioButt):
    return {
        'data':getPlot(jenisPlot,xax,radioButt),
        'layout':go.Layout(
                    xaxis={'title': xax},
                    yaxis={'title': radioButt},
                    margin=dict(l=40,b=40,t=10,r=10),
                    hovermode='closest',
                    boxmode ='group',
                    violinmode='group'
                    ),
    }


@app.callback(
    Output(component_id='pieChart', component_property='figure'),
    [Input(component_id='catFilterPie', component_property='value'),
    Input(component_id='estiFilterPie', component_property='value'),
    Input(component_id='colFilterPie', component_property='value')]   
)

def update_graph_pie(cat,esti,col):
    listlabel =(dfPokemon[cat].unique())
    listlabel.sort()
    

    return {
        'data':[
            #go pie = satu karena pie chart hanya satu
            go.Pie(
                labels=listlabel,
                # labels=list(dfPokemon[cat].unique()).sort(),
                #untuk menghitung jumlah panjang data
                values=[esti_func[esti](dfPokemon[dfPokemon[cat] == item][col]) for item in listlabel],
                textinfo='value',
                hoverinfo='label+percent',
                marker=dict(
                    line=dict(color='black', width=2)
                ),
                sort=False
            )
        ],

        'layout':go.Layout(
                    # xaxis={'title': xax},
                    # yaxis={'title': 'Total Stat'},
                    margin=dict(l=40,b=40,t=10,r=10),
                    #legend = dikiri atas
                    legend={'x':0,'y':1}
                    ),
    }

# @app.callback(
#     Output(component_id='categoricalPlot', component_property='figure'),
#     [Input(component_id='jenisPlot', component_property='value')]
    
# )

#disabled untuk count
@app.callback(

    Output('colFilterPie','disabled'),
    [Input('estiFilterPie','value')]
)

def update_ddl_cool(esti):
    return disabledEsti[esti]


if __name__ == '__main__':
    #run server on port 1997
    # debug= True for auto restart if code edited
    # port can change anytime , if we have 3 dashboard able to diffrent port 
    app.run_server(debug=True, port=1997)