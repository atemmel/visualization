#!/usr/bin/python

import pandas as pd
import numpy as np

from bokeh.plotting import figure, show
from bokeh.layouts import gridplot

df = pd.read_csv("./imdb_movie_metadata.csv")
df = df.dropna(how='any')

all_years = df["title_year"].unique()
first_year = int(min(all_years))
last_year = int(max(all_years))

print(first_year, last_year)

x = np.arange(first_year,last_year + 1, 1)
y1 = [0] * len(x)
y2 = [0] * len(x)
y3 = [0] * len(x)

for index, row in df.iterrows():
    try:
        title_year = int(row['title_year'])
        gross = row['gross']
        score = row['imdb_score']

        i = title_year - first_year
        y1[i] += 1
        y2[i] += gross
        y3[i] += score
    except ValueError as e:
        print("Skipped NaN value")

for i in range(len(y3)):
    if y1[i] > 0:
        y3[i] /= y1[i]

# create a new plot with a title and axis labels
s1 = figure(title="Year", x_axis_label='x', y_axis_label='y')

# add a line renderer with legend and line thickness to the plot
s1.line(x, y1, legend_label="Amount of Movies produced.", line_width=2)

s2 = figure(title="Year", x_axis_label='x', y_axis_label='y', x_range=s1.x_range)

s2.circle(x, y2, legend_label="Total Gross", size=10)

s3 = figure(title="Year", x_axis_label='x', y_axis_label='y', x_range=s1.x_range)

s3.line(x, y3, legend_label="Average IMDB score", line_width=2)

# show the results
#show(s1)
p = gridplot([[s1, s2, s3]], toolbar_location=None)
show(p)

"""
# create a new plot
s1 = figure(plot_width=250, plot_height=250, title=None)
s1.circle(x, y0, size=10, color="navy", alpha=0.5)

# create a new plot and share both ranges
s2 = figure(plot_width=250, plot_height=250, x_range=s1.x_range, y_range=s1.y_range, title=None)
s2.triangle(x, y1, size=10, color="firebrick", alpha=0.5)

# create a new plot and share only one range
s3 = figure(plot_width=250, plot_height=250, x_range=s1.x_range, title=None)
s3.square(x, y2, size=10, color="olive", alpha=0.5)

p = gridplot([[s1, s2, s3]], toolbar_location=None)
"""
