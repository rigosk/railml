import streamlit as st
import lxml.etree as ET
import pandas as pd
import gc
import base64


st.set_page_config(
     page_title="railML file ",
     page_icon="🛤️",
     layout="wide",
     initial_sidebar_state="expanded",
 )
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index = False, sheet_name='Sheet1')
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) # Tried with '0%' and '#,##0.00' also.
    worksheet.set_column('A:A', None, format1) # Say Data are in column A
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Your_File.xlsx">Download Excel file</a>' # decode b'abc' => abc



st.markdown(hide_streamlit_style, unsafe_allow_html=True)
ns='{http://www.railml.org/schemas/2013}'
namespaces={'ns':'http://www.railml.org/schemas/2013'}


def get_table_download_link2(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="railml-table.csv">Download table as a csv file</a>'
    return href

@st.cache
def get_trainParts(file_path, match=''):
    trainParts = []
    for _, elem in ET.iterparse(file_path, events=("end",), tag=[ns+'trainPart',ns+'trainParts'], remove_blank_text=True):
        if elem.tag == ns+'trainParts':
            break
        trainParts.append([elem.get('id'),elem.get('code'),elem.get('line'),
                      elem.get('trainNumber'),elem.get('processStatus'),
                      elem.get('timetablePeriodRef'),elem.get('categoryRef')])
        elem.clear()
    #elem.clear()
    del elem

    return pd.DataFrame(trainParts)

st.title('RailML file viewer')


uploaded_file = st.sidebar.file_uploader("Choose a railML file", type=["railml"])

# Space out the maps so the first one is 2x the size of the other three
c1, c2 = st.beta_columns((1, 4))
if uploaded_file is not None:

    df=get_trainParts(uploaded_file)
    uploaded_file.seek(0)
    gc.collect()
    c2.write(df)
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)


    c2.markdown(get_table_download_link2(df), unsafe_allow_html=True)
placeholder = c1.empty()
if not st.checkbox("Hide dataframe"):
    df2 = pd.DataFrame([0,1,2,3])
    placeholder.dataframe(df2)
else:
    placeholder.empty()



if not uploaded_file:
    st.warning('Please upload a railml file.')
    st.stop()
