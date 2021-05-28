from main import deriv, data_frame
import plotly.express as px


df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
fig.write_image("fig1.png")
