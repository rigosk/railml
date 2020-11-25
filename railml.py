import streamlit as st
import pandas as pd
import numpy as np
from lxml import etree

st.set_page_config(
    layout='wide',
    initial_sidebar_state='expanded',
    page_title='Railml reader',
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
st.sidebar.markdown('<p id="my-footer">Developed by <a  href="https://www.linkedin.com/in/konstantinosrigos/" target="_blank">Konstantinos Rigos</a></p>',unsafe_allow_html=True)


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
parser = etree.XMLParser(remove_blank_text=True)
#parser = etree.HTMLParser(recover=False)
def get_trains():
    trains_list=[]
    trains=railml.xpath('//ns:train',namespaces=namespaces)
    for i in range(len(trains)):
        dep_station=railml.xpath('//ns:train[@id="'+trains[i].get('id')+'"]/ns:trainPartSequence[@sequence="1"]/ns:trainPartRef',namespaces=namespaces)
        arr_station=railml.xpath('//ns:train[@id="'+trains[i].get('id')+'"]/ns:trainPartSequence[last()]/ns:trainPartRef',namespaces=namespaces)
        arr_station_name=railml.xpath('//ns:ocpTT[id="'+arr_station[0].get('ref')+'"]',namespaces=namespaces)
        trains_list.append([trains[i].get('trainNumber'),dep_station[0].get('ref'),arr_station_name[0].get('description')])
    return trains_list

st.title('Reading railML files')

st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/penguins_example.csv)
""")

name = st.text_input('Name')

uploaded_file = st.sidebar.file_uploader("Choose a railML file", type=["railml"])
if not uploaded_file:
    st.warning('Please upload a railml file.')
    st.stop()
st.success('Thank you for inputting a name.')
if uploaded_file is not None:
# read in a document
    #dom1 = minidom.parse(uploaded_file)
    root=etree.parse(uploaded_file,parser)
    #ocps = dom1.getElementsByTagName('ocp')
    railml=(root.getroot())

    #option = st.selectbox(
     #'What train you need information?',
     #(get_trains()))

    #st.write('You selected:', option)
    
############################################################
#print stations
    

    ocps = railml.xpath('//ns:ocp',namespaces=namespaces)
    #print(r)
    myDict={}
    for node in range(len(ocps)):
    #print(node)
    #print(r[node].get('id'))
        myDict[ocps[node].get('id')]=ocps[node].get('name')
        st.text(ocps[node].get('id'))
        st.text(ocps[node].attrib)
    st.text(myDict)

    ##################################################################


#print train parts
    my_bar = st.progress(0)



    train_parts=railml.xpath('//ns:trainPart',namespaces=namespaces)
    dict_list=[]
    for i in range(len(train_parts)):
        temp_dict=dict(train_parts[i].attrib)
        
        my_bar.progress((i+1)/len(train_parts))


        departure=railml.xpath('//ns:trainPart[@id="'+temp_dict['id']+'"]/ns:ocpsTT/ns:ocpTT[1]',namespaces=namespaces)
        arrival=railml.xpath('//ns:trainPart[@id="'+temp_dict['id']+'"]/ns:ocpsTT/ns:ocpTT[last()]',namespaces=namespaces)
        #st.write(myDict[departure[0].get('ocpRef')])
        temp_dict['departure']=myDict[departure[0].get('ocpRef')]
        temp_dict['arrival']=myDict[arrival[0].get('ocpRef')]
        
        dict_list.append(temp_dict)

    train_parts_list=pd.DataFrame.from_records(dict_list).fillna(0)
    st.dataframe(train_parts_list)
##############################################################
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
