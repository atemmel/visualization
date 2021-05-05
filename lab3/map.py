#!/usr/bin/python

import json
import geopandas as gpd
import pandas as pd

from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer

df = pd.read_csv("./imdb_movie_metadata.csv")
#df = df.dropna(how='any')
df.loc[df['country'] == "USA"] = "United States of America"
dict_country_number_of_movies = dict()

for i in df["country"].unique():
    dict_country_number_of_movies[i] = 0

for index, row in df.iterrows():
    country = row['country']
    try:
        if len(country) > 0:
            dict_country_number_of_movies[country] += 1
    except TypeError as e:
        print("lmao")
    
r_df = pd.DataFrame(list(dict_country_number_of_movies.items()), columns=["name", "number_of_movies"])
#print(r_df)

shapefile = "./shapefile.shp"
gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))[["name", "geometry"]]

merged = gdf.merge(r_df, left_on = 'name', right_on = 'name', how='left')
merged['number_of_movies'] = merged['number_of_movies'].fillna(0)

print(merged)

merged_json = json.loads(merged.to_json())
json_data = json.dumps(merged_json)

def plot_map(json_data,plot_col,title):

    geosource = GeoJSONDataSource(geojson = json_data)

    #Define a sequential multi-hue color palette.
    palette = brewer['Reds'][8]
    palette = palette[::-1]
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 1)

    tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}

    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

    p = figure(title = title, plot_height = 600 , plot_width = 950, toolbar_location = None)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    p.patches('xs','ys', source = geosource,fill_color = {'field' :plot_col, 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)

    p.add_layout(color_bar, 'below')

    #Display figure.
    show(p)

plot_map(json_data, "number_of_movies", "b")
