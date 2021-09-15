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
     page_icon="./railway.png",
     layout="wide",
     initial_sidebar_state="expanded",
 )

 # this removes "Made with Streamlit"
hide_streamlit_style = """
<style>
#MainMenu {/*visibility: hidden;*/}
footer {visibility: hidden;}
</style>

"""

ns="{http://www.railml.org/schemas/2013}"
namespaces={'ns':'http://www.railml.org/schemas/2013'}

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.sidebar.title('RailML file viewer')
link = '[GitHub](http://github.com)'
#############################################################
@st.cache
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
    if elem is not None:
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
    if elem  is not None:
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
    try:
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
    except:
        st.write('exception get operating periods')
#    if elem  is not None:
#        del elem
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
    try:
        for _, elem in ET.iterparse(file_path, events=['end',], tag=[ns+'ocp',ns+'operationControlPoints'], remove_blank_text=True):
            if elem.tag == ns+'operationControlPoints':
                break
            ocps.append([elem.get('id'),
                        elem.get('code'),
                        elem.get('name'),
                        elem.get('description'),
                        elem.get('xml:lang'),
                        elem.get('type')])
            elem.clear()
        #elem.clear()
    except:
        st.write('exception getocps')
    #if elem  is not None:
    #    del elem
    return pd.DataFrame(ocps,columns=['ocpRef','code','station-name','description','lang','type'])

@st.cache
def get_speedChanges(file_path):
    tracks=[]
    speed_changes=[]
    gradient_Changes=[]
    radius_Changes=[]
    try:
        for _, track_part in ET.iterparse(file_path, events=['end',], tag=[ns+'track'], remove_blank_text=True):
            tracks.append([
                     track_part.get('id'),
                     track_part.get('code'),
                     track_part.get('name'),
                     track_part.get('type'),
                     track_part.find('.//'+ns+"trackBegin").get('pos'),
                     track_part.find('.//'+ns+"trackEnd").get('pos'),
                     track_part.find('.//'+ns+"trackBegin").get('absPos'),
                     track_part.find('.//'+ns+"trackEnd").get('absPos'),
                    ])
           # print('ok')

            for speedChange in track_part.iter(ns+'speedChange'):
              #  print('pp')
                speed_changes.append([
                        track_part.get('id'), #track_id
                       # ref_track[1], #track_code
                       # ref_track[2], #track_name
                       # ref_track[3], #track_type
                        speedChange.get('id'),
                        speedChange.get('pos'),
                        speedChange.get('absPos'),
                        speedChange.get('dir'),
                        speedChange.get('profileRef'),
                        speedChange.get('vMax')])
                speedChange.clear()

            for gradientChange in track_part.iter(ns+'gradientChange'):
              #  print('pp')
                gradient_Changes.append([
                        track_part.get('id'), #track_id
                       # ref_track[1], #track_code
                       # ref_track[2], #track_name
                       # ref_track[3], #track_type
                        gradientChange.get('id'),
                        gradientChange.get('pos'),
                        gradientChange.get('absPos'),
                        gradientChange.get('dir'),
                        gradientChange.get('slope')])
                gradientChange.clear()

            for radiusChange in track_part.iter(ns+'radiusChange'):
              #  print('pp')
                radius_Changes.append([
                        track_part.get('id'), #track_id
                       # ref_track[1], #track_code
                       # ref_track[2], #track_name
                       # ref_track[3], #track_type
                        radiusChange.get('id'),
                        radiusChange.get('pos'),
                        radiusChange.get('absPos'),
                        radiusChange.get('dir'),
                        radiusChange.get('radius')])
                radiusChange.clear()

    except:
        print('exception')
 #   print(speed_changes)
    return [pd.DataFrame(speed_changes,columns=['track_id','id_change','pos','absPos','dir','profileRef','vMax']) ,
pd.DataFrame(gradient_Changes,columns=['track_id','id_change','pos','absPos','dir','slope']) ,
pd.DataFrame(radius_Changes,columns=['track_id','id_change','pos','absPos','dir','radius']) ,
pd.DataFrame(tracks,columns=['id','code','name','type','begpos','endpos','begabspos','endabspos'])]


def get_trainParts(file_path):
    st.write('trainParts')
    trainParts = []
    try:
        for _, elem in ET.iterparse(file_path, events=['end',], tag=[ns+'trainPart',ns+'trainParts'], remove_blank_text=True):
            if elem.tag == ns+'trainParts':
                break
            trainParts.append([elem.get('id'),elem.get('code'),elem.get('line'),
                          elem.get('trainNumber'),elem.get('processStatus'),
                          elem.get('timetablePeriodRef'),elem.get('categoryRef')])
            elem.clear()
        #elem.clear()
    except:
        st.write('exception train parts')
    #if elem  is not None:
    #    del elem
    return pd.DataFrame(trainParts,columns=['trainPart-id','code','line','trainNumber',
                                            'processStatus','timetablePeriodRef',
                                            'categoryRef'])


def get_ocpTT(file_path):
    st.write('getOCPTT')
    ocpTTs = []
    try:
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

    except:
        st.write('ocp exception')
    #if elem  is not None:
    #    del elem
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













file_path = st.sidebar.file_uploader("Choose a railML file", type=["railml"])
st.sidebar.write('or use a railml sample file')
if st.sidebar.button('Ostsachsen_V220'):
    try:
        with open('samples/Ostsachsen_V220.railml','rb') as input:
            file_path=BytesIO(input.read())
    except FileNotFoundError:
        st.error('File not found.')
if st.sidebar.button('railML_SimpleExample_v11_railML3-1_04'):
    try:
        with open('samples/railML_SimpleExample_v11_railML3-1_04.railml','rb') as input:
            file_path=BytesIO(input.read())
    except FileNotFoundError:
        st.error('File not found.')

# Space out the maps so the first one is 2x the size of the other three

c0=st.container()
c1= st.container()

c2= st.container()
@st.cache()
def main2():
    if file_path is not None:



        list=['g','h']
        result=st.selectbox('bbababab',list)
        st.write(result)

        file_path.seek(0)

        speedChanges_df=get_speedChanges(file_path)
        file_path.seek(0)

        gc.collect()






    #

    #    st.write(gc.get_stats())
    #    st.write(gc.get_objects())





        st.subheader('line-changes')
        st.write(speedChanges_df[0])
        st.write(speedChanges_df[1])
        st.write(speedChanges_df[2])
        st.write(speedChanges_df[3])
    #c1.markdown(get_table_download_link_to_excel(speedChanges_df), unsafe_allow_html=True)
    #c1.markdown(get_table_download_link_to_csv(speedChanges_df), unsafe_allow_html=True)
        st.stop()





    if not file_path:
        st.warning('Please upload a railml file.')
        st.stop()
main2()
