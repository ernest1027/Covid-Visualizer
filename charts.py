from main import calc_all
from data_collection import cases_list
import plotly.express as px
import matplotlib.pyplot as plt

the_dict = calc_all(1000000, 21)
master = {'days': [], 'count': []}
for key, values in the_dict.items():
        master['days'].append(key)
        master['count'].append(values['DL']['infected'])
print(type(the_dict))

fig = px.bar(master, x='days', y='count')
fig.write_image('fig1.jpeg')

"""
plt.style.use('ggplot')
df.plot(x='day',
        y= ['infected', 'susceptible', 'recovered'],
        color=['#aa6424', '#bbc6ca', '#cc8ac0'],
        kind='area',
        stacked= True)

df.plot.area()
plt.savefig('fig1.png')
"""

#function to return graph for a given state