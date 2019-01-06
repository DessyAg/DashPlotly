import plotly.graph_objs as go
import pandas as pd

dfPokemon = pd.read_csv('Pokemon.csv')


listGoFunc ={

    'bar' : go.Bar,
    'violin':go.Violin,
    'box':go.Box
}

def getPlot(jenis,xax,radioButt):
    return [listGoFunc[jenis](
                x=dfPokemon[xax],
                y=dfPokemon['Total'],
                text=dfPokemon['Type 2'],
                opacity=0.7,
                name='Total'
            ),

            listGoFunc[jenis](
                x=dfPokemon[xax],
                y=dfPokemon[radioButt],
                text=dfPokemon['Type 2'],
                opacity=0.7,
                name='Attack'
            )]

