import streamlit as st
import lxml.etree as ET
import numpy as np
import pandas as pd
import gc
import base64
from io import BytesIO
import sys


st.set_page_config(
     page_title="railML",
     page_icon="./favicon.ico",
     layout="wide",
     initial_sidebar_state="expanded",
 )
hide_streamlit_style = """
<style>
#MainMenu {/*visibility: hidden;*/}
footer {visibility: hidden;}
</style>

"""

ns="{http://www.railml.org/schemas/2013}"
namespaces={'ns':'http://www.railml.org/schemas/2013'}

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#############################################################

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output)
    df.to_excel(writer, index = False, sheet_name='Sheet1')
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    #format1 = workbook.add_format({'num_format': '0.00'}) # Tried with '0%' and '#,##0.00' also.
    #worksheet.set_column('A:A', None, format1) # Say Data are in column A
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link_to_excel(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Your_File.xlsx">Download Excel file</a>' # decode b'abc' => abc

def get_table_download_link_to_csv(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="railml-table.csv">Download table as a csv file</a>'
    return href
##########################################################3333333
#@st.cache
def get_trains(file_path):
    counter=0
    st.write('get_trains')
    trainPartREFS=[]

    for _, elem in ET.iterparse(file_path, events=["end"], tag=[ns+'train',ns+'trains'], remove_blank_text=True):
        if elem.tag == ns+'trains':
            break

        trainPartSequences=elem.findall('ns:trainPartSequence',namespaces=namespaces)
        for trainPartSequence in trainPartSequences:

            trainPartSequence_dict=trainPartSequence.attrib
            trainPartRefs=trainPartSequence.findall('ns:trainPartRef',namespaces=namespaces)
            for trainPartRef in trainPartRefs:

                trainPartRef_dict=trainPartRef.attrib

                trainPartREFS.append([elem.get('id'), #1
                                        elem.get('code'), #2
                                        elem.get('name'), #3
                                        elem.get('description'), #4
                                        elem.get('xml:lang'), #5
                                        elem.get('type'), #6
                                        elem.get('trainNumber'), #7
                                        elem.get('additionalTrainNumber'), #8
                                        elem.get('scope1'), #9
                                        elem.get('processStatus'), #10
                                        elem.get('cancellation'), #11
                                        trainPartSequence_dict['sequence'], #12
                                       # trainPartSequence_dict['pathStatus'], #13
                                      #  trainPartSequence_dict['categoryRef'],#14
                                        trainPartRef_dict['ref'], #15
                                      #  trainPartRef_dict['position'] #16
                      ])
               # st.write(trainPartREFS[counter])
               # counter=counter+1
               # st.write(counter)




        elem.clear()
    elem.clear()
    if elem:
        del elem
    gc.collect()

    return pd.DataFrame(trainPartREFS,columns=['train-id', #1
                                            'train-code',#2
                                            'train-name',#3
                                            'train-description',#4
                                            'train-xml:lang',#5
                                            'train-type',#6
                                            'train-trainNumber',#7
                                            'train-additionalTrainNumber',#8
                                            'train-scope', #9
                                            'train-processStatus', #10
                                            'train-cancellation', #11
                                            'trainPart-sequence', #12
                                         #   'trainPart-pathStatus', #13
                                          #  'trainPart-categoryRef',#14
                                            'trainPart-id', #15
                                            #'trainPartRef-position' #16
                                           ])
def get_categories(file_path):
    st.write('categories')
    categories=[]
    for _, elem in ET.iterparse(file_path, events=["end"], tag=[ns+'category',ns+'categories'], remove_blank_text=True):
        if elem.tag == ns+'categories':
            break

        categories.append([elem.get('id'), #1
                          elem.get('code'), #2
                          elem.get('name'), #3
                          elem.get('description'), #4
                          elem.get('xml:lang'), #5
                          elem.get('trainUsage'), #6
                          elem.get('deadrun'), #7
                          elem.get('categoryPriority')]) #8
        elem.clear()
    elem.clear()
    if elem:
        del elem
    return pd.DataFrame(categories,columns=['category-id', #1
                                            'category-code',#2
                                            'category-name',#3
                                            'category-description',#4
                                            'category-xml:lang',#5
                                            'category-trainUsage',#6
                                            'category-deadrun',#7
                                            'category-categoryPriority',#8
                                           ])

def get_operating_periods(file_path):
    st.write('get_operating_periods')
    operatingPeriods=[]
    for _, elem in ET.iterparse(file_path, events=["end"], tag=[ns+'operatingPeriod',ns+'operatingPeriods'], remove_blank_text=True):
        if elem.tag == ns+'operatingPeriods':
            break
        operatingPeriods.append([elem.get('id'), #1
                                 elem.get('code'), #2
                                 elem.get('name'), #3
                                 elem.get('description'), #4
                                 elem.get('xml:lang'), #5
                                 elem.get('timetablePeriodRef'), #6
                                 elem.get('startDate'), #7
                                 elem.get('endDate'), #8
                                 elem.get('bitMask')])  #9
        elem.clear()
    elem.clear()
    if elem:
        del elem
    return pd.DataFrame(operatingPeriods,columns=['operatingPeriod', #1
                                                  'operatingPeriod-code',#2
                                                  'operatingPeriod-name',#3
                                                  'operatingPeriod-description',#4
                                                  'operatingPeriod-xml:lang',#5
                                                  'operatingPeriod-timetablePeriodRef',#6
                                                  'operatingPeriod-startDate',#7
                                                  'operatingPeriod-endDate',#8
                                                  'operatingPeriod-bitMask',#9
                                           ])
def get_ocps(file_path):
    st.write('getocps')
    ocps=[]
    for _, elem in ET.iterparse(file_path, events=['end',], tag=[ns+'ocp',ns+'operationControlPoints'], remove_blank_text=True):
        if elem.tag == ns+'operationControlPoints':
            break
        ocps.append([elem.get('id'),elem.get('name')])
        elem.clear()
    #elem.clear()
    if elem:
        del elem
    return pd.DataFrame(ocps,columns=['ocpRef','station-name'])


def get_trainParts(file_path):
    st.write('trainParts')
    trainParts = []
    for _, elem in ET.iterparse(file_path, events=['end',], tag=[ns+'trainPart',ns+'trainParts'], remove_blank_text=True):
        if elem.tag == ns+'trainParts':
            break
        trainParts.append([elem.get('id'),elem.get('code'),elem.get('line'),
                      elem.get('trainNumber'),elem.get('processStatus'),
                      elem.get('timetablePeriodRef'),elem.get('categoryRef')])
        elem.clear()
    #elem.clear()
    if elem:
        del elem
    return pd.DataFrame(trainParts,columns=['trainPart-id','code','line','trainNumber',
                                            'processStatus','timetablePeriodRef',
                                            'categoryRef'])

def get_ocpTT(file_path):
    st.write('getOCPTT')
    ocpTTs = []
    for _, elem in ET.iterparse(file_path, events=["end",], tag=[ns+'trainPart',ns+'trainParts'], remove_blank_text=True):
        if elem.tag == ns+'trainParts':
            st.write('trainParts')
            break
        operatingPeriod_elem=elem.find('ns:operatingPeriodRef',namespaces=namespaces)
        #print(len(operatingPeriod_elem))
        if operatingPeriod_elem is not None:
            operatingPeriod=operatingPeriod_elem.get('ref')
        else:
            operatingPeriod=''
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
                           times_dict.get('arrival'),    #19
                           times_dict.get('departure'),    #20
                           operatingPeriod      #21
                          ])
        elem.clear()
    st.write('break')
    for value in dir():
        st.write(value,sys.getsizeof(value))
    st.write(dir())
    #elem.clear()
    if elem:
        del elem
    gc.collect()
    for value in dir():
        st.write(value,sys.getsizeof(value))
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
                                        'category-id', #13
                                        'trainPart-operator',#14
                                        'trainPart-cancellation',#15
                                        'trainPart-sequence',#16
                                        'ocpRef',#17
                                        'ocpType',#18
                                        'arrival_time',   #19
                                        'departure_time',#20
                                        'operatingPeriod' #21
                                       ])

