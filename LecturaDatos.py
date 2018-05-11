import pandas as pd
from shapely.geometry import Polygon
from shapely.geometry import Point

# Obtenemos un DataFrame con los datos de los barrios de Caceres
barrios = pd.read_json('Barrio.json', encoding = 'utf8')
poligonos_barrios = []
nombre_barrios = []

# Obtenemos un Dataframe con los datos de las farolas de Caceres
farolas = pd.read_json('Farola.json', encoding = 'utf8')
resultado = pd.DataFrame()

# Insertamos los datos de barrios y distritos
for barrio in barrios['results']['bindings']:
    i = 0
    lats = []
    lons = []
    nombre_barrios.append({'barrio': barrio['rdfs_label']['value'], 'distrito': barrio['om_perteneceADistrito']['value']})
    poligono = Polygon([[p[1], p[0]] for p in barrio['locn_geometry']])
    poligonos_barrios.append(poligono)

# Comprobamos en que poligono (barrio) se encuentra ubicado la farola, recorriendo todos los poligonos
# y en caso de no pertenecer a ninguno (Carretera de la montaña) nos dira que pertenece a un barrio desconocido
for index, row in farolas.iterrows():
    point = Point(row['geo_lat'], row['geo_long'])
    ha_encontrado_punto = False
    for id, pol in enumerate(poligonos_barrios):
        if point.within(pol):
            b = nombre_barrios[id]['barrio']
            d = nombre_barrios[id]['distrito']
            resultado = resultado.append({'barrio': b, 'distrito': d}, ignore_index=True)
            ha_encontrado_punto=True
    if not ha_encontrado_punto:
        desconocido = 'Desconocido'
        resultado = resultado.append({'barrio': desconocido, 'distrito': desconocido}, ignore_index=True)

# Concatenamos los dos DataFrames en horizontal (uno a la derecha del otro)
farolas = pd.concat([farolas, resultado], axis=1)

# Exportamos el fichero en csv para que sea facilmente reconocible por Weka
farolas.to_csv('Farolas.csv', encoding='utf8', index=False)

