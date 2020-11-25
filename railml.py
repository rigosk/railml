from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
st.set_page_config(
    layout='wide',
    initial_sidebar_state='expanded',
    page_title='Page Title',
    page_icon='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4vMQ4cL_Rf9dyzhTXyeCndOU7QQshyBy04w&usqp=CAU'
)

hide_streamlit_style="""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
#my-footer {
    text-align: center;
    position: fixed;
    bottom: 5%;
    }
</style>"""

st.markdown(hide_streamlit_style,unsafe_allow_html=True)
st.sidebar.markdown('<p id="my-footer">Made by <a  href="https://www.google.com" target="_blank">sdfs</a></p>',unsafe_allow_html=True)
import plotly_express as px
from plotly.offline import plot
iris = px.data.iris()
scatter_plot = px.scatter(iris, x="sepal_width", y="sepal_length")
st.write(scatter_plot)

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's :clock: desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""



@st.cache
def get_data():
    url = "http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv"
    return pd.read_csv(url)
df = get_data()

st.title("Streamlit 101: An in-depth introduction")
st.markdown("Welcome to this in-depth introduction to [...].")
st.header("Customary quote")
st.markdown("> I just love to go home, no matter where I am [...]")

st.dataframe(df.head())


cols = ["name", "host_name", "neighbourhood", "room_type", "price"]
st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)
st.write(st_ms)
st.dataframe(df[st_ms].head())


st.table(df.groupby("room_type").price.mean().reset_index()\
.round(2).sort_values("price", ascending=False)\
.assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
