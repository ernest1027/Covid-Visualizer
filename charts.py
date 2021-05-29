from main import deriv, data_frame
import plotly.express as px
import matplotlib.pyplot as plt

print (data_frame())

df = data_frame()

plt.style.use('ggplot')
df.plot(x='day',
        y= ['infected', 'susceptible', 'recovered'],
        color=['#aa6424', '#bbc6ca', '#cc8ac0'],
        kind='area',
        stacked= True)

df.plot.area()
plt.savefig('fig1.png')

#function to return graph for a given state