#
def main(file_path):
    for _ in range(1):
        file_path.seek(0)
        times=get_ocpTT(file_path)
        file_path.seek(0)
        station_names=get_ocps(file_path)
        st.write(sys.getsizeof(station_names))
        file_path.seek(0)
        merge1=pd.merge(times.reset_index(), station_names, on='ocpRef', how='left').set_index('index').sort_index()
        del times
        del station_names
        file_path.seek(0)
        merge1=pd.merge(merge1,get_operating_periods(file_path),on='operatingPeriod', how='left')
        file_path.seek(0)
        st.write(sys.getsizeof(merge1))
        file_path.seek(0)
        st.write(sys.getsizeof(get_trains(file_path)))
        file_path.seek(0)
        merge1=pd.merge(merge1,get_trains(file_path),on='trainPart-id', how='left')

    return merge1.dropna(axis=1,how='all',inplace=False)






st.title('RailML file viewer')
link = '[GitHub](http://github.com)'






file_path = st.sidebar.file_uploader("Choose a railML file", type=["railml"])


# Space out the maps so the first one is 2x the size of the other three
c1, c2 = st.beta_columns((1, 4))
if file_path is not None:

    st.write(type(file_path))

#    st.write(gc.get_stats())
#    st.write(gc.get_objects())
    df=get_trainParts(file_path)
    ocp_df=getocps(fle_path)
    ocpTT_df=getOCPTT(file_path)
    file_path.seek(0)
    gc.collect()
    c2.write(df)
    st.markdown(get_table_download_link_to_excel(df), unsafe_allow_html=True)


    c2.markdown(get_table_download_link_to_csv(df), unsafe_allow_html=True)

    st.dataframe(ocp_df)
    st.markdown(get_table_download_link_to_excel(ocp_df), unsafe_allow_html=True)


    c2.markdown(get_table_download_link_to_csv(ocp_df), unsafe_allow_html=True)

    st.write(ocpTT_df)
    st.markdown(get_table_download_link_to_excel(ocpTT_df), unsafe_allow_html=True)


    c2.markdown(get_table_download_link_to_csv(ocpTT_df), unsafe_allow_html=True)


placeholder = c1.empty()
if not st.checkbox("Hide dataframe"):
    df2 = pd.DataFrame([0,1,2,3])
    placeholder.dataframe(df2)
else:
    placeholder.empty()



if not file_path:
    st.warning('Please upload a railml file.')
    st.stop()
