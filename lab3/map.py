#!/usr/bin/python

import json
import geopandas as gpd
import pandas as pd
import numpy as np

from bokeh.io import show, curdoc
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, RangeSlider, GMapOptions, CDSView, IndexFilter
from bokeh.palettes import brewer
from bokeh.layouts import row, column

df = pd.read_csv("./imdb_movie_metadata.csv")
df.loc[df['country'] == "USA", 'country'] = "United States of America"

all_years = df["title_year"].unique()
min_year = int(min(all_years))
max_year = int(max(all_years))

shapefile = "./shapefile.shp"
gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))[["name", "geometry"]]

def gen_df_range(y1, y2):
    dict_country_number_of_movies = dict()

    for i in df["country"].unique():
        dict_country_number_of_movies[i] = 0

    for index, r in df.iterrows():
        country = r['country']
        year = r['title_year']
        try:
            if len(country) > 0 and year >= y1 and year <= y2:
                dict_country_number_of_movies[country] += 1
        except TypeError as e:
            print("lmao")
        
    return pd.DataFrame(list(dict_country_number_of_movies.items()), columns=["name", "number_of_movies"])

r_df = gen_df_range(min_year, max_year)

def transform_geojson(data):

    merged = gdf.merge(r_df, left_on = 'name', right_on = 'name', how='left')
    merged['number_of_movies'] = merged['number_of_movies'].fillna(0)

    merged_json = json.loads(merged.to_json())
    return json.dumps(merged_json)

json_data = transform_geojson(r_df)

def plot_map(json_data,plot_col,title):

    geosource = GeoJSONDataSource(geojson = json_data)

    #Define a sequential multi-hue color palette.
    palette = brewer['Reds'][8]
    palette = palette[::-1]
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 21)

    tick_labels = {'0': '0', '5': '5', '10':'10', '15':'15', '20':'20', '21':'>20'}

    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
        border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

    p = figure(title = title, plot_height = 600 , plot_width = 950, toolbar_location = None)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    p.patches('xs','ys', source = geosource,fill_color = {'field' :plot_col, 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)

    p.add_layout(color_bar, 'below')
    #slider = RangeSlider(title="Year: ", start=min_year, end=max_year, value=(0, 10), step=10)
    #slider.on_change('value', callback)
    #layout = column(p, slider)
    curdoc().add_root(p)

plot_map(json_data, "number_of_movies", "Number of movies")
