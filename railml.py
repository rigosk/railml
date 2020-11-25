import streamlit as st
import pandas as pd
#import sys
import lxml.etree as ET
import gc

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
namespaces={'ns':'http://www.railml.org/schemas/2013'}
ns='{http://www.railml.org/schemas/2013}'


def get_ocpTT2(file_path):
    ocpTTs = []
    for _, elem in ET.iterparse(file_path, events=('end'), tag=[ns+'trainParts',ns+'trainPart'], remove_blank_text=True):
        print('i')
        if elem.tag == ns+'trainParts':
            break
        operatingPeriod=elem.find('ns:operatingPeriodRef',namespaces=namespaces)

        for ocpTT in elem.findall('ns:ocpsTT/ns:ocpTT',namespaces=namespaces):
            ocpTT_dict=ocpTT.attrib
            times_dict=ocpTT.find('ns:times',namespaces=namespaces).attrib
            #print(times_dict)

        #ocpTTs=elem.find('ns:ocpsTT',namespaces=namespaces)
        #times=ocpTTs.find('ns:times',namespaces=namespaces)
        #trainPart=elem.xpath('parent::*/parent::node()',namespaces=namespaces)

        #print(len(operatingPeriod),operatingPeriod[0].get('ref'))
        #print(trainPart[0].get('id'))
        #print(dep_time.get('departure'))
        #ocp_code=elem.get('ocpRef')



            ocpTTs.append([elem.get('id'), #required !    #1
                           elem.get('code'),#optional       #2
                           elem.get('name'), #optional    #3
                           elem.get('description'), #optional    #4
                           #elem.get('xml:lang'),#optional    #5
                           elem.get('line'),#optional    #6
                           elem.get('trainLine'),#optional    #7
                           elem.get('trainNumber'),#optional    #8
                          # elem.get('additionalTrainNumber'),#optional    #9
                           elem.get('debitcode'),#optional    #10
                           elem.get('remarks'),#optional    #11
                           elem.get('timetablePeriodRef'),#optional    #12
                           elem.get('categoryRef'),#optional    #13
                           elem.get('operator'),#optional    #14
                           elem.get('cancellation'),#optional    #15
                           ocpTT_dict.get('sequence'),    #16
                           ocpTT_dict.get('ocpRef'),    #17
                           ocpTT_dict.get('ocpType'),    #18
                           times_dict.get('departure'),    #19
                           times_dict.get('arrival'),    #20
                           operatingPeriod.get('ref')                 #21
                          ])
        elem.clear()
    #elem.clear()
    del elem
    return pd.DataFrame(ocpTTs,columns=['trainPart-id', #1
                                        'trainPart-code',#2
                                        'trainPart-name',#3
                                        'trainPart-description',#4
                                       # 'trainPart-xml:lang',#5
                                        'trainPart-line',#6
                                        'trainPart-trainLine',#7
                                        'trainPart-trainNumber',#8
                                       # 'trainPart-additionalTrainNumber',#9
                                        'trainPart-debitcode',#10
                                        'trainPart-remarks',#11
                                        'trainPart-timetablePeriodRef',#12
                                        'trainPart-categoryRef', #13
                                        'trainPart-operator',#14
                                        'trainPart-cancellation',#15
                                        'sequence',#16
                                        'ocp-id',#17
                                        'ocpType',#18
                                        'departure_time',#19
                                        'arrival_time',   #20
                                        'operatingPeriod' #21
                                       ]).fillna('')


#this is to get the station names
def get_ocps(file_path):
    ocps=[]
    for _, elem in ET.iterparse(file_path, events="end", tag=[ns+'ocp',ns+'operationControlPoints'], remove_blank_text=True):
        if elem.tag == ns+'operationControlPoints':
            break
        ocps.append([elem.get('id'),elem.get('name')])
        elem.clear()
    #elem.clear()
    del elem
    return pd.DataFrame(ocps,columns=['ocp-id','station-name'])






st.title('Reading railML files')

st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example .railml input file](https://raw.githubusercontent.com/dataprofessor/data/master/penguins_example.csv)
""")



file_path = st.sidebar.file_uploader("Choose a railML file", type=["railml"])
if not file_path:
    st.warning('Please upload a railml file.')
    st.stop()
st.success('Thank you for inputting a name.')
if file_path is not None:
# read in a document
    #times=pd.DataFrame(get_ocpTT2(file_path))
    station_names=get_ocps(file_path)
    #merge1=pd.merge(times.reset_index(), station_names,on='ocp-id', how='left').set_index('index').sort_index()
    st.dataframe(station_names)
