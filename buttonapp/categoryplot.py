import plotly.graph_objs as go
import pandas as pd

dfPokemon = pd.read_csv('dataPokemon.csv')

listGOFunc = {
    "bar": go.Bar,
    "violin": go.Violin,
    "box": go.Box
}

def getPlot(jenisPlot,jenisPok,radioButt):
    return[listGOFunc[jenisPlot](
            x=dfPokemon[jenisPok],
            y=dfPokemon['Total'],
            text=dfPokemon['Type 2'],                        
            opacity=0.7,
            name='Total'
        ),                        
        listGOFunc[jenisPlot](
            x=dfPokemon[jenisPok],
            y=dfPokemon[radioButt],
            text=dfPokemon['Type 2'],
            opacity=0.7,
            name='Attack'
        )]                                                                                                        
                                
                            