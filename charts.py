import json

import plotly.utils

from main import calc_all
from data_collection import cases_list, get_SIDRV
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt

the_dict = calc_all(1000000, 30)


def make_plot(location, days_ago=60):
    master = {'days': [], 'infected': [], 'deaths': [], 'recovered': [], 'active': []}
    deceased = cases_list('deceased', days_ago, location)[location]
    infected = cases_list('infected', days_ago, location)[location]
    recovered = cases_list('recovered', days_ago, location)[location]
    active = []
    for i in range(days_ago):
        SIDRV = get_SIDRV(i, location)
        master['active'].append(SIDRV['a']['confirmed'])
    for i in range(-days_ago, 0):
        master['days'].append(i)
    for case in cases_list('deceased', days_ago, location)[location]:
        master['deaths'].append(case)

    for key, values in the_dict.items():
        master['days'].append(key)
        master['active'].append(values[location]['infected'])
        master['deaths'].append(values[location]['dead'])
        try:
            master['vaccinated'].append(values[location]['vaccinated'])
        except KeyError:
            pass

    plot = go.Figure()

    plot.add_trace(go.Scatter(
        name='Deaths',
        x=master['days'],
        y=master['deaths'],
        stackgroup='one'
    ))

    plot.add_trace(go.Scatter(
        name='Infected',
        x=master['days'],
        y=master['active'],
        stackgroup='one'
    )
    )

    plot.show()
    # fig = px.line(master, x='days', y='count')
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return graphJSON


if __name__ == '__main__':
    make_plot('DL')

# function to return graph for a given state
